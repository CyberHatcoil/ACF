from ipwhois import IPWhois
from metadata import MetadataPlugin


class WhoIsPlugin(MetadataPlugin):
    def __init__(self):
        MetadataPlugin.__init__(self)
        self.name = "WhoIs"

    def run(self):
        try:
            ip_whois = IPWhois(self._dst_ip)
            raw_res = ip_whois.lookup()
            res = []
            for k,v in raw_res.iteritems():
                if not v is None:
                    res.append("%s: %s" % (k,v))
            return ",".join(res)
        except Exception, e:
             return ""