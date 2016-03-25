# -*- coding: utf-8 -*-

from remotestatsclient import RemoteStatsClient


def main():
    server = "http://127.0.0.1:4567/"
    hostname = "lalaa"
    RemoteStatsClient(server, hostname, 5).run()

if __name__ == '__main__':
    main()
