import sys
import time
import json

from rich.box import SIMPLE
from rich.table import Table
from rich.status import Status
from rich.progress import Progress

from lib.logger import Logger
from lib.common.abc import Module
from lib.arguments import arguments

from lib.utils.threading import (
    start_module_thread, wait_for_threads_to_stop
)

from lib import (
    __version__, database
)

from modules.securitytrails import SecurityTrails
from modules.hackertarget import Hackertarget
from modules.threatcrowd import ThreatCrowd
from modules.threatminer import ThreatMiner
from modules.alienvault import AlienVault
from modules.fullhunt import FullHunt
from modules.twitter import Twitter
from modules.anubis import Anubis
from modules.shodan import Shodan
from modules.google import Google
from modules.crtsh import CRTSh
from modules.yahoo import Yahoo


modules = (
    Hackertarget, CRTSh, AlienVault, FullHunt,
    ThreatMiner, Shodan, ThreatCrowd, Yahoo,
    Anubis, SecurityTrails, Twitter, Google
)


if __name__ == "__main__":

    for module in modules:
        if not issubclass(module, Module):
            Logger.warning("<%s> is not a subclass of <lib.common.abc.Module> !" % module.__name__)

    Logger.console.print(r"""[bold yellow]
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

    for j, target_domain in enumerate(target_domains):

        with Status(
            f"Running modules... (0/{len(modules)}, found {database.count}, job {j + 1}/{len(target_domains)})",
            console=Logger.console, spinner="moon"
        ) as status:

            for i, module in enumerate(module(target_domain) for module in modules):

                status.update(
                    f"Running modules... ({i}/{len(modules)}, found {database.count}), job {j + 1}/{len(target_domains)}",
                    spinner="moon"
                )

                start_module_thread(module)

        wait_for_threads_to_stop()

    results = database.get_subdomains()

    if not results:
        Logger.error("No results found")
        sys.exit(1)

    Logger.success(f"Found {len(results)} results!")

    # gotta improve this boolean logic, lol.
    if arguments.dont_resolve is False or arguments.dont_gather_http is False:

        with Progress() as progress:
            resolve, probe_http = None, None

            if arguments.dont_resolve is False:
                resolve = progress.add_task(
                    "[bold magenta]Resolving subdomains[/bold magenta]", 
                    total=len(results), start=False
                )

            if arguments.dont_gather_http is False:
                probe_http = progress.add_task(
                    "[bold magenta]Gathering HTTP banners[/bold magenta]", 
                    total=len(results), start=False
                )

            if resolve is not None:
                progress.start_task(resolve)

                for subdomain in results:

                    progress.advance(resolve, 1)

                    if subdomain.resolvable is False:
                        continue

                    resolutions = subdomain.resolve()

                    if resolutions is None:
                        continue

                    for address in resolutions:
                        database.update_subdomain(subdomain, address)

            if probe_http is not None:
                progress.start_task(probe_http)

                for subdomain in results:

                    progress.advance(probe_http, 1)

                    if subdomain.resolvable is False:
                        continue

                    subdomain.gather_http_banner()

        table = Table(
            row_styles=("none", "dim"),
            box=SIMPLE
        )

        table.add_column(
            "#",
            style="cyan"
        )

        table.add_column(
            "Subdomain",
            style="green"
        )

        table.add_column(
            "Resolutions",
            style="green"
        )

        table.add_column(
            "HTTP banner",
            style="green"
        )

        for i, subdomain in enumerate(results):
            row = (str(i), str(subdomain),)

            if arguments.dont_resolve is False:
                resolutions = subdomain.resolve()
                row += (", ".join(resolutions), ) if resolutions is not None else ("n/a", )

            if arguments.dont_gather_http is False:
                row += (subdomain.http_banner,)

            table.add_row(*row)

        Logger.console.print(table)

    else:
        for subdomain in results:
            Logger.console.print(f"[green]*[/green] [white]{subdomain}[/white]")


    if arguments.output_file is not False:
        json_data = []

        for subdomain in database.get_subdomains():

            report = {
                "hostname": str(subdomain),
                "resolvable": subdomain.resolvable,
                "resolutions": subdomain.resolutions,
                "http": subdomain.http_banner,
            }

            json_data.append(report)

        with open(arguments.output_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(json_data, indent=4))

    end_time = time.time()

    Logger.success(f"Finished in {round(end_time - start_time, 2)} seconds.")
