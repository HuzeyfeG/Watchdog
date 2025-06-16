import requests
from argparse import ArgumentParser

parser = ArgumentParser()
parser.usage = "python3 track_ip.py"
parser.parse_args()


class TrackIP:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def track_ip(self):
        return requests.get(f"http://ip-api.com/json/{self.ip_address}").json()
    

if __name__ == "__main__":
    target_ip = input("Enter an IP -> ")
    tracker = TrackIP(target_ip)
    ip_address_info = tracker.track_ip()

    if ip_address_info["status"] == "fail":
        print(ip_address_info["message"])
    else:
        print(f"IP: {ip_address_info['query']}")
        print(f"Country: {ip_address_info['country']}")
        print(f"Region: {ip_address_info['regionName']}")
        print(f"City: {ip_address_info['city']}")
        print(f"ISP: {ip_address_info['isp']}")
        print(f"Organization: {ip_address_info['org']}")
        print(f"Latitude: {ip_address_info['lat']}")
        print(f"Longitude: {ip_address_info['lon']}")
