import subprocess

def arp_a(ip_address):
    try:
        # Voer de 'arp -a' opdracht uit en decodeer de uitvoer naar een leesbare string
        arp_output = subprocess.check_output(['arp', '-a', ip_address]).decode('utf-8')
        return arp_output  # Retourneer de uitvoer van 'arp -a'
    except subprocess.CalledProcessError:
        return None  # Retourneer None als er een fout optreedt tijdens het uitvoeren van de opdracht

def main():
    ip_addresses = ['192.168.1.1', '192.168.1.10','192.168.1.23','192.168.1.30']  # Voorbeeldlijst met IP-adressen

    for ip_address in ip_addresses:
        arp_result = arp_a(ip_address)  # Voer 'arp -a' uit voor het huidige IP-adres
        if arp_result:
            print(f"ARP result for {ip_address}:")
            print(arp_result)  # Print de ARP-resultaten als er resultaten zijn
        else:
            print(f"No ARP result found for {ip_address}")  # Print een melding als er geen resultaten zijn gevonden

if __name__ == "__main__":
    main()  # Roep de hoofdfunctie aan om het script uit te voeren



['192.168.1.1', '192.168.1.10','192.168.1.23','192.168.1.30']