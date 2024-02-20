import ipaddress
from pythonping import ping
from scapy.all import srp, Ether, ARP

def ping_cidr_network(cidr):
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
            mac_address = get_mac_address(str(ip))
            print(f"IP: {ip} MAC: {mac_address} is live.")
            live_hosts.append((ip, mac_address))
        else:
            print(f"{ip} is not reachable.")


    return live_hosts

def get_mac_address(ip_address):
    arp = ARP(pdst=ip_address)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=False)[0]
    return result[0][1].hwsrc if result else None

# Voorbeeldgebruik:
cidr = "192.168.178.80/28"
live_hosts = ping_cidr_network(cidr)
print("Live hosts:")
for host, mac_address in live_hosts:
    print(f"IP: {host} MAC: {mac_address}")