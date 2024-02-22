import socket  # Importeer de socketmodule voor netwerkcommunicatie
import threading  # Importeer de threadingmodule voor multithreading
import nmap  # Importeer de nmap-module voor service-identificatie

def scan_port(host, port, open_ports):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Maak een TCP socket
        s.settimeout(1)  # Stel de time-out in op 1 seconde
        result = s.connect_ex((host, port))  # Probeert verbinding te maken met het opgegeven adres en poort
        s.close()  # Sluit de socket
        if result == 0:  # Als de poort open is (0 betekent succesvolle verbinding)
            open_ports.append(port)  # Voeg de open poort toe aan de lijst
            nm = nmap.PortScanner()  # Maak een nmap PortScanner-object
            nm.scan(host, str(port))  # Scan de poort om de service te identificeren
            service = nm[host]['tcp'][port]['name']  # Haal de service op die bij de poort hoort
            print(f"Poort {port} op IP {host} is open. Service: {service}")
    except Exception as e:  # Vang eventuele fouten op
        print(f"Fout bij het scannen van poort {port}: {e}")  # Druk de fout af

def main():
    # Lijst van IP-adressen om te scannen
    target_hosts = ["192.168.178.1", "192.168.178.90"]  # Voeg hier je lijst met IP-adressen toe

    min_port = 1  # Minimale poort
    max_port = 1024  # Maximale poort

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

if __name__ == "__main__":
    main()


