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
            
        else:
            print(f"No IP found for {selected_adapter}")
    else:
        clear_terminal()
        # Handle manual IP range entry
        ip_range = input("Enter the IP range (e.g., 192.168.1.0/24): ")
        print(f"You entered: {ip_range}")


if __name__ == "__main__":
    main()
