import subprocess
import os
from time import sleep

BYTES_THRESHOLD = 20000

def return_command_output(command):
    proc = subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)
    (out, err) = proc.communicate()
    output = out.rstrip('\n'.encode('utf8'))
    return output

if __name__ == "__main__":
    while True:
        sleep(45)
        command = "ls /var/cache/nfdump/"
        files = return_command_output(command).decode('utf8')
        files_list = files.split("\n")
    
        max_timestamp = -1
        for afile in files_list:
            timestamp = afile.split(".")[1]
            if str(timestamp) == "current":
                continue
            else:
                timestamp = int(timestamp)
                if max_timestamp < timestamp:
                    max_timestamp = timestamp
        afile = "nfcapd." + str(max_timestamp)
    
        command = "nfdump -r /var/cache/nfdump/" + str(afile) + " -a -N -O packets"
        nfdump_output = return_command_output(command).decode('utf8')
        nfdump_split = nfdump_output.split("\n")

        ip_info = nfdump_split[1]
        ip_info = " ".join(ip_info.split())
        ip_info = ip_info.split(" ")

        protocol = ip_info[4]
        src_ip = ip_info[5].split(":")[0]
        dst_ip = ip_info[7].split(":")[0]
        number_bytes = ip_info[11]

        if int(number_bytes) > BYTES_THRESHOLD:
            os.chdir("/srv/flowspy")
            command = "./inst/helpers/enable_rule.sh " + str(src_ip) + "/32 " + str(dst_ip) + "/32 " + str(protocol) + " 1"
            os.system(command)

