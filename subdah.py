import sys

from rich.status import Status

from lib.common.abc import Module
from lib.arguments import arguments
from lib.logger import Logger

from lib import __version__, database

from modules.hackertarget import Hackertarget
from modules.alienvault import AlienVault
from modules.fullhunt import FullHunt
from modules.crtsh import CRTSh
from modules.threatminer import ThreatMiner
from modules.shodan import Shodan
from modules.threatcrowd import ThreatCrowd
from modules.yahoo import Yahoo
from modules.anubis import Anubis
from modules.securitytrails import SecurityTrails


modules = (
    Hackertarget, CRTSh, AlienVault, FullHunt, 
    ThreatMiner, Shodan, ThreatCrowd, Yahoo,
    Anubis, SecurityTrails
)


if __name__ == '__main__':

    [
        Logger.warning("<%s> is not a subclass of <lib.common.abc.Module> !" % module.__name__)
        for module in modules
        if not issubclass(module, Module)
    ]

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
        f"Running modules... (0/{len(modules)}, found {database.count})", console=Logger.console, spinner="moon"
    ) as status:

        for i, module in enumerate(module(target_domain) for module in modules):
            status.update(f"Running modules... ({i}/{len(modules)}, found {database.count})", spinner="moon")
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

    if arguments.dont_resolve is False:
        Logger.info("Resolving subdomains...")

        for subdomain in results:
            if subdomain.resolvable is False:
                continue
            
            resolutions = subdomain.resolve()
            
            if resolutions is None:
                continue

            for address in resolutions:
                database.update_subdomain(subdomain, address)

        results = {
            str(subdomain): ", ".join(subdomain.resolutions)
            if subdomain.resolutions is not None and subdomain.resolvable is True else "[red]n/a[/red]"
            for subdomain in database.get_subdomains()
        }

        Logger.display_dict(results)
    else:
        for subdomain in results:
            Logger.console.print(f"[green]*[/green] [white]{subdomain}[/white]")

    Logger.success("Finished")
