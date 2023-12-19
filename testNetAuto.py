from ncclient import manager
from email.policy import default
import sys
import xml.dom.minidom
import requests

while True:
    try:
        with manager.connect(
            host="192.168.174.128",
            port=830,
            username="cisco",
            password="cisco123!",
            hostkey_verify=False,
            device_params={'name': 'csr'}
        ) as m:

            def print_table(headers, data):
                print("-" * 50)
                print("{:<50}".format(headers))
                for row in data:
                    print("{:<50}".format(row))

            def hostname_config(rtr_hostname):
                config = """
                    <config>
                        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                            <hostname>{}</hostname>
                        </native>
                    </config>
                """.format(rtr_hostname)
                m.edit_config(target='running', config=config)
                print_table("Configuration is a success!", ["Hostname: {}".format(rtr_hostname)])

            def loopint_config(interface_name, interface_description, interface_ip, interface_mask):
                config = """
                    <config>
                        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                            <interface>
                                <Loopback>
                                    <name>{}</name>
                                    <description>{}</description>
                                    <ip>
                                        <address>
                                            <primary>
                                                <address>{}</address>
                                                <mask>{}</mask>
                                            </primary>
                                        </address>
                                    </ip>
                                </Loopback>
                            </interface>
                        </native>
                    </config>
                """.format(interface_name, interface_description, interface_ip, interface_mask)

                m.edit_config(target='running', config=config)
                print_table("Configuration is a success!",
                            ["Interface Name: {}".format(interface_name),
                             "Description: {}".format(interface_description),
                             "IP Address: {}".format(interface_ip),
                             "Subnet Mask: {}".format(interface_mask)])

            def ipv6_config(ipv6_add, prefix_length):
                config = """
                    <config>
                        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                            <interface>
                                <name>GigabitEthernet1</name>
                                    <description>Interface G1</description>
                                        <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                                            <address>
                                                <ip>{}</ip>
                                                <prefix-length>{}</prefix-length>
                                            </address>
                                        </ipv6>
                            </interface>
                        </interfaces>
                    </config>
                    """.format(ipv6_add, prefix_length)

                m.edit_config(target='running', config=config)
                print_table("Configuration is a success!",
                            ["IPv6 Address: {}".format(ipv6_add),
                             "Prefix Length: {}".format(prefix_length)])

            print_table("  | Automated Network Configuration on CSR1kv |", [])
            print_table(">> Enter number option for configuration:", [])
            print_table(" > 1. Set new hostname", [])
            print_table(" > 2. Assign a Loopback Interface", [])
            print_table(" > 3. Configure IPv6 Address for GigabitEthernet1", [])
            print_table(" > Type q or quit to exit\n", [])
            config_option = input("Input Option -> ")

            if config_option == "1":
                rtr_hostname = input("Enter the new hostname: ")
                hostname_config(rtr_hostname)
                
                access_token = 'MmEyZTA5NjctMmIyNy00Y2U5LTk2ZTItMjdlZmU2ZTM2ZTgyMDlmNTYwOGMtNThi_P0A1_d0b19fc5-a717-4064-90e2-8d88b3acad9c'
                room_id = '05f86f00-3ca2-11ee-a5e9-c96f64fbde09'
                message = f'Hostname **{rtr_hostname}** has been added successfully.'
                url = 'https://webexapis.com/v1/messages'
                headers = {
                    'Authorization': 'Bearer {}'.format(access_token),
                    'Content-Type': 'application/json'
                }
                params = {'roomId': room_id, 'markdown': message}
                res = requests.post(url, headers=headers, json=params)

            elif config_option == "2":
                interface_name = input("Enter desired Loopback interface: ")
                interface_description = input("Enter interface description: ")
                interface_ip = input("Enter the IP address of the interface (X.X.X.X): ")
                interface_mask = input("Enter the subnet mask  of the interface (X.X.X.X): ")
                loopint_config(interface_name, interface_description, interface_ip, interface_mask)

                access_token = 'MmEyZTA5NjctMmIyNy00Y2U5LTk2ZTItMjdlZmU2ZTM2ZTgyMDlmNTYwOGMtNThi_P0A1_d0b19fc5-a717-4064-90e2-8d88b3acad9c'
                room_id = '05f86f00-3ca2-11ee-a5e9-c96f64fbde09'
                message = 'Loopback interface has been successfully configured.'
                url = 'https://webexapis.com/v1/messages'
                headers = {
                    'Authorization': 'Bearer {}'.format(access_token),
                    'Content-Type': 'application/json'
                }
                params = {'roomId': room_id, 'markdown': message}
                res = requests.post(url, headers=headers, json=params)

            elif config_option == "3":
                default_prefixlength = 64
                ipv6_add = input("Enter IPv6 Address (X:X:X::X): ")
                prefix_length = input("Enter Prefix length: ") or default_prefixlength
                ipv6_config(ipv6_add, prefix_length)

                access_token = 'MmEyZTA5NjctMmIyNy00Y2U5LTk2ZTItMjdlZmU2ZTM2ZTgyMDlmNTYwOGMtNThi_P0A1_d0b19fc5-a717-4064-90e2-8d88b3acad9c'
                room_id = '05f86f00-3ca2-11ee-a5e9-c96f64fbde09'
                message = 'IPv6 Address successfully configured.'
                url = 'https://webexapis.com/v1/messages'
                headers = {
                    'Authorization': 'Bearer {}'.format(access_token),
                    'Content-Type': 'application/json'
                }
                params = {'roomId': room_id, 'markdown': message}
                res = requests.post(url, headers=headers, json=params)

            elif config_option == "q" or config_option == "quit":
                break

            try:
                res = requests.post(url, headers=headers, json=params)
                res.raise_for_status()
                print_table("Notification sent to Webex teams successfully!", [])
            except requests.exceptions.RequestException as e:
                print_table("Error sending notification: {}".format(e), [])

    except Exception as e:
        print("Error: ", e)
        sys.exit(1)
