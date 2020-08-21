import socket
from contextlib import closing
import argparse
import os
import sys
import pdb
import argparse
sys.path.insert(0, '/scratche/home/ashutosh/services/queue/')

from queue_client import QueueClient


# AVAILABLE SERVERS
SERVERS = {
    "idli" : "10.24.28.102",
    "momo" : "10.24.28.103",
    "dosa" : "10.24.28.104",
    "poha" : "10.24.28.105",
    "puri" : "10.24.28.106",
    "peda" : "10.24.28.107",
    "pani" : "10.24.28.108"
}

# QUEUE CLIENT RUNNING HERE
S = 'http://10.24.28.106:7815/'
q = QueueClient(S)

def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return not (sock.connect_ex((host, port)) == 0)

def checkrange(host, ll=4200, ul=4300):
    res = []
    for b in range(ll, ul+1):
        if check_socket(host, b):
            res.append(b)
    return res


def main(args):
    host = SERVERS[args.system]

    available_ports = checkrange(host)
    print('{} Available ports on {}:{}'.format(len(available_ports), args.system, host))

    if args.writeinq:
        print('Writing in queue server at {}'.format(S))
        for i, ports in enumerate(available_ports):
            q.enqueue(ports)
            print('{} ports added in queue'.format(i+1), end='\r')

        print('{} ports added in queue'.format(i+1))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check available ports and put them in\
                                     queue server')
    parser.add_argument('-system',
                        type=str,
                        required=True,
                        choices=['idli', 'momo', 'dosa', 'poha', 'puri','peda','pani'],
                        help='Which server to check for open ports')
    parser.add_argument('-clear',     	action='store_true')
    parser.add_argument('-allclear',    action='store_true')
    parser.add_argument('-writeinq', action='store_true')
    args = parser.parse_args()

    if args.clear:
        q.clear()
    if args.allclear:
        q.clear()
        exit(0)

    main(args)
