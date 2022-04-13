import rich_click

from rich.console import Console
from rich.table import Table

from .scanner import Scanner


@rich_click.command()
@rich_click.argument("target", type=rich_click.types.STRING,)
def main(target: str):
    console = Console()

    console.print("""
[cyan]
 _   |_  _| _ |_
_)|_||_)(_|(_|| | [green]2.0.0[/]
[bright_black]-> [green]github.com/traumatism[/][/]
[/]
    """)

    console.log("Starting subdah...")

    scanner = Scanner(
        target,
        verbose=True,
        console=console
    )

    console.log("Enumerating subdomains...")

    subdomains = scanner.scan()

    console.log("Resolving subdomains...")

    table = Table(show_header=True)

    table.add_column("#", style="bright_black")
    table.add_column("Subdomain", style="cyan")
    table.add_column("IP Address", style="green")

    for idx, subdomain in enumerate(subdomains):
        row = map(str, (idx, subdomain.subdomain, subdomain.ip_address() or "n/a"))
        table.add_row(*row)

    console.print(table)

    console.log("Done!")

if __name__ == "__main__":
    main()
