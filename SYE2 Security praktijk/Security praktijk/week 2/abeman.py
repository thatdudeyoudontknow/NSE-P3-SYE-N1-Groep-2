from scapy.all import srp, Ether, ARP, IP
import ipaddress

# Definieer het doel-IP-adres en het subnet
target_ip = "192.168.178.0/24"

# Convert the target IP to a network
network = ipaddress.ip_network(target_ip, strict=False)

# Get all hosts in the network
hosts = list(network.hosts())

# Lijst om live IP-adressen op te slaan
live_ips = []

# Loop through each chunk of 10 hosts
for i in range(0, len(hosts), 10):
    # Get the current chunk of hosts
    chunk = hosts[i:i+10]

    # Loop through each host in the chunk
    for host in chunk:
        # Maak een ARP-pakket om uit te zenden
        arp = ARP(pdst=str(host))

        # Maak een Ethernet-frame
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")

        # Combineer het Ethernet-frame en het ARP-pakket
        packet = ether / arp

        # Verzend het pakket en ontvang antwoorden
        result = srp(packet, timeout=5, verbose=0)[0]

        # Loop door de ontvangen antwoorden
        for sent, received in result:
            # Voeg het IP-adres toe aan de lijst met live IPs
            live_ips.append(received.psrc)

# Toon de live IP-adressen
print("Live IP-adressen:")
for ip in live_ips:
    print(ip)