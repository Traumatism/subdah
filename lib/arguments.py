import argparse


parser = argparse.ArgumentParser(
    usage="%(prog)s <arguments>",
    description="Subdah - a cool subdomains scanner."
)

global_flags = parser.add_argument_group("Global flags")

output_flags = parser.add_argument_group("Output flags")

misc_flags = parser.add_argument_group("Miscellanious flags")

global_flags.add_argument(
    "-d",
    help="Domain to scan.",
    required=True,
    type=str,
    dest="domain",
    metavar="<domain #1,domain #2…>"
)

global_flags.add_argument(
    "-n", "--disable-resolutions",
    help="Don't resolve found subdomains.",
    action="store_true",
    dest="dont_resolve",
    default=False
)

output_flags.add_argument(
    "-o", "--output",
    help="Output file.",
    required=False,
    dest="output_file",
    default=False,
    metavar="<file path>"
)

misc_flags.add_argument(
    "--debug",
    help="Debug mode.",
    action="store_true",
    dest="debug",
    default=False
)

arguments = parser.parse_args()
