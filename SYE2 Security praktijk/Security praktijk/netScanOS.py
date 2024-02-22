import nmap

def scan_ip(ip_address):
    scanner = nmap.PortScanner()
    scanner.scan(ip_address, arguments='-O')

    if scanner[ip_address]['osmatch']:
        os_type = scanner[ip_address]['osmatch'][0]['name']
        return os_type
    else:
        return "Unknown"

def main():
    ip_addresses = ['192.168.178.1', '192.168.178.90']  # Voeg hier je lijst met IP-adressen toe

    for ip in ip_addresses:
        os_type = scan_ip(ip)
        print(f"IP-adres: {ip}, Besturingssysteem: {os_type}")

if __name__ == "__main__":
    main()
