import argparse


def parse_arguments():
    """ Возвращает парсер для входных данных """

    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", help="input timeout of waiting", default=2, type=float)
    parser.add_argument("ip_address", nargs=1)
    parser.add_argument("tcp_udp", nargs="+")
    parser.add_argument("-j", "--num-threads", type=int, default=32)
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def parse_parts(parts, tcp_or_udp):
    """ Парсит части портов """

    for part in parts:
        part = part.split("-")
        if len(part) == 2:
            tcp_or_udp |= set(list(range(int(part[0]), int(part[1]) + 1)))
            continue
        tcp_or_udp.add(int(part[0]))
