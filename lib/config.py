from . import __version__

USER_AGENT = "subdah/%s" % __version__

SUBDOMAIN_REGEX = r"[a-zA-Z0-9-]+"

BASE_REGEX = r"(" + SUBDOMAIN_REGEX + r" +\.%s)"
