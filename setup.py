import os

host1 = "clab-rare-lab-host1"
host2 = "clab-rare-lab-host2"
mtc   = "clab-rare-lab-mtc"

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
    # Apt update in host1, host2 and FoD containers
    command = "apt update"
    debug(command)
    execute_command(host1, command)
    execute_command(host2, command)
    execute_command(mtc, command)

    # Installation of package "net-tools" for ifconfig
    command = "apt install -y net-tools"
    debug(command)
    execute_command(host1, command)
    execute_command(host2, command)
    execute_command(mtc, command)

    # Installation of package "inetutils-ping" for ping
    command = "apt install -y inetutils-ping"
    debug(command)
    execute_command(host1, command)
    execute_command(host2, command)
    execute_command(mtc, command)

    # Installation of package "iproute2" for static routes
    command = "apt install -y iproute2"
    debug(command)
    execute_command(host1, command)
    execute_command(host2, command)

    # Ifconfig commands to configure non-management container interfaces
    command = "ifconfig eth1 10.0.1.2"
    debug(command)
    execute_command(host1, command)
    command = "ifconfig eth1 10.0.2.2"
    execute_command(host2, command)
    command = "ifconfig eth1 10.0.3.2"
    execute_command(mtc, command)

    # Configuration of static routes on hosts host1 and host2
    command = "ip route add 10.0.2.0/24 via 10.0.1.1"
    debug(command)
    execute_command(host1, command)
    command = "ip route add 10.0.1.0/24 via 10.0.2.1"
    debug(command)
    execute_command(host2, command)

    # Install of package "hping3" in host1 in order to DDoS host2
    command = "apt install -y hping3"
    debug(command)
    execute_command(host1, command)

    # Install of package "nfdump" in FoD (NetFlow collector)
    command = "apt install -y nfdump"
    debug(command)
    execute_command(mtc, command)

    # Run "nfcapd" command to collect NetFlow records
    command = "nfcapd -b 10.0.3.2 -p 9995 -l /var/cache/nfdump/ -t 30s"
    debug(command)
    execute_command_detached(mtc, command)

    # Copy the "parser.py" script that parsers nfdump output
    command = "docker cp parser.py clab-rare-lab-mtc:/root/parser.py"
    debug(command)
    os.system(command)

    # Install Python 3 within the FoD container
    command = "apt install -y python3"
    debug(command)
    execute_command(mtc, command)

    # Rewrite ExaBGP configuration in the FoD container with the necessary parameters
    command = "./exabgp/run-exabgp-generic --init-conf 10.0.3.2 10.0.3.2 1001 10.0.3.1 10.0.3.1 2001 -- --supervisord --restart"
    debug(command)
    execute_command(mtc, command)

    # DDoS host2 from host1 using "hping3"
    command = "timeout 10m hping3 --icmp 10.0.2.2 --flood"
    debug(command)
    execute_command_detached(host1, command)

    # Run the "parser.py" Python script
    command = "python3 /root/parser.py"
    debug(command)
    execute_command_detached(mtc, command)
