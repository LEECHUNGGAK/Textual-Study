from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Digits
from textual.containers import HorizontalGroup, VerticalScroll
from textual.reactive import reactive
from time import monotonic


class TimeDisplay(Digits):
    start_time = reactive(monotonic)
    time = reactive(0.0)

    def on_mount(self) -> None:
        """사건 취급자가 위젯이 앱에 추가될 때 이 메소드를 호출합니다."""
        self.set_interval(1 / 60, self.update_time)

    def update_time(self) -> None:
        self.time = monotonic() - self.start_time

    def watch_time(self, time: float) -> None:
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02.0f}:{minutes:02.0f}:{seconds:05.2f}")


class Stopwatch(HorizontalGroup):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.add_class("started")

        elif event.button.id == "stop":
            self.remove_class("started")

    def compose(self):
        yield Button("시작", id="start", variant="success")
        yield Button("정지", id="stop", variant="error")
        yield Button("다시 맞추기", id="reset")
        yield TimeDisplay("00:00:00.00")


class StopwatchApp(App):
    CSS_PATH = "stopwatch.tcss"
    BINDINGS = [("d", "toggle_dark", "다크 모드")]

    def compose(self) -> ComposeResult:
        """위젯을 추가합니다."""
        yield Header()
        yield Footer()
        yield VerticalScroll(
            Stopwatch(),
            Stopwatch(),
            Stopwatch(),
        )

    def action_toggle_dark(self) -> None:
        """다크 모드로 전환하는 액션입니다."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = StopwatchApp()
    app.run()
