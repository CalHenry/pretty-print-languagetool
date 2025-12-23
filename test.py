import json
from tkinter import OFF

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# load content - test file - not automatic
with open("test_inputs/rm.json", "r", encoding="utf-8") as f:
    content = json.load(f)


# extract relevant elements from the json file
indice = 8  # testing purposes
# ####
error_offset = content["matches"][indice]["context"]["offset"]
error_len = content["matches"][indice]["context"]["length"]

issue_type = content["matches"][indice]["rule"]["issueType"]
mess_content = content["matches"][indice]["message"]

# context = content["matches"][indice]["context"]["text"]
before_bad_element = content["matches"][indice]["context"]["text"][:error_offset]
after_bad_elements = content["matches"][indice]["context"]["text"][
    error_offset + error_len :
]

bad_element = content["matches"][indice]["context"]["text"][
    error_offset : error_offset + error_len
]
correction_proposal = content["matches"][indice]["replacements"][0]["value"]

replacements = content["matches"][indice]["replacements"]
corrections = [r["value"] for r in replacements]
if corrections:
    # First line with bad word and arrow to first correction
    correction_text = f"[red]{bad_element}[/red] → [green]{corrections[0]}[/green]"

    # Add remaining corrections, padded to align with first correction
    padding = " " * (len(bad_element) + 1)
    for correction in corrections[1:]:
        correction_text += f"\n{padding}→ [green]{correction}[/green]"
else:
    correction_text = ""


# Rich #################
console = Console()

# Header
console.print(
    Panel.fit("[bold cyan]LanguageTool Report[/bold cyan]", border_style="cyan")
)

# Summary stats


# Issues table
table = Table(show_header=True, header_style="bold magenta")
table.add_column("Line", style="dim", width=6)
table.add_column("Type", style="cyan")
table.add_column("Message", style="yellow")
table.add_column("Context", style="white")
table.add_column("Correction", style="white")

table.add_row(
    "15",
    f"{issue_type}",
    "Subject-verb agreement",
    f"{before_bad_element}[red underline]{bad_element}[/red underline]{after_bad_elements}",
    f"{correction_text}",
    # f"[red]{bad_element}[/red] → [green]{corrections}[/green]",
)

console.print(table)

# Severity colors
console.print("\n[red]● Error[/red]  [yellow]● Warning[/yellow]  [blue]● Info[/blue]")
