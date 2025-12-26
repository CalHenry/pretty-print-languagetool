from typing import Optional

import typer
from rich.console import Console

from .helpers import pretty_print_languagetool_report, run_languagetool

console = Console()
app = typer.Typer()


# wrapper around languagetool command. We repeat the options - might add more
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
    args:
        language: get the list of supported languages with 'languagetool --list'. Specify the region (like en-GB) to enable spell checking
        text: cli argument or stdin text
        file: plain text file. LanguageTool don't read XML, docx, tex, HTML or other non plain text formats
    """

    # Get text from argument or stdin
    if text:
        input_text = text
        input_name = "the text"
    elif file:
        input_text = file.read()
        input_name = f"{file.name}"
    else:
        console.print("[yellow]Reading from stdin (Ctrl+D to finish)...[/yellow]")
        input_text = typer.get_text_stream("stdin").read()
        input_name = "stdin text"
    if not input_text.strip():
        console.print("[red]Error: No text provided[/red]")
        raise typer.Exit(1)

    # Run languagetool
    with console.status(
        f"[bold green]LanguageTool is working on [underline]{input_name}[/underline] ({language})..."
    ):
        results = run_languagetool(input_text, language)

    # Pretty print results
    pretty_print_languagetool_report(results)


if __name__ == "__main__":
    app()
