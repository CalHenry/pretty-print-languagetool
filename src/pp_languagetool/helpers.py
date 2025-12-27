import json
import subprocess

import typer
from docx import Document
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


# run languagetool as a subprocess
def run_languagetool(text: str, language: str) -> dict:
    """
    Run languagetool cli and return json output
    Compute the line and col position of the error
    args:
        text: text to be analysed by languagetool
        language: language of the text
    """
    try:
        # Build offset mapping before sending to languagetool
        offset_map = build_offset_to_line_col_map(text)

        # languagetool command
        result = subprocess.run(
            ["languagetool", "-l", language, "--json"],
            input=text,
            text=True,
            capture_output=True,
            check=True,
        )

        # Parse JSON output
        lt_output = json.loads(result.stdout)

        # Add line/col information to each match
        for match in lt_output.get("matches", []):
            offset = match["offset"]
            if offset in offset_map:
                line, col = offset_map[offset]
                match["line"] = line
                match["column"] = col

        return lt_output

    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error running languagetool:[/red] {e.stderr}")
        raise typer.Exit(1)
    except json.JSONDecodeError as e:
        console.print(f"[red]Error parsing languagetool output:[/red] {e}")
        raise typer.Exit(1)
    except FileNotFoundError:
        console.print(
            "[red]Error: languagetool command not found. Please install it first.[/red]"
        )
        raise typer.Exit(1)


def build_offset_to_line_col_map(text: str) -> dict:
    """Build a mapping from character offset to (line, column) position.

    Args:
        text: The input text

    Returns:
        A dict with offset as key and (line, col) tuple as value
    """
    offset_map = {}
    line = 1
    col = 1

    for offset, char in enumerate(text):
        offset_map[offset] = (line, col)
        if char == "\n":
            line += 1
            col = 1
        else:
            col += 1

    # Add one more entry for the position right after the last character
    offset_map[len(text)] = (line, col)

    return offset_map


####
def pretty_print_languagetool_report(content: dict):
    # Header
    console.print(
        Panel.fit(
            "[bold cyan]LanguageTool Report[/bold cyan]",
            border_style="cyan",
        )
    )
    # Summary stats
    total_matches = len(content["matches"])
    console.print(f"\n[bold]Total issues found:[/bold] {total_matches}\n")
    # Issues table
    table = Table(
        show_header=True,
        header_style="bold magenta",
        leading=1,
        box=box.ROUNDED,
    )
    table.add_column(
        "Line:Col", style="dim", max_width=8
    )  # Made slightly wider for "Line:Col" format
    table.add_column("Type", style="cyan")
    table.add_column("Message", style="yellow")
    table.add_column("Context", style="white")
    table.add_column("Correction", style="white")

    # Loop through all matches
    for match in content["matches"]:
        # Extract relevant elements
        # issue info
        issue_type = match["rule"]["issueType"]
        mess_content = match["message"]

        # error coord - now using the line and column we added
        error_offset = match["context"]["offset"]
        error_len = match["context"]["length"]

        # Extract context parts
        context_text = match["context"]["text"]
        before_bad_element = context_text[:error_offset]
        bad_element = context_text[error_offset : error_offset + error_len]
        after_bad_elements = context_text[error_offset + error_len :]

        # Build corrections text ('bad → correction')
        replacements = match["replacements"]
        corrections = [r["value"] for r in replacements]
        if corrections:
            # First line with bad word and arrow to first correction
            correction_text = (
                f"[red]{bad_element}[/red] → [green]{corrections[0]}[/green]"
            )
            # Add remaining corrections, padded to align with first correction
            padding = " " * (len(bad_element) + 1)
            for correction in corrections[1:3]:  # [1:3] we limit to 3 corrections
                correction_text += f"\n{padding}→ [green]{correction}[/green]"
        else:
            correction_text = "[dim]No suggestions[/dim]"

        # if issue is about whitespaces, change the elements for simpler info, tell the number of whitespaces
        if issue_type == "whitespace":
            correction_text = f"→ remove {error_len} whitespaces"
        else:
            correction_text = correction_text

        # Get line and col number from the match -  added to languagetool json report in 'run_languagetool'
        line_number = match.get("line", "?")
        column_number = match.get("column", "?")
        location = f"{line_number}:{column_number}"

        # Add row to table
        table.add_row(
            location,
            f"{issue_type}",
            f"{mess_content}",
            f"{before_bad_element}[red underline]{bad_element}[/red underline]{after_bad_elements}",
            f"{correction_text}",
        )

    # Display table
    console.print(table)


def docx_to_text(docx_path: str) -> str:
    """
    Convert .docx files (Windows Word 2007+) to plain text
    no support for tables
    """
    doc = Document(docx_path)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return "\n".join(full_text)
