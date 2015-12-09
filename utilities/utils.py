import inspect
import os
import socket
import struct

from datetime import datetime
from netaddr import IPAddress

PROTOCOLS = {6: "tcp",
             17: "udp"}
STATES = {1: "established",
          2: "syn_sent",
          3: "syn_recv",
          4: "fin_wait1",
          5: "fin_wait2",
          6: "time_wait",
          7: "close",
          8: "close_wait",
          9: "last_ack",
          10: "listen",
          11: "closing",
          12: "new_syn_recv"
          }


def load_metadata_plugins():
    def import_plugins():
        for name in os.listdir('metadata'):
            if (name.startswith(u'_')) or (not name.endswith(u'py')):
                continue
            name = u'metadata.%s' % name[:-3]
            mod = __import__(name)
            components = name.split(u'.')
            for comp in components[1:]:
                mod = getattr(mod, comp)
            yield mod
    metadata_plugins = []
    for mod in import_plugins():
        try:
            for name, obj in inspect.getmembers(mod):
                if inspect.isclass(obj) and obj.__name__ != "MetadataPlugin":
                    if obj.__name__.endswith("Plugin"):
                        metadata_plugins.append(obj())
        except Exception, e:
            pass
    return metadata_plugins


def get_running_processes(adb):
    try:
        ps = adb.get_processes()
        for process in ps:
            pDict = {}
            cols = process.split()
            pDict.update({
                "user": cols[0],
                "pid": cols[1],
                "name": cols[-1]
            })
            yield pDict
    except Exception, e:
        print "[!] Cannot retrieve running processes. Exception: %s" % e.message


def log_file_writer(loq_queue, filename):
    log_file = open(filename, "w")
    while True:
        line = list(loq_queue.get())
        line[0] = datetime.fromtimestamp(line[0])
        line[3] = PROTOCOLS[line[3]]
        line[4] = hex_to_ip(line[4])
        line[6] = hex_to_ip(line[6])
        line[-1] = STATES[line[-1]]

        log_file.write(', '.join(map(str, line)) + "\n")
        log_file.flush()
        loq_queue.task_done()


def console_writer(console_writer_queue):
    while True:
        line = list(console_writer_queue.get())
        line[3] = PROTOCOLS[line[3]]
        line[4] = hex_to_ip(line[4])
        line[6] = hex_to_ip(line[6])
        line[-1] = STATES[line[-1]]
        print ', '.join(map(str, line))
        console_writer_queue.task_done()


def metadata_file_writer(q, filename):
    metadata_plugins = load_metadata_plugins()
    metadata_file = open(filename, "w")
    ip_adresses = [0]
    while True:
        connection = q.get()
        ip = connection[6]
        if ip not in ip_adresses and not IPAddress(hex_to_ip(ip)).is_private():
            ip_adresses.append(ip)
            for p in metadata_plugins:
                p.set_connection(connection)
                res = p.run()
                if len(res):
                    metadata_file.write("%s, %s,%s\n" % (p.name, hex_to_ip(ip), res))
                    metadata_file.flush()
        q.task_done()


def hex_to_ip(ip):
    packed = struct.pack("<L", ip)
    return socket.inet_ntoa(packed)


def hex_to_port(port):
    return int(port, 16)
