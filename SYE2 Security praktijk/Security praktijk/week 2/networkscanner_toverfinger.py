"""
Module to retrieve network adapters and IP addresses on a Windows system.
pylint score: 10/10
#pylint .\networkscanner_toverfinger.py
pycodesyle score: 10/10
#pycodestyle --show-source --show-pep8 .\networkscanner_toverfinger.py
"""
import os
import psutil

APIPA_PREFIX = "169.254"


def get_network_adapters():
    """
    Retrieves the available network adapters on the system.

    Returns:
        list: A list of available network adapters.
    """
    network_addresses = psutil.net_if_addrs()
    network_stats = psutil.net_if_stats()

    available_networks = []
    for interface, addr_list in network_addresses.items():
        # Skip adapters with Automatic Private IP Addressing (APIPA)
        if any(
            getattr(addr, 'address').startswith(APIPA_PREFIX)
            for addr in addr_list
        ):
            continue
        # Check if the interface is up and running
        if interface in network_stats and getattr(
                network_stats[interface], "isup"):
            available_networks.append(interface)

    return available_networks


def get_ip_from_ipconfig(adapter_name):
    """
    Retrieves the IP address associated with the specified network adapter.

    Parameters:
    adapter_name (str): The name of the network adapter.

    Returns:
    str: The IP address associated with the network adapter,
    or None if not found.
    """
    addrs = psutil.net_if_addrs()
    for interface, addr_list in addrs.items():
        if interface == adapter_name:
            for addr in addr_list:
                if addr.family == psutil.AF_LINK:
                    continue
                return addr.address
    return None


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
            print(f"{i}. {adapter}")
        selected_adapter_index = int(input("Select a network adapter: ")) - 1
        clear_terminal()
        selected_adapter = adapters[selected_adapter_index]
        ip_address = get_ip_from_ipconfig(selected_adapter)
        if ip_address:
            print(f"IP address of {selected_adapter}: {ip_address}")
        else:
            print(f"No IP found for {selected_adapter}")
    else:
        clear_terminal()
        # Handle manual IP range entry
        ip_range = input("Enter the IP range (e.g., 192.168.1.0/24): ")
        print(f"You entered: {ip_range}")


if __name__ == "__main__":
    main()
