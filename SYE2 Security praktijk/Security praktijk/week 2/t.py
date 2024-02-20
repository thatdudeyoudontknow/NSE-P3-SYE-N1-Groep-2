import psutil

def get_available_network_adapters():
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    available_networks = []
    for interface, addr_list in addrs.items():
        # Skip adapters with Automatic Private IP Addressing (APIPA)
        if any(getattr(addr, 'address').startswith("169.254") for addr in addr_list):
            continue
        # Check if the interface is up and running
        elif interface in stats and getattr(stats[interface], "isup"):
            available_networks.append(interface)

    return available_networks

if __name__ == "__main__":
    network_adapters = get_available_network_adapters()
    print("Available network adapters:")
    for adapter in network_adapters:
        print(adapter)
