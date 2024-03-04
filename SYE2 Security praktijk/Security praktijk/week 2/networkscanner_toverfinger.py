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
from scapy.all import srp, ARP,Ether

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


<<<<<<< Updated upstream
=======
def scan_port(host, port, open_ports):
    """
    Scans a specific port on a host. If the port is open, it adds the port and
    the service running on it to the open_ports list.
    Parameters:
    host (str): The host to scan.
    port (int): The port to scan.
    open_ports (list): A list to store the open ports and their services.
    Returns:
    None
    """
    try:
        # Maak een TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Stel de time-out in op 1 seconde
        # Probeert verbinding te maken met het opgegeven adres en poort
        result = s.connect_ex((host, port))
        s.close()  # Sluit de socket
        # Als de poort open is (0 betekent succesvolle verbinding)
        if result == 0:
            nm = nmap.PortScanner()
            nm.scan(host, str(port))
            service = nm[host]['tcp'][port]['name']
            # Voeg de open poort toe aan de lijst met open poorten
            open_ports.append((port, service))
    except socket.error as e:  # Vang eventuele fouten op
        print(f"Fout bij het scannen van poort {port}: {e}")  # Druk de fout af


def scan_ports():
    """
    Scans a range of ports on a list of hosts.
    The hosts are read from a file named 'live_hosts.txt'.
    For each host, it creates a new thread for each port to be scanned.
    It then waits for all threads to complete.
    After all ports have been scanned,
    it prints the host and any open ports found.

    Parameters:
    None

    Returns:
    None
    """

    global live_hosts_file_global
    live_hosts = open("live_hosts.txt", "r", encoding='utf-8')
    #  Lijst van IP-adressen om te scannen
    #  gets all the live hosts from live_hosts_file
    #  and stores them in a list
    target_hosts = [host.split()[1] for host in live_hosts]
    min_port = 1  # Minimale poort
    max_port = 65535  # Maximale poort

    print(f"Scannen van poorten {min_port} "
          f"t/m {max_port} op de volgende IP-adressen: {target_hosts}")

    # Loop over alle IP-adressen en scan de poorten
    for target_host in target_hosts:
        open_ports = []  # Lijst om de open poorten op te slaan

        # Multithreading: maak een thread voor elke poort en start deze
        threads = []
        for port in range(min_port, max_port + 1):
            #  Maak een thread voor het scannen van de poort
            thread = threading.Thread(target=scan_port, args=(
                target_host, port, open_ports))
            # Voeg de thread toe aan de lijst met threads
            threads.append(thread)
            thread.start()  # Start de thread

        # Wacht tot alle threads zijn voltooid
        for thread in threads:
            thread.join()  # Wacht op de voltooiing van elke thread

        open_ports_str = ", ".join([f"{port} ({service})"
                                    for port, service in open_ports])
        print(f"IP: {target_host}, OpenPoort(en): {open_ports_str}")
        live_hosts_file_global.close()


def get_hostname(ip_address):
    """
    Resolves the hostname from the given IP address.

    Parameters:
    ip_address (str): The IP address to resolve.

    Returns:
    str: The hostname if it can be resolved,
    otherwise returns "Unable to resolve hostname".
    """
    try:
        # Resolve the IP address to hostname
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        return "Unable to resolve hostname"


def scan_live_ips(cidr, network_interface):
    """
    Scans a range of IP addresses in a given CIDR block
    and identifies live hosts.

    This function sends an ARP request to each IP address in the CIDR
    block and checks for a response.
    If a response is received, the IP address is considered live and
    additional information is gathered
    such as the MAC address, OS type, and hostname. The results are written
    to a file and also returned as a list of tuples.

    Args:
        cidr (str): The CIDR block to scan. For example, '192.168.1.0/24'.
        network_interface (str):
        The network interface to use for sending packets.

    Returns:
        list: A list of tuples where each tuple
        contains the IP and MAC address of a live host.

    Side Effects:
        Writes the results to 'live_hosts.txt' and 'unreachable_hosts.txt'
    """
    # Verkrijg basis-IP-adres en aantal hostbits van CIDR-notatie
    ip_network = ipaddress.ip_network(cidr, strict=False)
    base_ip = ip_network.network_address
    subnet_mask = ip_network.netmask
    host_bits = subnet_mask.max_prefixlen - ip_network.prefixlen

    # Bepaal het aantal IP-adressen in het subnetwerk
    num_addresses = 2 ** host_bits

    # Define the file objects
    global live_hosts_file_global, unreachable_hosts_file
    live_hosts_file_global = open("live_hosts.txt", "a", encoding='utf-8')
    unreachable_hosts_file = open("unreachable_hosts.txt",
                                  "a", encoding='utf-8')

    # Ping each IP address in the subnet
    live_hosts = []
    for i in tqdm(range(num_addresses)):
        # if i reaches 50, stop the loop
        if i == 53:
            break
        ip = str(base_ip + i)
        print(f"Scanning {ip}")
        # Create an ARP request packet
        arp = ARP(pdst=ip)
        # Create an Ethernet frame
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        # Combine the Ethernet frame and the ARP packet
        packet = ether / arp
        print(f"Packet: {packet}")
        # Send the packet and receive responses
        print(network_interface)
        result = srp(packet, timeout=3, verbose=0, iface=network_interface)[0]
        print(f"Result: {result}")
        # If we received at least one response, the IP is live
        if len(result) > 0:
            mac_address = get_mac_address(ip)
            #  call scan_ip function
            os_type = scan_ip(ip)
            hostname = get_hostname(ip)
            live_hosts_file_global.write(f"IP: {ip} "
                                         f"MAC: {mac_address} "
                                         f"OS: {os_type} "
                                         f"Hostname: {hostname} "
                                         f"is live.\n")
            print(f"\nHit on\n"
                  f"IP: {ip} \n"
                  f"MAC: {mac_address} \n"
                  f"OS: {os_type} \n"
                  f"Hostname: {hostname} \n")
            live_hosts.append((ip, mac_address))
        else:
            unreachable_hosts_file.write(f"{ip} is not reachable.\n")

    # Close the file objects
    live_hosts_file_global.close()
    unreachable_hosts_file.close()
    return live_hosts


>>>>>>> Stashed changes
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

    # Define the file objects
    live_hosts_file = open("live_hosts.txt", "w")
    unreachable_hosts_file = open("unreachable_hosts.txt", "w")

    # Ping each IP address in the subnet
    live_hosts = []
    for i in range(num_addresses):
        ip = base_ip + i
        response = ping(str(ip), count=1)
        if response.success():
            mac_address = get_mac_address(str(ip))
            live_hosts_file.write(f"IP: {ip} MAC: {mac_address} is live.\n")
            print(f"IP: {ip} MAC: {mac_address} is live.")
            live_hosts.append((ip, mac_address))


        else:
            print(f"{ip} is not reachable.")
            unreachable_hosts_file.write(f"{ip} is not reachable.\n")

    # Close the file objects
    live_hosts_file.close()
    unreachable_hosts_file.close()
    return live_hosts


def get_mac_address(ip_address):
    arp = ARP(pdst=ip_address)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=False)[0]
    return result[0][1].hwsrc if result else None


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
        print("Getting IP range...")
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
