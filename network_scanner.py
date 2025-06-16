import scapy.all as scapy
from netaddr import EUI, NotRegisteredError
import requests
import socket


class NetworkScanner:
    def __init__(self):
        self.device_list = []
        self.network_range = ""
    
    def get_vendor(self, mac_address):
        try:
            mac_obj = EUI(mac_address)
            mac_vendor = mac_obj.oui.registration().org
            return mac_vendor
        except NotRegisteredError:
            try:
                response = requests.get(f"https://api.macvendors.com/{mac_address}")
                if response.status_code == 200:
                    return response.text
            except Exception:
                pass
        return "Unknown Vendor"
    
    def get_hostname(self, ip_address):
        try:
            hostname = socket.gethostbyaddr(ip_address)
            return hostname[0]
        except socket.herror:
            return "Unknown Host"

    def scan_network(self):
        self.device_list = []
        arp_requests = scapy.ARP(pdst=self.network_range)
        broadcast_package = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        packages_all = broadcast_package / arp_requests
        (answered, _) = scapy.srp(packages_all, timeout=1, verbose=False)
        for _, received in answered:
            ip_address = received.psrc
            mac_address = received.hwsrc.upper()
            mac_vendor = self.get_vendor(mac_address)
            hostname = self.get_hostname(ip_address)
            self.device_list.append([received.psrc, (received.hwsrc).upper(), mac_vendor, hostname])


if __name__ == "__main__":
    network_scanner = NetworkScanner()
    # network_scanner.network_range = input("\nPlease enter the network range (ex: 192.168.1.0/24) -> ")
    network_scanner.network_range = "192.168.1.0/24"
    network_scanner.scan_network()
    from tabulate import tabulate
    table_headers = ["id", "IP", "MAC", "Vendor", "Hostname"]
    print(f"\n{tabulate(tabular_data=network_scanner.device_list, headers=table_headers, tablefmt="simple", showindex="always")}")
