from utilities.utils import hex_to_ip


class MetadataPlugin(object):
    def __init__(self):
        self.name = ""
        self._pName = ""
        self._src_ip = ""
        self._src_port = ""
        self._dst_ip = ""
        self._dst_port = ""
        self._state = ""

    def run(self):
        pass

    def set_connection(self, connection):
        self._pName = connection[1]
        self._src_ip = hex_to_ip(connection[4])
        self._src_port = connection[5]
        self._dst_ip = hex_to_ip(connection[6])
        self._dst_port = connection[7]
        self._state = connection[8]
