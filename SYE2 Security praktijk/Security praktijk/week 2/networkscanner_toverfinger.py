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
import threading
import subprocess
import nmap

# Open the file objects
live_hosts_file = open("live_hosts.txt", "a")
unreachable_hosts_file = open("unreachable_hosts.txt", "a")

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


def scan_port(host, port, open_ports):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Maak een TCP socket
        s.settimeout(1)  # Stel de time-out in op 1 seconde
        result = s.connect_ex((host, port))  # Probeert verbinding te maken met het opgegeven adres en poort
        s.close()  # Sluit de socket
        if result == 0:  # Als de poort open is (0 betekent succesvolle verbinding)
            open_ports.append(port)  # Voeg de open poort toe aan de lijst
    except Exception as e:  # Vang eventuele fouten op
        print(f"Fout bij het scannen van poort {port}: {e}")  # Druk de fout af


def scan_ports():
    # Lijst van IP-adressen om te scannen
    global live_hosts_file
    #gets all the live hosts from live_hosts_file and stores them in a list
    with open('live_hosts.txt', 'r') as live_hosts_file:
        live_hosts = live_hosts_file.readlines()
    target_hosts = [host.split()[1] for host in live_hosts]
    
    min_port = 1  # Minimale poort
    max_port = 65535  # Maximale poort

    print(f"Scannen van poorten {min_port} t/m {max_port} op de volgende IP-adressen: {target_hosts}")

    # Loop over alle IP-adressen en scan de poorten
    for target_host in target_hosts:
        open_ports = []  # Lijst om de open poorten op te slaan

        # Multithreading: maak een thread voor elke poort en start deze
        threads = []
        for port in range(min_port, max_port + 1):
            thread = threading.Thread(target=scan_port, args=(target_host, port, open_ports))  # Maak een thread voor het scannen van de poort
            threads.append(thread)  # Voeg de thread toe aan de lijst met threads
            thread.start()  # Start de thread

        # Wacht tot alle threads zijn voltooid
        for thread in threads:
            thread.join()  # Wacht op de voltooiing van elke thread

        # Afdrukken van de lijst met open poorten voor dit IP-adres
        print(f"IP: {target_host}, OpenPoort(en): {open_ports}")


        # Afdrukken van de lijst met open poorten voor dit IP-adres
        print(f"IP: {target_host}, OpenPoort(en): {open_ports}")


# def arp_a(ip_address):
#     try:
#         # Voer de 'arp -a' opdracht uit en decodeer de uitvoer naar een leesbare string
#         arp_output = subprocess.check_output(['arp', '-a', ip_address]).decode('utf-8')
#         return arp_output  # Retourneer de uitvoer van 'arp -a'
#     except subprocess.CalledProcessError:
#         return None  # Retourneer None als er een fout optreedt tijdens het uitvoeren van de opdracht

# def find_MAC():
#     # Lijst van IP-adressen om te scannen
#     global live_hosts_file
#     #gets all the live hosts from live_hosts_file and stores them in a list
#     with open('live_hosts.txt', 'r') as live_hosts_file:
#         live_hosts = live_hosts_file.readlines()
#     print (f"Scanning MAC address for {live_hosts}")
#     target_hosts = [host.split()[1] for host in live_hosts]
#     print (f"Scanning MAC address for {target_hosts}")
#     for ip_address in target_hosts:
#         print (f"Scanning MAC address for {ip_address}")
#         arp_result = arp_a(ip_address)  # Voer 'arp -a' uit voor het huidige IP-adres
#         if arp_result:
#             print(f"ARP result for {ip_address}:")
#             print(arp_result)  # Print de ARP-resultaten als er resultaten zijn
#         else:
#             print(f"No ARP result found for {ip_address}")  # Print een melding als er geen resultaten zijn gevonden




def scan_live_ips(target_ip):
    # Maak een ARP-pakket om uit te zenden
    arp = ARP(pdst=target_ip)
    # Maak een Ethernet-frame
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Combineer het Ethernet-frame en het ARP-pakket
    packet = ether / arp
    # Verzend het pakket en ontvang antwoorden
    result = srp(packet, timeout=3, verbose=0)[0]
    # Lijst om live IP-adressen op te slaan
    live_ips = []
    # Loop door de ontvangen antwoorden
    for sent, received in result:
        # Voeg het IP-adres toe aan de lijst met live IPs
        live_ips.append(received.psrc)
        print(received.psrc)

    return live_ips


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
    global live_hosts_file, unreachable_hosts_file

    # Ping each IP address in the subnet
    live_hosts = []
    for i in range(num_addresses):
        # if i reaches 50, stop the loop
        if i == 50:
            break
        ip = base_ip + i
        response = ping(str(ip), count=1)
        if response.success():
            mac_address = get_mac_address(str(ip))
            #call scan_ip function 
            os_type = scan_ip(str(ip))
            live_hosts_file.write(f"IP: {ip} MAC: {mac_address} OS: {os_type}  is live.\n")
            print(f"IP: {ip} MAC: {mac_address} OS: {os_type}  is live.")
            live_hosts.append((ip, mac_address))


        else:
            print(f"{ip} is not reachable.")
            unreachable_hosts_file.write(f"{ip} is not reachable.\n")

    # Close the file objects
    live_hosts_file.close()
    unreachable_hosts_file.close()
    return live_hosts

def scan_ip(ip_address):
    scanner = nmap.PortScanner()
    scanner.scan(ip_address, arguments='-O')

    if scanner[ip_address]['osmatch']:
        os_type = scanner[ip_address]['osmatch'][0]['name']
        return os_type
    else:
        return "Unknown"


def get_mac_address(ip_address):

    try:
        # Voer de 'arp -a' opdracht uit en decodeer de uitvoer naar een leesbare string
        arp_output = subprocess.check_output(['arp', '-a', ip_address]).decode('utf-8')
        #return the output of 'arp -a' but only the mac address

        return arp_output.split()[10]
    except subprocess.CalledProcessError:
        print (f"No MAC address found for {ip_address}")
        return None




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
    return live_hosts


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
    clear_terminal()
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
        print("1. Get IP range from ipconfig (fast but less accurate)")
        print("2. Get IP range from network adapters (slow but accurate)")
        choice = input("Enter your choice (1 or 2): ")
        print(f"IP address of {ip_address}")
        print(ip_address)
        
        if choice== '2' and ip_address:
            abe(ip_address)
            port_scan = input("Do you want to scan the live hosts for open ports? (y/n): ")
            if port_scan == 'y':
                scan_ports()
        if choice == '1':
            scan_live_ips(ip_address)
            port_scan = input("Do you want to scan the live hosts for open ports? (y/n): ")
            if port_scan == 'y':
                scan_ports()
            else:
                #exit the program
                exit()
        else:
            print(f"No IP found for {selected_adapter}")
    else:
        clear_terminal()
        # Handle manual IP range entry
        ip_range = input("Enter the IP range (e.g., 192.168.1.0/24): ")
        print(f"You entered: {ip_range}")


if __name__ == "__main__":
    main()
