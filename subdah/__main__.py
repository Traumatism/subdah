import rich_click

from rich.console import Console
from rich.table import Table

from subdah.utils import json_to_rich_table

from .scanner import Scanner


@rich_click.command()
@rich_click.argument("target", type=rich_click.types.STRING,)
@rich_click.option("-s", "--no-shodan", is_flag=True, default=False, help="Disable using Shodan to lookup the results")
def main(target: str, no_shodan: bool):
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

    table = Table(show_header=True, show_lines=True)

    table.add_column("#", style="bright_black")
    table.add_column("Subdomain", style="cyan")
    table.add_column("IP Address", style="green")

    if not no_shodan:
        table.add_column("Shodan", style="cyan")

    for idx, subdomain in enumerate(subdomains):
        row = (
            str(idx),
            subdomain.subdomain,
            subdomain.ip_address() or "n/a"
        )

        if not no_shodan:
            row += (json_to_rich_table(subdomain.internetdb()), )

        table.add_row(*row)

    console.print(table)

    console.log("Done!")

if __name__ == "__main__":
    main()
