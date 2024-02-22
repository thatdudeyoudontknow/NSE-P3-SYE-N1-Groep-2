from scapy.all import srp, Ether, ARP

def scan_live_ips(target_ip):
    # Maak een ARP-pakket om uit te zenden
    arp = ARP(pdst=target_ip)
    # Maak een Ethernet-frame
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Combineer het Ethernet-frame en het ARP-pakket
    packet = ether / arp
    # Verzend het pakket en ontvang antwoorden
    result = srp(packet, timeout=5, verbose=0)[0]
    # Lijst om live IP-adressen op te slaan
    live_ips = []
    # Loop door de ontvangen antwoorden
    for sent, received in result:
        # Voeg het IP-adres toe aan de lijst met live IPs
        live_ips.append(received.psrc)
        
    return live_ips

# Test de functie met het doel-IP-adres en subnet
target_ip = "192.168.178.0/24"
live_ips = scan_live_ips(target_ip)

# Toon de live IP-adressen
print("Live IP-adressen:")
for ip in live_ips:
    print(ip)
