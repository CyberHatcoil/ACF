import requests
from flask import json

from metadata import MetadataPlugin


class IP_Rep(MetadataPlugin):
    def __init__(self):
        MetadataPlugin.__init__(self)

    def run(self, ip):
        ip_info = self.get_ip_info(ip)
        res = []
        for k,v in ip_info.iteritems():
            res.append("%s: %s" % (k,v))
        return ",".join(res)


    def get_ip_info(self, ip):
        try:
            url = 'https://dazzlepod.com/ip/%s.json' % ip
            response = json.loads(requests.get(url).text)
            for k in response.keys():
                response[k] = unicode(response[k])
            return response
        except Exception, e:
            return 'Error: Cannot retrieve %s info. Exception: %s' % (ip, e.message)