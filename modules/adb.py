from subprocess import Popen, PIPE


class AndroidDebuggingBridge(object):
    def __init__(self, device_id):
        self.device = device_id
        self.error = ""
        self.output = ""
        self.connected_devices()

    def execute(self, cmd):
        (stdout, stderr) = Popen('adb -s %s %s' % (self.device, cmd), shell=True, stdout=PIPE).communicate()
        self.output = stdout
        self.error = stderr

    @staticmethod
    def shell(cmd, device):
        (stdout, stderr) = Popen('adb -s %s %s' % (device, cmd), shell=True, stdout=PIPE).communicate()
        output = stdout
        error = stderr
        return stdout

    def kill_server(self):
        self.execute("kill-server")
        return self.output

    def start_server(self):
        self.execute("start-server")
        return self.output

    def push(self, local, remote):
        self.execute("pull {local} {remote}".format(remote=local, local=remote))

    def connected_devices(self):
        self.execute("devices")
        if "device" in self.output.split("\n")[1]:
            return True
        print "Please connect a device. Make sure usb debugging mode is enabled and pc is authorized"
        exit(0)

    def get_dumpsys(self, package):
        self.execute("shell dumpsys package {package}".format(package=package))
        return self.output

    def get_model(self):
        self.execute("shell getprop ro.product.model")
        return self.output

    def get_serial_number(self):
        self.execute("get-serialno")
        return self.output

    def get_processes(self):
        self.execute("shell ps")
        return self.output.split('\n')[1:-1]

    def get_os_version(self):
        self.execute("shell getprop ro.build.version.release")
        return self.output