# coding=utf-8
from time import time


class Process(object):
    def __init__(self, p_dict, console_writer, log_file_writer, metadata_file_writer):
        self._connections_history = []
        self._console_writer = console_writer
        self._log_file_writer = log_file_writer
        self._metadata_file_writer = metadata_file_writer
        self.name = p_dict["name"]
        self.pid = p_dict["pid"]
        self.owner = p_dict["user"]

    def _manage_connections(self, connections, protocol):
        for src_ip, src_port, dst_ip, dst_port, state in connections:
            conn = (src_ip, src_port, dst_ip, dst_port, state)
            if conn in self._connections_history:
                continue
            self._connections_history.append(conn)
            output = (int(time()), self.name, self.pid, protocol, src_ip, src_port, dst_ip, dst_port, state)
            self._console_writer.put(output)
            self._log_file_writer.put(output)
            self._metadata_file_writer(output)

    def updateUdp(self, udp_conns):
        conns = []
        udp_conns = udp_conns[1:-1]
        for line in udp_conns:
            connection = line.split()
            src_ip = int(connection[1][:-5], 16)
            src_port = int(connection[1][-4:], 16)
            dst_ip = int(connection[2][:-5], 16)
            dst_port = int(connection[2][-4:], 16)
            state = int(connection[3], 16)

            conns.append((src_ip, src_port, dst_ip, dst_port, state))
        self._manage_connections(conns, 17)

    def updateTcp(self, tcp_conns):
        conns = []
        tcp_conns = tcp_conns[1:-1]
        for line in tcp_conns:
            connection = line.split()
            src_ip = int(connection[1][:-5], 16)
            src_port = int(connection[1][-4:], 16)
            dst_ip = int(connection[2][:-5], 16)
            dst_port = int(connection[2][-4:], 16)
            state = int(connection[3], 16)
            conns.append((src_ip, src_port, dst_ip, dst_port, state))
        self._manage_connections(conns, 6)

    def updateIcmp(self, icmp_conns):
        pass

    def updateRaw(self, raw_conns):
        pass