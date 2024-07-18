from netmiko import Netmiko
import rpl_topo_graph
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
                print("\nOutput:")
                print(output)
                self.print_config()

                # Create a filename with current timestamp and command
                now = datetime.datetime.now().replace(microsecond=0)
                timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
                sanitized_cmd = re.sub(r'[^a-zA-Z0-9]', '_', cmd)[:65]
                filename = f"{timestamp}_{sanitized_cmd}.txt"

                # Write output to file
                with open(filename, 'w') as file:
                    file.write(output)

        except Exception as e:
            print(f"Error executing commands: {str(e)}")
            self.print_config()

ip = rpl_topo_graph.final_ip_address
command_list = [
    f'ask_node -d {ip} -ci 0x41 -m get4e0',
    f'ask_node -d {ip} -ci 0x41 -m get4e1',
    f'ask_node -d {ip} -ci 0x41 -m get4e2',
    f'ask_node -d {ip} -ci 0x41 -m get4e3'
]
Device = DeviceManager("10.91.77.152", "root", "landisRoot", "linux", command_list)
Device.connect()
Device.execute_command()
