"""
Module to retrieve network adapters and IP addresses on a Windows system.
pylint score: 10/10
#pylint .\networkscanner_toverfinger.py
pycodesyle score: 10/10
#pycodestyle --show-source --show-pep8 .\networkscanner_toverfinger.py
"""
import os
import ipaddress
import socket
import psutil
from pythonping import ping


# Automatic Private IP Addressing (APIPA) prefix
APIPA_PREFIX = "169.254"


def get_network_adapters():
    """
    Returns a list of available network adapters that are up and running
    and do not have an Automatic Private IP Addressing (APIPA).
    """
    network_addresses = psutil.net_if_addrs()
    network_stats = psutil.net_if_stats()

    available_networks = []
    for interface, addr_list in network_addresses.items():
        # Skip adapters with Automatic Private IP Addressing (APIPA)
        if any(addr.address.startswith("169.254") for addr in addr_list):
            continue
        # Check if the interface is up and running
        if interface in network_stats and network_stats[interface].isup:
            for addr in addr_list:
                if addr.family == socket.AF_INET:
                    netmask = addr.netmask
                    ip_with_netmask = (
                        f"{addr.address}/"
                        f"{ipaddress.IPv4Network((0, netmask)).prefixlen}"
                    )
                    available_networks.append((interface, ip_with_netmask))

    return available_networks


def clear_terminal():
    """
    Clears the terminal screen.
    """
    os.system('cls')


def ping_cidr_network(cidr):
    """
    Ping all IP addresses in a given CIDR network and return a list
    of live hosts.
    Args:
        cidr (str): The CIDR notation representing the network.
    Returns:
        list: A list of live host IP addresses.
    """
    # Verkrijg basis-IP-adres en aantal hostbits van CIDR-notatie
    ip_network = ipaddress.ip_network(cidr, strict=False)
    base_ip = ip_network.network_address
    subnet_mask = ip_network.netmask
    host_bits = subnet_mask.max_prefixlen - ip_network.prefixlen

    # Bepaal het aantal IP-adressen in het subnetwerk
    num_addresses = 2 ** host_bits

    # Ping elk IP-adres in het subnetwerk
    live_hosts = []
    for i in range(num_addresses):
        ip = base_ip + i
        response = ping(str(ip), count=1)
        if response.success():
            print(f"{ip} is live.")
            live_hosts.append(ip)
        else:
            print(f"{ip} is not reachable.")
    return live_hosts


# Voorbeeldgebruik:
def abe(ip_address):
    """
    Function to scan a network for live hosts using ICMP ping.
    Args:
        ip_address (str): The IP address or CIDR notation of the network
        to scan.
    Returns:
        None
    """
    cidr = ip_address
    live_hosts = ping_cidr_network(cidr)
    print("Live hosts:")
    for host in live_hosts:
        print(host)


def main():
    """
    This function is the entry point of the network scanner program.
    It provides options to either enter the IP range manually or
    get the IP range from ipconfig.
    """
    clear_terminal()
    print("1. Enter IP range manually")
    print("2. Get IP range from ipconfig")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '2':
        clear_terminal()
        print("Getting IP range from ipconfig...")
        adapters = get_network_adapters()
        for i, adapter in enumerate(adapters, start=1):
            print(f"{i}. {adapter[0]}")
        selected_adapter_index = int(input("Select a network adapter: ")) - 1
        clear_terminal()
        selected_adapter = adapters[selected_adapter_index]
        ip_address = selected_adapter[1]
        if ip_address:
            print(f"IP address of {ip_address}")
            print(ip_address)
            abe(ip_address)
        else:
            print(f"No IP found for {selected_adapter}")
    else:
        clear_terminal()
        # Handle manual IP range entry
        ip_range = input("Enter the IP range (e.g., 192.168.1.0/24): ")
        print(f"You entered: {ip_range}")


if __name__ == "__main__":
    main()
