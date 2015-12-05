from metadata import MetadataPlugin


class IP_Rep(MetadataPlugin):
    def __init__(self):
        MetadataPlugin.__init__(self)

    def run(self, ip):
        return "hi"
