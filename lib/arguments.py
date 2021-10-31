import argparse


__parser = argparse.ArgumentParser(
    usage="%(prog)s <arguments>",
    description="Subdah - a cool subdomains scanner."
)

__parser.add_argument(
    "-d", "--domain",
    help="Domain to scan.",
    required=True,
    type=str,
    dest="domain",
    metavar="<domain>"
)

__parser.add_argument(
    "-n", "--disable-resolutions",
    help="Don't resolve found subdomains.",
    action="store_true",
    dest="dont_resolve",
    default=False
)

__parser.add_argument(
    "--debug",
    help="Debug mode.",
    action="store_true",
    dest="debug",
    default=False
)

arguments = __parser.parse_args()
