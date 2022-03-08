from rich.console import Console
from rich.status import Status
from rich.style import Style
from rich.theme import Theme


class Spinner:
    def __init__(self, text: str):
        self.spinner = Status(
            status=text,
            spinner="dots"
        )
        self.spinner.start()

    def stop(self):
        self.spinner.stop()
        del self


theme = Theme({
        "log": Style(
            color="white"
        ),
        "success": Style(
            color="green",
            bold=True,
            underline=True
        ),
        "error": Style(
            color="red",
            bold=True,
            underline=True
        )
    })

console = Console(
            theme=theme,
            highlight=False
)
