from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Digits
from textual.containers import HorizontalGroup, VerticalScroll
from textual.reactive import reactive
from time import monotonic


class TimeDisplay(Digits):
    start_time = reactive(monotonic)
    time = reactive(0.0)
    total_time = reactive(0.0)

    def on_mount(self) -> None:
        """사건 취급자가 위젯이 앱에 추가될 때 이 메소드를 호출합니다."""
        self.update_timer = self.set_interval(
            1 / 60,
            self.update_time,
            pause=True,
        )

    def update_time(self) -> None:
        self.time = self.total_time + (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def start(self) -> None:
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        self.update_timer.pause()
        self.total_time += monotonic() - self.start_time
        self.time = self.total_time

    def reset(self) -> None:
        self.time = 0.0
        self.total_time = 0.0


class Stopwatch(HorizontalGroup):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        time_display = self.query_one(TimeDisplay)

        if event.button.id == "start":
            time_display.start()
            self.add_class("started")

        elif event.button.id == "stop":
            time_display.stop()
            self.remove_class("started")

        elif event.button.id == "reset":
            time_display.reset()

    def compose(self):
        yield Button("시작", id="start", variant="success")
        yield Button("정지", id="stop", variant="error")
        yield Button("다시 맞추기", id="reset")
        yield TimeDisplay()


class StopwatchApp(App):
    CSS_PATH = "stopwatch.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "다크 모드"),
        ("a", "add_stopwatch", "스톱워치 추가"),
        ("r", "remove_stopwatch", "스톱워치 삭제"),
    ]

    def compose(self) -> ComposeResult:
        """위젯을 추가합니다."""
        yield Header()
        yield Footer()
        yield VerticalScroll(
            Stopwatch(),
            Stopwatch(),
            Stopwatch(),
            id="timers",
        )

    def action_add_stopwatch(self) -> None:
        """스톱워치를 추가하는 액션입니다."""
        new_stopwatch = Stopwatch()
        self.query_one("#timers").mount(new_stopwatch)
        new_stopwatch.scroll_visible()

    def action_remove_stopwatch(self) -> None:
        timers = self.query("Stopwatch")
        if timers:
            timers.last().remove()

    def action_toggle_dark(self) -> None:
        """다크 모드로 전환하는 액션입니다."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = StopwatchApp()
    app.run()
