import unittest
import base64
import json

class testBase(unittest.TestCase):
    def test_base64_encode(self):
        param_dict = {
            "host": "172.16.165.131",
            "port": "5901"
        }

        json_str = json.dumps(param_dict)

        print base64.encodestring(json_str)


    # def test_decode(self):
    #     encode_str = "eyJob3N0IjogIjE3Mi4xNi4xNjUuMTMxIiwgInBvcnQiOiAiNTkwMSJ9"
    #
    #     decode_str = base64.decodestring(encode_str)
    #
    #     param_dict = json.loads(decode_str)
    #
    #     print param_dict.__dict__