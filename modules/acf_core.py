import Queue
import threading
from time import sleep
from modules.adb import AndroidDebuggingBridge

DIRECTORY_NOT_FOUND = "directory"

class Acf(threading.Thread):
    def __init__(self, device_id, threads_num=20):
        threading.Thread.__init__(self)
        self.processes = []
        self._command = "shell cat /proc/{pid}/net/icmp /proc/{pid}/net/tcp /proc/{pid}/net/udp /proc/{pid}/net/raw"
        self._adb = AndroidDebuggingBridge(device_id)
        self._processes_queue = Queue.Queue()
        self._THREADS_NUM = threads_num
        self._create_threads()

    def run(self):
        while True:
            if self._processes_queue.empty():
                self._populate_processes_queue()
            sleep(0.8)

    def _populate_processes_queue(self):
        for p in self.processes:
            self._processes_queue.put(p)

    def _acm_worker(self):
        while True:
            #todo: adb instance for each worker
            process = self._processes_queue.get()
            self._adb.execute(self._command.format(pid=process.pid))
            if DIRECTORY_NOT_FOUND in self._adb.output:
                self._processes_queue.task_done()
                continue
            conns = self._adb.output.split("\r\r\n")
            process.updateConnections(conns)

            self._processes_queue.task_done()

    def _create_threads(self):
        for i in xrange(self._THREADS_NUM):
            t = threading.Thread(target=self._acm_worker)
            t.daemon = True
            t.start()
