from ipaddress import IPv4Address, ip_address
from dataclasses import dataclass, field


@dataclass(order=True)
class IPAddress:
    _ip: IPv4Address = field(init=False, repr=False)
    ip: str = field(compare=False)
    mask: int

    def __post_init__(self):
        self._ip = ip_address(self.ip)


ip1 = IPAddress('10.10.1.1', 24)
ip2 = IPAddress('10.2.1.1', 24)

ip_list = [ip1, ip2]

print(sorted(ip_list))
