import subprocess

def return_command_output(command):
    proc = subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)
    (out, err) = proc.communicate()
    output = out.rstrip('\n'.encode('utf8'))
    return output

if __name__ == "__main__":
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

    command = "nfdump -r /var/cache/nfdump/" + str(afile) + " -s srcip -a"
    print(command)
    nfdump_output = return_command_output(command).decode('utf8')
    nfdump_split = nfdump_output.split("\n")

    output_temp = nfdump_split[2]
    output_temp = " ".join(output_temp.split())
    output_temp = output_temp.split(" ")

    src_ip = output_temp[4]
    flows = output_temp[5] + " " + output_temp[6]
    packets = output_temp[7] + " " + output_temp[8] 
    number_bytes = output_temp[9] + " " + output_temp[10]

    print("src_ip: ", src_ip)
    print("flows: ", flows)
    print("packets: ", packets)
    print("number_bytes: ", number_bytes)
