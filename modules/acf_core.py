import Queue
import threading
from time import sleep
from modules.adb import AndroidDebuggingBridge


class Acf(threading.Thread):
    def __init__(self, device_id, threads_num=20):
        threading.Thread.__init__(self)
        self.processes = []
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
            process = self._processes_queue.get()
            self._adb.execute("shell cat /proc/%s/net/tcp" % process.pid)
            tcp_conns = self._adb.output.split("\r\r\n")
            process.updateTcp(tcp_conns)

            self._adb.execute("shell cat /proc/%s/net/udp" % process.pid)
            udp_conns = self._adb.output.split("\r\r\n")
            process.updateUdp(udp_conns)
            self._processes_queue.task_done()

    def _create_threads(self):
        for i in xrange(self._THREADS_NUM):
            t = threading.Thread(target=self._acm_worker)
            t.daemon = True
            t.start()
