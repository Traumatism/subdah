import socket
import threadz

from typing import Iterable


def port_scan(subdomain) -> Iterable[int]:
    """ Scan a subdomain for open ports """
    PORTS = (
        21, 22, 80, 443, 3306,
        8080, 8081, 8181, 27017
    )

    def _port_scan(host: str, port: int) -> bool:
        """ Scan a port on a host """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            try:
                sock.connect((host, port))
                return True
            except socket.timeout:
                return False
            except socket.error:
                return False

    tasks = [
        (
            _port_scan, tuple(),
            {"host": subdomain.subdomain, "port": port}
        )
        for port in PORTS
    ]

    results = threadz.gather(tasks, concurrency=10)

    for idx, state in results.items():
        if state:
            yield tasks[idx][2]["port"]

