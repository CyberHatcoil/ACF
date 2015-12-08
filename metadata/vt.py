import json
import urllib
from metadata import MetadataPlugin
from utilities.utils import hex_to_ip


class VirusTotalPlugin(MetadataPlugin):
    def __init__(self):
        MetadataPlugin.__init__(self)
        self.name = "VirusTotal"
        self._api_key = ""
        self._api_url = 'https://www.virustotal.com/vtapi/v2/'


    def run(self):
        if self._api_key == "":
            return ""
        return ""

    def _scan_ip(self):
        request_url = self._api_url + 'ip-address/report?'
        parameters = {'ip': self._dst_ip, 'apikey': self._api_key}
        encoded_params = urllib.urlencode(parameters)
        full_url = request_url + encoded_params
        try:
            response = urllib.urlopen(full_url).read()
            json_response = json.loads(response)

            if json_response['response_code'] == 0:
                return ""
            else:
                return json_response
        except Exception, e:
            return ""



conn = ("AC10010C",
        "172.16.1.12",
        "1234",
        "08080808",
        "80",
        "tcp")