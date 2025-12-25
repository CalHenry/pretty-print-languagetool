from typing import Optional

import typer
from rich.console import Console

from .helpers import pretty_print_languagetool_report, run_languagetool

console = Console()
app = typer.Typer()


@app.command()
def check(
    language: str = typer.Option(
        "en-US", "-l", "--language", help="Language code (e.g., en-US, de-DE, fr)"
    ),
    text: Optional[str] = typer.Option(None, "-t", "--text", help="Text to check"),
    file: Optional[typer.FileText] = typer.Option(
        None, "-f", "--file", help="File to check"
    ),
):
    """
    Check text with LanguageTool and display results with Rich formatting.
    """

    # Get text from argument or stdin
    if text:
        input_text = text
    elif file:
        input_text = file.read()
    else:
        console.print("[yellow]Reading from stdin (Ctrl+D to finish)...[/yellow]")
        input_text = typer.get_text_stream("stdin").read()

    if not input_text.strip():
        console.print("[red]Error: No text provided[/red]")
        raise typer.Exit(1)

    # Run languagetool
    with console.status(f"[bold green]Checking text with LanguageTool ({language})..."):
        results = run_languagetool(input_text, language)

    # Pretty print results
    pretty_print_languagetool_report(results)


if __name__ == "__main__":
    app()
