import socket
import threading
import nmap

def scan_port(host, port, open_ports):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((host, port))
        s.close()
        if result == 0:
            nm = nmap.PortScanner()
            nm.scan(host, str(port))
            service = nm[host]['tcp'][port]['name']
            open_ports.append((port, service))
    except Exception as e:
        print(f"Fout bij het scannen van poort {port}: {e}")

def main():
    target_hosts = ['192.168.1.1', '192.168.1.10', '192.168.1.23', '192.168.1.30']
    min_port = 1
    max_port = 65534

    print(f"Scannen van poorten {min_port} t/m {max_port} op de volgende IP-adressen: {target_hosts}")

    for target_host in target_hosts:
        open_ports = []

        threads = []
        for port in range(min_port, max_port + 1):
            thread = threading.Thread(target=scan_port, args=(target_host, port, open_ports))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        open_ports_str = ", ".join([f"{port} ({service})" for port, service in open_ports])
        print(f"IP: {target_host}, OpenPoort(en): {open_ports_str}")

if __name__ == "__main__":
    main()
