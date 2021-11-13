from re import sub
import sys
import time
import json
import itertools

from rich.tree import Tree
from rich.panel import Panel
from rich.status import Status
from rich.columns import Columns

from rich.progress import (
    BarColumn, Progress, SpinnerColumn, TextColumn,
    TimeElapsedColumn, TimeRemainingColumn,
    BarColumn
)
from lib import (
    __version__, database, console
)

from lib.logger import Logger

from lib.common.abc import Module

from lib.arguments import arguments

from lib.utils.threading import (
    start_module_thread, 
    wait_for_threads_to_stop
)


from modules.securitytrails import SecurityTrails
from modules.hackertarget import Hackertarget
from modules.threatcrowd import ThreatCrowd
from modules.threatminer import ThreatMiner
from modules.duckduckgo import DuckDuckGo
from modules.alienvault import AlienVault
from modules.fullhunt import FullHunt
from modules.twitter import Twitter
from modules.anubis import Anubis
from modules.shodan import Shodan
from modules.google import Google
from modules.crtsh import CRTSh
from modules.yahoo import Yahoo
from modules.qwant import Qwant

modules = (
    Hackertarget, CRTSh, AlienVault, FullHunt,
    ThreatMiner, Shodan, ThreatCrowd, Yahoo,
    Anubis, SecurityTrails, Twitter, Google,
    DuckDuckGo, Qwant
)


if __name__ == "__main__":

    for module in modules:
        if not issubclass(module, Module):
            Logger.warning("<%s> is not a subclass of <lib.common.abc.Module> !" % module.__name__)

    console.print(r"""[bold yellow]
             _     _     _   
     ___ _ _| |_ _| |___| |_ 
    |_ -| | | . | . | .'|   |
    |___|___|___|___|__,|_|_| [white]([cyan]v%s[/cyan])[/white][/bold yellow]

    [cyan]the third eye for subdomains 👁[/cyan]
     
    [green]github.com/traumatism[/green]

    """ % __version__)

    target_domain = arguments.domain.lower()

    if "," in target_domain:
        target_domains = target_domain.split(",")
    else:
        target_domains = [target_domain]

    Logger.info("Starting...")

    start_time = time.time()

    with Progress(
        SpinnerColumn(finished_text="[bold green]✓[/bold green]"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=True
    ) as progress:

        task_1 = progress.add_task(
            "[bold magenta]Running modules       [bold yellow](waiting)[/bold yellow][/bold magenta]", 
            total=len(modules) * len(target_domains), start=False
        )
            
        task_2 = progress.add_task(
            "[bold magenta]Resolving subdomains  [bold yellow](waiting)[/bold yellow][/bold magenta]", 
            total=0, start=False
        )

        task_3 = progress.add_task(
            "[bold magenta]Grabbing HTTP servers [bold yellow](waiting)[/bold yellow][/bold magenta]", 
            total=0, start=False
        )

        progress.start_task(task_1)

        progress.update(task_1, description="[bold magenta]Running modules       [bold cyan](running)[/bold cyan][/bold magenta]")

        for target_domain in target_domains:
            for module in (module(target_domain) for module in modules):
                start_module_thread(module)
                progress.advance(task_1, 1)

        wait_for_threads_to_stop()
        
        progress.update(task_1, description="[bold magenta]Running modules       [bold green](done)[/bold green][/bold magenta]")

        results = database.get_subdomains()

        if not results:
            Logger.error("No results found")
            sys.exit(1)

        progress.update(task_2, total=len(results))
        
        progress.update(task_3, total=len(results))

        progress.start_task(task_2)

        progress.update(task_2, description="[bold magenta]Resolving subdomains  [bold cyan](running)[/bold cyan][/bold magenta]", )

        for subdomain in results:

            progress.advance(task_2, 1)

            resolutions = subdomain.resolve() if subdomain.resolvable is True else None

            if resolutions is None:
                continue

            for address in resolutions:
                database.update_subdomain(subdomain, address)

        progress.update(task_2, description="[bold magenta]Resolving subdomains  [bold green](done)[/bold green][/bold magenta]", )

        progress.start_task(task_3)

        progress.update(task_3, description="[bold magenta]Grabbing HTTP servers [bold cyan](running)[/bold cyan][/bold magenta]")

        for subdomain in results:
            progress.advance(task_3, 1)

            if subdomain.resolvable is False:
                continue

            subdomain.grab_http_banner()
            
        progress.update(task_3, description="[bold magenta]Grabbing HTTP servers [bold green](done)[/bold green][/bold magenta]")

    colors = itertools.cycle(("bold green", "dim green"))

    trees = []

    for domain in {subdomain.domain for subdomain in database.get_subdomains()}:
        main_tree = Tree(f"[green bold]+[/green bold] {domain}")

        for subdomain in database.get_subdomains():
            if subdomain.domain != domain:
                continue

            tree = main_tree.add(f"[green bold]+[/green bold] {subdomain}")

            if subdomain.http_banner is not None:
                tree.add(f"[green bold]+[/green bold] {subdomain.http_banner}")

            if subdomain.resolvable is False:
                tree.add('[red bold]-[/red bold] unresolvable\n')

            if subdomain.resolutions is not None and len(subdomain.resolutions) >= 1:
                resolutions_tree = tree.add(f"[green bold]+[/green bold] resolutions ({len(subdomain.resolutions)})")

                for i, ip_addr in enumerate(subdomain.resolutions):

                    if i == len(subdomain.resolutions) - 1:
                        resolutions_tree.add(f"[green bold]+[/green bold] {ip_addr}\n")
                        continue
    
                    resolutions_tree.add(f"[green bold]+[/green bold] {ip_addr}")

        trees.append(main_tree)

    console.print(Columns(trees))

    if arguments.output_file is not False:
        json_data = {domain: [] for domain in target_domains}

        for subdomain in database.get_subdomains():

            report = {
                "hostname": str(subdomain),
                "resolvable": subdomain.resolvable,
                "resolutions": subdomain.resolutions,
                "http_server": subdomain.http_banner,
            }

            json_data[subdomain.domain].append(report)

        with open(arguments.output_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(json_data, indent=4))

    end_time = time.time()

    Logger.success(f"Finished in {round(end_time - start_time, 2)} seconds.")
