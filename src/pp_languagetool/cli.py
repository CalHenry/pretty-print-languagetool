import subprocess
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .helpers import (
    docx_to_text,
    pretty_print_languagetool_report,
    run_languagetool,
)

console = Console()
app = typer.Typer()


# wrapper around languagetool command. We repeat the options - might add more
@app.command()
def check(
    language: str = typer.Option(
        "en-US", "-l", "--language", help="Language code (e.g., en-GB, fr)"
    ),
    text: Optional[str] = typer.Option(None, "-t", "--text", help="Text to check"),
    file: Optional[str] = typer.Option(None, "-f", "--file", help="File to check"),
    list_languages: bool = typer.Option(
        False, "--list", is_eager=True, help="Print all available languages and exit."
    ),
):
    """
    Check text with LanguageTool and display the results in a simple table with colors.
    """
    # just list the available language - mimics 'languagetool --list'
    if list_languages:
        result = subprocess.run(
            ["languagetool", "--list"],
            capture_output=True,
            text=True,
        )
        console.print(result.stdout)
        raise typer.Exit(0)

    # Get text from argument or stdin
    if text:
        input_text = text
        input_name = "the text"
    elif file:
        file_path = Path(file)
        if file_path.suffix.lower() == ".docx":  # handle docx files
            input_text = docx_to_text(file_path)
        else:
            with open(file, "r", encoding="utf-8") as f:
                input_text = f.read()
        input_name = file_path.name
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
