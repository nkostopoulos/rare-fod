import os

host1 = "clab-fod-lab-host1"
host2 = "clab-fod-lab-host2"

def execute_command(host, command):
    arg = "docker exec -it " + str(host) + " " + str(command)
    os.system(arg)
    return None

def execute_command_detached(host, command):
    arg = "docker exec -d " + str(host) + " " + str(command)
    os.system(arg)
    return None

def debug(command):
    print("Executing: ", command)
    print("------------------------------------")
    return None

if __name__ == "__main__":
    command = "apt update"
    debug(command)
    execute_command(host1, command)
    execute_command(host2, command)

    command = "apt install -y net-tools"
    debug(command)
    execute_command(host1, command)
    execute_command(host2, command)

    command = "apt install -y inetutils-ping"
    debug(command)
    execute_command(host1, command)
    execute_command(host2, command)

    command = "ifconfig eth1 10.0.1.2"
    debug(command)
    execute_command(host1, command)
    command = "ifconfig eth1 10.0.2.2"
    execute_command(host2, command)

    command = "apt install -y hping3"
    debug(command)
    execute_command(host1, command)

    command = "apt install -y nfdump"
    debug(command)
    execute_command(host2, command)

    command = "nfcapd -b 10.0.2.2 -p 9995 -l /var/cache/nfdump/"
    debug(command)
    execute_command_detached(host2, command)

    command = "docker cp parser.py clab-fod-lab-host2:/root/parser.py"
    debug(command)
    os.system(command)

    command = "apt install -y python3"
    debug(command)
    execute_command(host2, command)

    command = "timeout 10m hping3 -S 10.0.1.1 --flood"
    debug(command)
    execute_command_detached(host1, command)

    command = "python3 /root/parser.py"
    debug(command)
    execute_command(host2, command)
