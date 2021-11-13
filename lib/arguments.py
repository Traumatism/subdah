import argparse

parser = argparse.ArgumentParser(
    usage="%(prog)s <arguments>",
    description="Subdah - a cool subdomains scanner."
)

global_flags = parser.add_argument_group("Global flags")

output_flags = parser.add_argument_group("Output flags")

http_flags = parser.add_argument_group("HTTP flags")

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
    "-t", "--threads",
    help="Max threads to use.",
    type=int,
    dest="threads",
    default=5,
    metavar="<int value>"
)

output_flags.add_argument(
    "-o", "--output",
    help="Output file.",
    required=False,
    dest="output_file",
    default=False,
    metavar="<file path>"
)

http_flags.add_argument(
    "--timeout",
    help="Timeout to use. (in ms)",
    type=int,
    dest="http_timeout",
    default=1500,
    metavar="<int value>"
)



misc_flags.add_argument(
    "--debug",
    help="Debug mode.",
    action="store_true",
    dest="debug",
    default=False
)

arguments = parser.parse_args()
