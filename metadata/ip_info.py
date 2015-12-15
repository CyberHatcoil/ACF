import json
import requests
from metadata import MetadataPlugin


class IpInfoPlugin(MetadataPlugin):
    def __init__(self):
        MetadataPlugin.__init__(self)
        self.name = "IpInfo"
        self._url = 'https://dazzlepod.com/ip/%s.json'

    def run(self):
        ip_info = self.get_ip_info(self._dst_ip)
        res = []
        for k, v in ip_info.iteritems():
            if len(v):
                res.append("%s: %s" % (k,v))
        return ",".join(res)

    def get_ip_info(self, ip):
        try:
            response = json.loads(requests.get(self._url % ip).text)
            for k in response.keys():
                response[k] = unicode(response[k])
            return response
        except Exception, e:
            return 'Error: Cannot retrieve %s info. Exception: %s' % (ip, e.message)