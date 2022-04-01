import paramiko
import time
import pymsgbox
#username = pymsgbox.prompt('Enter Your Username: ', "SSH Test With MassageBox")
passwd = pymsgbox.password('Enter Your password: ', 'SSH Test With MassageBox')
IP = "bekci.superonline.net"
port = 2222
username = "admin"
# pass_file = open("password.txt", "r")
# passwd = pass_file.read()
# passwd = passwd.strip()
# pass_file.close
start = time.time()

fp = open("IP_list.txt", "r")
node_list = fp.readlines()
fp.close()

fp = open("config.txt", "r")
command_list_tan = fp.readlines()
fp.close()

record_log = open("log_rbc.txt", "a+")

def func_timeout(node_info):
    print(node_info.strip() + ' is not accessible ' + '(' + time.ctime() + ')\n')
    record_log.write(node_info.strip() + ' is not accessible ' + '(' + time.ctime() + ')\n')
    channel.send('\r')
    time.sleep(2)


def func_no_device(node_info):
    print(node_info.strip() + ' does not exist in SSO ' + '(' + time.ctime() + ')\n')
    record_log.write(node_info.strip() + ' does not exist in SSO ' + '(' + time.ctime() + ')\n')
    channel.send('n' + '\r')
    time.sleep(2)


def func_no_exact_device(node_info):
    print(node_info.strip() + ' is not exactly in sso ' + '(' + time.ctime() + ')\n')
    record_log.write(node_info.strip() + ' is not exactly in sso ' + '(' + time.ctime() + ')\n')
    channel.send('n' + '\r')
    time.sleep(2)
    channel.send('*' + '\r')
    time.sleep(2)


def config_control():
    func_output = ''
    i = 0
    while i < len(command_list_tan):
        channel.send(command_list_tan[i] + '\r')
        print (command_list_tan[i] )
        time.sleep(2)
        i += 1

    while '>' not in func_output:
        func_output += str(channel.recv(65536).decode("ISO-8859-1"))
    return func_output

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(IP, port, username, password=passwd)
    print(IP, "Success entered")
    time.sleep(1)
except paramiko.AuthenticationException:
    print(IP, "Unsuccess entered")

channel = ssh.invoke_shell()
print(str(channel.recv(65536).decode("ISO-8859-1")))

for node in node_list:
    output = ''
    channel.send('\r')
    while 'Type to search or select one:' not in output:
        output += str(channel.recv(65536).decode("ISO-8859-1"))

    print(output + '\n')
    output = ''
    channel.send(node + '\r')
    time.sleep(2)

    while True:
        output += str(channel.recv(65536).decode("ISO-8859-1"))
        print(output)

        if "Cannot connect to device reason" in output:
            func_timeout(node)
            break

        if "Management IP Detection" in output:
            func_no_device(node)
            break

        if "No exact device Type '*'" in output:
            func_no_exact_device(node)
            break

        if "Type '*' to clear" in output:
            func_no_exact_device(node)
            break

        if "Info: No device found!" in output:
            record_log.write(node.strip() + ' is not found ' + '(' + time.ctime() + ')\n')
            break

        else:

            i = 0
            while i < len(command_list_tan):
                channel.send(' '+ command_list_tan[i] + '\r')
                print(command_list_tan[i])
                time.sleep(2)
                i += 1

            channel.send('\r')
            channel.send("logout" + '\r')
            time.sleep(2)

            channel.send('\r')
            time.sleep(2)
            output = str(channel.recv(65536).decode("ISO-8859-1"))

            print(output)
            record_screen = open("tan_config_log.csv", "a+")
            record_screen.write(output)
            record_screen.close()

            record_log.write(node.strip() + ' is OK ' + '(' + time.ctime() + ')\n')
            break
record_log.close()
channel.close()
end = time.time()
print("executed in " + str(end - start) + " seconds")
