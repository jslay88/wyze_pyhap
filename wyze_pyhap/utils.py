import logging
from typing import Optional, Union

import psutil


logger = logging.getLogger(__name__)


def f_to_c(value: Union[int, float]) -> float:
    return (value - 32) * (5 / 9)


def discover_interface_address(name: str) -> Optional[str]:
    if name is None:
        return None
    logger.info(f"Discovering Interface Address for {name}...")
    interfaces = psutil.net_if_addrs()
    if name not in interfaces:
        logger.warning(
            f"Interface {name} was not found. Binding to default interface. "
            f"May have unexpected results."
        )
        return None
    for address in interfaces[name]:
        if address.family.value == 2:
            logger.info(f"Discovered address {address.address} for Interface {name}.")
            return address.address
    logger.warning(
        f"No IPv4 Addresses found for Interface {name}. Binding to default interface. "
        f"May have unexpected results."
    )
    return None
