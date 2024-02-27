import socket

def get_hostname(ip_address):
    try:
        # Resolve the IP address to hostname
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        return "Unable to resolve hostname"

def main():
    ip_addresses = ['192.168.1.1', '192.168.1.10','192.168.1.23','192.168.1.30']

    for ip_address in ip_addresses:
        try:
            # Check if the input is a valid IP address
            socket.inet_aton(ip_address)
        except socket.error:
            print(f"Invalid IP address format for {ip_address}.")
            continue

        hostname = get_hostname(ip_address)
        print(f"IP Address: {ip_address} - Hostname: {hostname}")

if __name__ == "__main__":
    main()
