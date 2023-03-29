import subprocess
import threading

def start_script_on_other_vehicle(remote_ip):
    username = "pi"
    password = "gopigo"
    remote_script_path = "/home/pi/platoon/run.py"

    command = "sshpass -p '{}' ssh {}@{} sudo python3 {}".format(password, username, remote_ip, remote_script_path)

    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        print("Script executed successfully on remote machine {}".format(remote_ip))
        print("Output:")
        print(result.stdout.decode("utf-8"))
    else:
        print("Error executing script on remote machine {}".format(remote_ip))
        print("Error message:")
        print(result.stderr.decode("utf-8"))

common_ip = "158.39.162."
unique_ip = ["127", "157", "181", "197"]

threads = []

for ip in unique_ip:
    full_ip = common_ip + ip
    # Create a new thread for each IP and add it to the threads list
    thread = threading.Thread(target=start_script_on_other_vehicle, args=(full_ip,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()
