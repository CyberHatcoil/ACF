import inspect
import os
import socket
import struct

import requests
from flask import json

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
PROTOCOLS = {6: "tcp",
             17: "udp"}
STATES = {1: "established",
          2: "tcp_syn_sent",
          3: "tcp_syn_recv",
          4: "tcp_fin_wait1",
          5: "tcp_fin_wait2",
          6: "time_wait",
          7: "tcp_close",
          8: "tcp_close_wait",
          9: "tcp_last_ack",
          10: "tcp_listen",
          11: "tcp_closing",
          12: "tcp_new_syn_recv"
          }


def load_metadata_plugins():
    def import_plugins():
        for name in os.listdir(os.path.join(ABS_PATH, 'metadata')):
            if (name.startswith(u'_')) or (not name.endswith(u'py')):
                continue
            name = u'metadata.%s' % name[:-3]
            mod = __import__(name)
            components = name.split(u'.')
            for comp in components[1:]:
                mod = getattr(mod, comp)
            yield mod
    for mod in import_plugins():
        try:
            for name, obj in inspect.getmembers(mod):
                if inspect.isclass(obj) and obj.__name__ != "MetadataPlugin":
                    yield obj()
        except Exception, e:
            pass


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
    ip_adresses = []
    while True:
        line = q.get()
        ip = line[6]
        res = []
        if ip not in ip_adresses:
            for p in metadata_plugins:
                res.append(p.run(ip))
            metadata_file.write("%s,%s" % (ip, ",".join(res)))
            metadata_file.flush()
        q.task_done()





def hex_to_ip(ip):
    packed = struct.pack("<L", ip)
    return socket.inet_ntoa(packed)


def hex_to_port(port):
    return int(port, 16)
