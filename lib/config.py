from . import __version__

# user agent to use
USER_AGENT = "subdah/%s" % __version__

SUBDOMAIN_REGEX = r"[a-zA-Z0-9-]+"

BASE_REGEX = SUBDOMAIN_REGEX + r"\.%s"

# colors to use for logging (see https://rich.readthedocs.io/en/stable/appendix/colors.html)
INFO_COLOR = "bold cyan"

SUCCESS_COLOR = "bold green"

ERROR_COLOR = "bold red"

WARN_COLOR = "bold yellow"

DEBUG_COLOR = "bold blue"

