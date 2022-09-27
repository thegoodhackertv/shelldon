# Shelldon
Automated fully interactive reverse shell generator for Windows

Tool inspired by [hoaxshell](https://github.com/t3l3machus/hoaxshell).  - Generate a fully interactive reverse shell for Windows with [ConPtyShell](https://github.com/antonioCoco/ConPtyShell/)

# Installation
```bash
sudo apt install python3 python3-pip -y
git clone https://github.com/thegoodhackertv/shelldon.git
cd shelldon
pip install -r requirements.txt
```

# Usage
```bash
python3 shelldon.py -h
```
# Demo 
img-here

# How it works

1. First we use the payload.ps1 template to create powershell oneliner that invokes conpty.ps1
2. Encode the previous payload in base64
3. Create conpty.ps1 using ConPtyShell.ps1 template, change IP and PORT
4. Start a web server where conpty.ps1 will be hosted
5. Start a really ugly nc listener
6. Spawn a very pretty interactive shell

# References
[https://github.com/t3l3machus/hoaxshell](https://github.com/t3l3machus/hoaxshell)

[https://github.com/antonioCoco/ConPtyShell](https://github.com/antonioCoco/ConPtyShell)
