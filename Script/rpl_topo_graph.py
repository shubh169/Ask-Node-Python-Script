from netmiko import Netmiko
import datetime
import re

class DeviceManager:
    def __init__(self, IpAddress, UserName, PassKey, DeviceType, command_list):
        self.IpAddress = IpAddress
        self.UserName = UserName
        self.PassKey = PassKey
        self.DeviceType = DeviceType
        self.command_list = command_list
        self.connection_status = None  # Initialize connection_status as None

    def print_config(self):
        print("="*30)

    def connect(self):
        self.print_config()
        print(f"Going to connect {self.IpAddress}")
        try:
            connection = Netmiko(
                host=self.IpAddress,
                username=self.UserName,
                password=self.PassKey,
                device_type=self.DeviceType
            )
            prompt = connection.find_prompt()
            if prompt.endswith("#"):
                print("Device connected successfully")
                self.connection_status = connection  # Update connection_status on successful connection
            else:
                print("Error: Unable to connect to the device")
        except Exception as e:
            print(f"Error connecting to device: {str(e)}")

    def execute_command(self):
        self.print_config()
        if not self.connection_status:
            print("Error: No active connection. Please establish a connection first.")
            return

        print("Going to execute commands on device")
        try:
            for cmd in self.command_list:
                print(f"\nCommand: {cmd}")
                output = self.connection_status.send_command(
                    cmd, delay_factor=150, expect_string=r"# ", read_timeout=30)
                # print("\nOutput:")
                # print(output)
                self.print_config()

                # Create a filename with current timestamp and command
                filename = "RPL_Topology_Graph.txt"

                # Write output to file
                with open(filename, 'w') as file:
                    file.write(output)

        except Exception as e:
            print(f"Error executing commands: {str(e)}")
            self.print_config()

# Enter your device lan address.
command_list=['cat /opt/iprf/tmp/rpltopology_graphWithMAC.txt | grep 61291212']
Device = DeviceManager("10.91.77.152", "root", "landisRoot", "linux", command_list)
Device.connect()
Device.execute_command()

with open("RPL_Topology_Graph.txt",'r') as ip_file:
    ip_details=ip_file.read()

# Regular expression pattern for matching IPv6 addresses
ipv6_pattern = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b'

# Read the contents of the file
filename = "RPL_Topology_Graph.txt"
with open(filename, 'r') as file:
    file_contents = file.read()

# Find all IPv6 addresses using re.findall
ipv6_addresses = re.findall(ipv6_pattern, file_contents)

# Print the IPv6 addresses found
for ipv6 in ipv6_addresses:
    final_ip_address=ipv6
    break

