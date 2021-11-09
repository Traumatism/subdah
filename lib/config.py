USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"

SUBDOMAIN_REGEX = r"[a-zA-Z0-9-]+"

BASE_REGEX = r"(" + SUBDOMAIN_REGEX + r" +\.%s)"
