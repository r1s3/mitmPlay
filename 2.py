__author__ = 'silex'
#!/usr/bin/env python
"""
This example builds on mitmproxy's base proxying infrastructure to
implement functionality similar to the "sticky cookies" option.

Heads Up: In the majority of cases, you want to use inline scripts.
"""
import os
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer


class StickyMaster(controller.Master):
    def __init__(self, server):
        controller.Master.__init__(self, server)
        self.stickyhosts = {}

    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_request(self, flow):
        hid = (flow.request.host, flow.request.port)
        print hid
        if flow.request.headers["cookie"]:
            self.stickyhosts[hid] = flow.request.headers["cookie"]
        elif hid in self.stickyhosts:
            flow.request.headers["cookie"] = self.stickyhosts[hid]
        flow.reply()

    def handle_response(self, flow):
        hid = (flow.request.host, flow.request.port)

        if flow.response.headers["set-cookie"]:
            self.stickyhosts[hid] = flow.response.headers["set-cookie"]
        # flow.reply()
        print(flow.response.headers)
        print(flow.response.msg)
        print(flow.response.code)
        print(flow.response.get_state())
        print(flow.response.content)
        s2 = "mawa"
        flow.response.content = s2
        print "==========================="
        print(flow.response.content)
        flow.reply

config = proxy.ProxyConfig(port=8080)
server = ProxyServer(config)
m = StickyMaster(server)
m.run()