"""
Android Connections Forensics (ACF)

Copyright (c) 2015-2016, Itay Kruk, CyberHat LTD
All rights reserved.

"""
import Queue
import argparse
import threading
from time import sleep
from modules.acf_core import Acf
from modules.adb import AndroidDebuggingBridge
from modules.process import Process
from utilities.utils import get_running_processes, console_writer, log_file_writer, metadata_file_writer


def set_up_writers(args):
    console_writer_q = Queue.Queue()
    console_writer_t = threading.Thread(target=console_writer, args=(console_writer_q,))
    console_writer_t.daemon = True
    console_writer_t.start()

    log_file_q = Queue.Queue()
    log_file_t = threading.Thread(target=log_file_writer, args=(log_file_q, args.log_file))
    log_file_t.daemon = True
    log_file_t.start()

    metadata_file_q = Queue.Queue()
    metadata_file_t = threading.Thread(target=metadata_file_writer, args=(metadata_file_q, args.plugin_file))
    metadata_file_t.daemon = True
    metadata_file_t.start()

    return console_writer_q, log_file_q, metadata_file_q


def main(args):
    processes = []
    try:
        console_writer_q, log_file_q, metadata_file_q = set_up_writers(args)

        acm = Acf(device_id=args.device_id, threads_num=args.threads)
        acm.setDaemon(True)
        acm.start()

        adb = AndroidDebuggingBridge(args.device_id)

        while True:
            running_processes = get_running_processes(adb)
            for process in running_processes:
                if process not in processes:
                    p = Process(process, console_writer_q, log_file_q, metadata_file_q)
                    processes.append(process)
                    acm.processes.append(p)
            sleep(1.2)

    except KeyboardInterrupt:
        print "Bye Bye"
        exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Acm - Android Connections Monitor')
    parser.add_argument('-d', action="store", dest="device_id",
                        help="Target device serial number or ip:port address [REQUIRED]")
    parser.add_argument('-o', action="store", dest="log_file", default="acm-log.log",
                        help="Output filename. Default: acm-log.log")
    parser.add_argument('-p', action="store", dest="metadata_file", default="metadata.log",
                        help="Output filename. Default: acm-log.log")
    parser.add_argument('-t', action="store", dest="threads", default=20, type=int,
                        help="Number of threads to use for monitoring. Default: 20")
    options = parser.parse_args()
    if options.device_id is None:
        parser.print_help()
        exit(0)
    main(options)
