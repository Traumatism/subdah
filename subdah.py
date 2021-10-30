import sys

from rich.status import Status

from lib.arguments import arguments
from lib.logger import Logger

from lib import __version__, database

from modules.hackertarget import Hackertarget
from modules.alienvault import AlienVault
from modules.fullhunt import FullHunt
from modules.crtsh import CRTSh
from modules.threatminer import ThreatMiner

modules = (Hackertarget, CRTSh, AlienVault, FullHunt, ThreatMiner)

if __name__ == '__main__':
    Logger.console.print(r"""[bold yellow]
              _     _     _   
      ___ _ _| |_ _| |___| |_ 
     |_ -| | | . | . | .'|   |
     |___|___|___|___|__,|_|_| [cyan](v%s)[/cyan][bold yellow]

 [white]github.com/traumatism [green]|[/green] @toastakerman[/white]

    """ % __version__)

    target_domain = arguments.domain.lower()

    Logger.info("Starting...")

    with Status(
        f"Running modules... (0/{len(modules)})", console=Logger.console, spinner="moon"
    ) as status:

        for i, module in enumerate(module(target_domain) for module in modules):

            status.update(f"Running modules... ({i}/{len(modules)})", spinner="moon")

            Logger.debug(f"Running module: {module.__class__.__name__}")

            try:
                module.run()
            except Exception as exc:
                Logger.warning(f"Error running module: {module.__class__.__name__}: {exc}")

    results = database.get_subdomains()

    if not results:
        Logger.error("No results found")
        sys.exit(1)

    Logger.success(f"Found {len(results)} results!")

    Logger.info("Resolving subdomains...")

    for subdomain in results:
        if subdomain.resolvable is False:
            continue

        for address in [x.address for x in subdomain.resolve()]:
            database.update_subdomain(subdomain, address)

    results = {}

    for subdomain in database.get_subdomains():
        if subdomain.resolvable is False:
            results[str(subdomain)] = "[red]n/a[/red]"
            continue

        results[str(subdomain)] = ", ".join(subdomain.resolutions)

    Logger.display_dict(results)

    Logger.success("Finished")
