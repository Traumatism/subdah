import sys

from rich.status import Status

from lib.arguments import arguments
from lib.logger import Logger

from lib import __version__, database

from modules.hackertarget import Hackertarget
from modules.alienvault import AlienVault
from modules.fullhunt import FullHunt
from modules.crtsh import CRTSh


modules = (Hackertarget, CRTSh, AlienVault, FullHunt)


if __name__ == '__main__':
    print("""

👀 Subdah v%s
by @toastakerman

    """ % __version__)

    target_domain = arguments.domain.lower()


    with Status("running modules... (0/%d)" % len(modules), console=Logger.console, spinner="moon") as status:

        for i, module in enumerate(module(target_domain) for module in modules):

            status.update(f"Running modules... ({i}/{len(modules)})", spinner="moon")

            Logger.debug(f"Running module: {module.__class__.__name__}")

            try:
                module.run()
            except:
                Logger.warning("Error running module: %s" % module.__class__.__name__)

    results = database.get_subdomains()

    if not results:
        Logger.error("No results found")
        sys.exit(1)

    for subdomain in results:
        if subdomain.resolvable is False:
            continue

        for address in [x.address for x in subdomain.resolve()]:
            database.update_subdomain(subdomain, address)

    results = {}

    for subdomain in database.get_subdomains():
        if subdomain.resolvable is False:
            results[str(subdomain)] = "n/a"
            continue
        
        results[str(subdomain)] = ", ".join(subdomain.resolutions)

    Logger.display_dict(results)

    Logger.success("Finished")