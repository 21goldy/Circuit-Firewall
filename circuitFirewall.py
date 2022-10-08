import time

print('Choose 1 for ip blocking and 2 for url blocking: \n')

print('1. IP Blocking. \n2. URL Blocking')
print(" ")

choice = int(input("\nMake your choice 1 or 2: "))

if choice == 1:
    import os

    print("\n\nImporting Required Modules...")
    time.sleep(3)

    print("\nFinishing Importing.\n")

    ip = input('Enter IP here: ')
    print(" ")

    while True:
        if os.geteuid() != 0:
            print("Authentication Required!\n No root privileges.")
            print(" ")
            break

        else:
            IPTABLES_LIST = os.popen("iptables -L")
            read_iptables_list = IPTABLES_LIST.read()

            os.popen(f'iptables -I INPUT -s {ip} -j DROP')
            os.popen("ipset create Slowloris_blacklist hash:ip hashsize 4096")

            os.popen("iptables -I INPUT -m set --match-set Slowloris_blacklist src -j DROP")
            os.popen("iptables -I FORWARD -m set --match-set Slowloris_blacklist src -j DROP")

            os.popen(f"ipset add Slowloris_blacklist {ip}")

            blocking_IPTABLES = os.popen("ipset list")

            ip_IPTABLES = blocking_IPTABLES.read()

            print(ip_IPTABLES)
            print(" ")
            
            break

elif choice == 2:
    import os

    print("\n\nImporting Required Modules...")
    time.sleep(3)

    print("\nFinishing Importing.\n")

    os.popen("apt-get install squid -y")
    os.popen("systemctl start squid")
    os.popen("systemctl enable squid")

    print("Checking the squid status...")
    time.sleep(3)

    os.popen("systemctl status squid")
    print(" ")

    os.popen("squid -v")
    print(" ")

    os.popen("cd /etc/squid")
    print(" ")

    print("Enter the below details to proceed! \n")
    ip_server = input("Enter server ip: \n")
    url_blck = input("Enter url over here: \n")

    os.popen("cd /etc/squid")
    print(" ")

    with open("/etc/squid/squid.conf", "w") as file:
        file.write(f"acl test src {ip_server}\n")
        file.write("acl block dstdomain")

    with open("/etc/squid/block.txt", "w") as file:
        file.write(f"{url_blck}")

    with open("/etc/squid/squid.conf", "w") as file:
        file.write(f"acl test src {ip_server}\n")
        file.write('acl block dstdomain "/etc/squid/block.txt"\n')
        file.write("http_access deny test block\n")
        file.write("http_access allow test\n")

    os.popen("squid -s")

else:
    print("\nInvalid Input.")
