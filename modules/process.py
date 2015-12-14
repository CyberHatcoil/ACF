# coding=utf-8
from time import time
from utilities.utils import PROTOCOLS, hex_to_ip
from netaddr import IPAddress


class Process(object):
    def __init__(self, p_dict, console_writer, log_file_writer, metadata_file_writer):
        self._connections_history = []
        self._console_writer = console_writer
        self._log_file_writer = log_file_writer
        self._metadata_file_writer = metadata_file_writer
        self._protocols = sorted([p for p in PROTOCOLS])
        self.name = p_dict["name"]
        self.pid = p_dict["pid"]
        self.owner = p_dict["user"]

    def _manage_connections(self, connections):
        for src_ip, src_port, dst_ip, dst_port, protocol, state in connections:
            conn = (src_ip, src_port, dst_ip, dst_port, state)
            if (conn[2] == 0) or (conn in self._connections_history) or (IPAddress(hex_to_ip(conn[2])).is_loopback()):
                continue
            self._connections_history.append(conn)
            output = (int(time()), self.name, self.pid, protocol, src_ip, src_port, dst_ip, dst_port, state)
            self._console_writer.put(output)
            self._log_file_writer.put(output)
            self._metadata_file_writer.put(output)

    def updateConnections(self, conns):
        try:
            formatted_conns = []
            current_protocol = 0
            conns = conns[1:-1]
            for connection in conns:
                if "local_address" in connection:
                    current_protocol += 1
                    continue
                connection = connection.split()
                src_ip = int(connection[1][:-5], 16)
                src_port = int(connection[1][-4:], 16)
                dst_ip = int(connection[2][:-5], 16)
                dst_port = int(connection[2][-4:], 16)
                protocol = self._protocols[current_protocol]
                state = int(connection[3], 16)
                formatted_conns.append((src_ip, src_port, dst_ip, dst_port, protocol, state))
        except Exception,e:
            print "[!] Exception while parsing connections from %s. Exception: %s" % (self.name, e.message)
        self._manage_connections(formatted_conns)
