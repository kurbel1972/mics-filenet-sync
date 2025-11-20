import subprocess
import sys
import re

def is_vpn_connected():
    try:
        result = subprocess.run(['route', 'print'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        if re.search(r'185\.2\.\d+\.\d+', output):
            print("Company VPN detected.")
            return True
        else:
            print("Company VPN not detected.")
            return False
    except Exception as e:
        print(f"Error checking VPN connection: {e}", file=sys.stderr)
        return False