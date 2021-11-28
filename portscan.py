#!/usr/bin/env python3
# it's a BIG unicorn
import sys
import socket
import time
import parser
from multiprocessing.dummy import Pool


class PortScan:
    """ Класс-скан портов """

    def __init__(self):
        """ Инициализация """

        self.parser = parser.parse_arguments()
        self.timeout = self.parser.parse_args(sys.argv[1:]).timeout
        self.ip = self.parser.parse_args(sys.argv[1:]).ip_address[0]
        self.ports = self.parser.parse_args(sys.argv[1:]).tcp_udp
        self.tcp = set()
        self.udp = set()
        self.verbose = self.parser.parse_args(sys.argv[1:]).verbose

    def main(self):
        """ Запускает программу """

        self.parse_tcp_and_udp()
        count_of_threads = self.parser.parse_args(sys.argv[1:]).num_threads
        pool = Pool(count_of_threads)
        pool.map(self.tcp_scan_port, sorted(list(self.tcp)))
        pool.map(self.udp_scan_port, sorted(list(self.udp)))
        pool.close()
        pool.join()

    def parse_tcp_and_udp(self):
        """ Парсит TCP и UDP порты """

        for i in range(len(self.ports) - 1):
            if self.ports[i] == "tcp" and self.ports[i + 1].startswith("udp/") or \
                    self.ports[i] == "udp" and self.ports[i + 1].startswith("tcp/"):
                parts = self.ports[i + 1][4:].split(",")
                parser.parse_parts(parts, self.tcp)
                parser.parse_parts(parts, self.udp)
            elif self.ports[i].startswith("tcp/"):
                parts = self.ports[i][4:].split(",")
                parser.parse_parts(parts, self.tcp)
            else:
                parts = self.ports[i][4:].split(",")
                parser.parse_parts(parts, self.udp)
        if self.ports[-1].startswith("tcp/"):
            parts = self.ports[-1][4:].split(",")
            parser.parse_parts(parts, self.tcp)
        elif self.ports[-1].startswith("udp/"):
            parts = self.ports[-1][4:].split(",")
            parser.parse_parts(parts, self.udp)

    def tcp_scan_port(self, port):
        """ TCP сканер """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        span_in_ms = ""
        try:
            if self.verbose:
                t = time.time()
                connect = sock.connect((self.ip, port))
                span_in_ms = f" {time.time() * 1000 - t * 1000}"
            else:
                connect = sock.connect((self.ip, port))
            print(f"TCP {port}{span_in_ms}")
            connect.close()
        except socket.error as e:
            print(f"Something wrong! {e}")

    def udp_scan_port(self, port):
        """ UDP сканер """

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)
        try:
            sock.sendto(b'qwertyasdfghzxcvbn123', (self.ip, port))
            data, addr = sock.recvfrom(1024)
            print(f"UDP {port}")
            sock.close()
        except socket.error as e:
            print(f"Something wrong! {e}")


if __name__ == "__main__":
    PortScan().main()
