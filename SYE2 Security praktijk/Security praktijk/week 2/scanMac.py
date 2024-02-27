from getmac import get_mac_address

target_ip = "192.168.1.1"
mac_address = get_mac_address(ip=target_ip)
if mac_address:
    print(f"MAC-adres van {target_ip}: {mac_address}")
else:
    print(f"Geen MAC-adres gevonden voor {target_ip}")
