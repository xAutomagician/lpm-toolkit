import ipaddress
from typing import List

from app.models.subnet import InvalidCIDRError, SubnetInfo


def subnet_info(cidr: str) -> SubnetInfo:
    """
    Compute subnet details for a given CIDR string, e.g. '192.168.1.0/24'.
    Raises InvalidCIDRError on bad input.
    """
    try:
        network = ipaddress.ip_network(cidr, strict=False)
    except ValueError as exc:
        raise InvalidCIDRError(str(exc)) from exc

    # NOTE: deliberately avoid network.hosts() here — it enumerates every
    # address, which is fine for a /24 but never finishes for a /64 (2**64
    # addresses). Everything below is O(1) arithmetic instead.
    num_addresses = network.num_addresses
    network_addr_int = int(network.network_address)
    last_addr_int = int(network.broadcast_address)  # O(1): highest addr in range

    if network.version == 4 and network.prefixlen < 31:
        has_broadcast = True
        first_usable_int = network_addr_int + 1
        last_usable_int = last_addr_int - 1
        num_usable = num_addresses - 2
    else:
        # /31 and /32 (RFC 3021) have no reserved broadcast; IPv6 has no
        # broadcast concept at all — every address in the range is usable.
        has_broadcast = False
        first_usable_int = network_addr_int
        last_usable_int = last_addr_int
        num_usable = num_addresses

    ip_cls = ipaddress.IPv4Address if network.version == 4 else ipaddress.IPv6Address

    return SubnetInfo(
        cidr=str(network),
        network_address=str(network.network_address),
        broadcast_address=str(network.broadcast_address) if has_broadcast else None,
        netmask=str(network.netmask),
        wildcard_mask=str(network.hostmask),
        num_addresses=num_addresses,
        num_usable_hosts=num_usable,
        first_usable_host=str(ip_cls(first_usable_int)),
        last_usable_host=str(ip_cls(last_usable_int)),
        is_private=network.is_private,
        version=network.version,
    )


def range_to_cidrs(start: str, end: str) -> List[str]:
    """
    Convert an inclusive IPv4 address range [start, end] into the minimal
    list of CIDR blocks that exactly covers it.

    Ranges from real-world sources like iptoasn.com are the result of
    merging adjacent BGP-announced prefixes, so they are frequently *not*
    aligned to a power-of-two boundary — a single range can require several
    CIDR blocks to represent exactly (e.g. 3 addresses -> a /31 + a /32).
    """
    start_ip = ipaddress.IPv4Address(start)
    end_ip = ipaddress.IPv4Address(end)
    return [str(net) for net in ipaddress.summarize_address_range(start_ip, end_ip)]
