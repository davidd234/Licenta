import platform
import socket
import subprocess

import yaml
from netmiko import ConnectHandler


YAML_FILE = "network.yaml"


def load_yaml():
    with open(YAML_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def normalize_devices(data):
    devices = []

    if not data:
        return devices

    if "devices" in data:
        for name, info in data["devices"].items():
            if info.get("enabled", True) is False:
                continue

            devices.append({
                "name": info.get("display_name", name),
                "ip": info.get("ip"),
                "protocol": info.get("protocol", "ssh"),
                "device_type": info.get("device_type", "cisco_ios"),
                "username": info.get("username", "admin"),
                "password": info.get("password", "remote"),
                "secret": info.get("secret", "cisco")
            })

        return devices

    # Compatibilitate cu formatul vechi de YAML, in caz ca exista sectiuni pe site-uri.
    for section_name, section in data.items():
        if not isinstance(section, dict):
            continue

        for name, interfaces in section.items():
            if not isinstance(interfaces, dict):
                continue

            for int_name, values in interfaces.items():
                if isinstance(values, list) and len(values) >= 1:
                    ip = values[0]
                    devices.append({
                        "name": name,
                        "ip": ip,
                        "protocol": "ssh",
                        "device_type": "cisco_ios",
                        "username": "admin",
                        "password": "remote",
                        "secret": "cisco"
                    })

    return devices


def ping_ip(ip):
    try:
        system_name = platform.system().lower()

        if system_name == "windows":
            command = ["ping", "-n", "1", "-w", "1000", ip]
        else:
            command = ["ping", "-c", "1", "-W", "1", ip]

        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False


def check_port(ip, port=22):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def build_connection(device):
    protocol = device.get("protocol", "ssh").lower()
    device_type = device.get("device_type", "cisco_ios")

    # Daca in YAML scrie protocol: telnet, Netmiko trebuie sa foloseasca driverul telnet.
    if protocol == "telnet" and device_type == "cisco_ios":
        device_type = "cisco_ios_telnet"

    connection = {
        "device_type": device_type,
        "host": device["ip"],
        "username": device.get("username", "admin"),
        "password": device.get("password", "remote"),
        "secret": device.get("secret", "cisco"),
        "timeout": 15,
        "conn_timeout": 15,
        "banner_timeout": 20,
        "auth_timeout": 20,
        "fast_cli": False
    }

    if protocol == "telnet":
        connection["port"] = 23

    return connection


def save_config(connection):
    try:
        return connection.save_config()
    except Exception:
        return connection.send_command_timing("write memory")


def choose_device(devices):
    if not devices:
        print("No devices found in network.yaml.")
        return None

    print("\nAvailable devices:")
    for index, device in enumerate(devices):
        protocol = device.get("protocol", "ssh").upper()
        print(f"{index}. {device['name']} - {device['ip']} ({protocol})")

    try:
        choice = int(input("\nChoose device number: ").strip())
        if choice < 0 or choice >= len(devices):
            print("Invalid choice.")
            return None
        return devices[choice]
    except ValueError:
        print("Invalid choice.")
        return None


def configure_interface(devices):
    device = choose_device(devices)
    if not device:
        return

    interface = input("Interface name: ").strip()
    ip = input("IP address: ").strip()
    mask = input("Subnet mask: ").strip()

    if not interface or not ip or not mask:
        print("Interface, IP address and subnet mask are required.")
        return

    commands = [
        f"interface {interface}",
        f"ip address {ip} {mask}",
        "no shutdown"
    ]

    try:
        print(f"\nConnecting to {device['name']} ({device['ip']})...")
        connection = ConnectHandler(**build_connection(device))
        connection.enable()

        print("\n--- Applying configuration ---")
        output = connection.send_config_set(commands)
        print(output)

        print("\n--- Saving configuration ---")
        print(save_config(connection))

        print("\n--- Verification ---")
        verify_output = connection.send_command(f"show ip interface brief | include {interface}")
        print(verify_output if verify_output.strip() else "No matching interface found in output.")

        connection.disconnect()
        print("\nConfiguration applied successfully.")

    except Exception as e:
        print(f"Connection/configuration failed: {e}")


def verify_connectivity(devices):
    device = choose_device(devices)
    if not device:
        return

    target = input("Target IP for ping: ").strip()

    if not target:
        print("Target IP is required.")
        return

    try:
        print(f"\nConnecting to {device['name']} ({device['ip']})...")
        connection = ConnectHandler(**build_connection(device))
        connection.enable()

        output = connection.send_command_timing(f"ping {target}")
        print(output)

        connection.disconnect()
    except Exception as e:
        print(f"Ping failed: {e}")


def test_all_yaml_devices(devices):
    print("\n--- Test conectivitate NetworkAutomation -> toate device-urile din YAML ---\n")
    print(f"Au fost gasite {len(devices)} device-uri.\n")

    print(f"{'Nr':<5}{'Device':<12}{'IP':<18}{'PING':<12}{'SSH/TELNET'}")
    print("-" * 65)

    for index, device in enumerate(devices):
        ip = device["ip"]
        protocol = device.get("protocol", "ssh").lower()

        ping_status = "OK" if ping_ip(ip) else "FAIL"

        if protocol == "telnet":
            port_status = "OK" if check_port(ip, 23) else "FAIL"
        else:
            port_status = "OK" if check_port(ip, 22) else "FAIL"

        print(f"{index:<5}{device['name']:<12}{ip:<18}{ping_status:<12}{port_status}")


def see_config(devices):
    device = choose_device(devices)
    if not device:
        return

    try:
        print(f"\nConnecting to {device['name']} ({device['ip']})...")
        connection = ConnectHandler(**build_connection(device))
        connection.enable()

        output = connection.send_command("show running-config")
        print(output)

        connection.disconnect()
    except Exception as e:
        print(f"Could not get config: {e}")


def delete_interface(devices):
    device = choose_device(devices)
    if not device:
        return

    interface = input("Interface name to delete, example Loopback99: ").strip()

    if not interface:
        print("Interface name is required.")
        return

    commands = [
        f"no interface {interface}"
    ]

    try:
        print(f"\nConnecting to {device['name']} ({device['ip']})...")
        connection = ConnectHandler(**build_connection(device))
        connection.enable()

        print("\n--- Removing interface ---")
        output = connection.send_config_set(commands)
        print(output)

        print("\n--- Saving configuration ---")
        print(save_config(connection))

        print("\n--- Verification ---")
        verify_output = connection.send_command(f"show ip interface brief | include {interface}")
        if verify_output.strip():
            print(verify_output)
        else:
            print(f"{interface} no longer appears in show ip interface brief.")

        connection.disconnect()
        print("\nInterface removed successfully.")

    except Exception as e:
        print(f"Interface removal failed: {e}")


def menu():
    data = load_yaml()
    devices = normalize_devices(data)

    while True:
        print("\nWelcome to Network Automation's Main Menu")
        print("==========================================")
        print("1. Configure an interface on a device (Interactively)")
        print("2. Verify Connectivity")
        print("3. Test NetworkAutomation reachability to all YAML devices")
        print("4. See the config of a device")
        print("5. Delete a test interface")
        print("0. Exit")
        print("==========================================")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            configure_interface(devices)
        elif choice == "2":
            verify_connectivity(devices)
        elif choice == "3":
            test_all_yaml_devices(devices)
        elif choice == "4":
            see_config(devices)
        elif choice == "5":
            delete_interface(devices)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()
