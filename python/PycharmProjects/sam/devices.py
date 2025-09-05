import subprocess
import platform


def LAN_SCAN():
    if platform.system() == "Windows":
        try:
            CMD_PROMPT_OUTPUT = subprocess.check_output("arp -a", shell=True, text=True)
            lines = CMD_PROMPT_OUTPUT.splitlines()
            ip_addresses = [line.split()[0] for line in lines if "." in line]
            return ip_addresses
        except subprocess.SubprocessError:
            print("KYS NIGGA")
            return []
    else:
        print("You not on windows bruhhhh")


text = input("c:\\>")
if text == "arp":
    lan = LAN_SCAN()
    if lan:
        print("Devices connected to LAN: ")
        for ip in lan:
            print(ip)
