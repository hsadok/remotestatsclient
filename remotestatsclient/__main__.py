# -*- coding: utf-8 -*-
import sys
import socket

from remotestatsclient import RemoteStatsClient


def main():
    if not (2 <= len(sys.argv) <= 4):
        print('RemoteStats (client)')
        print('')
        print('usage: python {} <http://server_address> [ hostname '
              '[interval] ]'.format(sys.argv[0]))
        print('')
        print('hostname: defaults to the computer name')
        print('interval: defaults to 5s')
        sys.exit(1)

    server = sys.argv[1]
    hostname = sys.argv[2] if len(sys.argv) > 2 else socket.gethostname()
    interval = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    RemoteStatsClient(server, hostname, interval).run()

if __name__ == '__main__':
    main()
