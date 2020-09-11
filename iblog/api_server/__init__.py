import threading

from iblog import target
from iblog.api_server.api import register_api


class ApiServer(threading.Thread):
    def __init__(self, host='0.0.0.0', port=8080, debug=False):
        super().__init__()
        self.host = host
        self.port = port
        self.debug = debug
        from flask import Flask
        app = Flask(__name__)
        app.config['issue_config'] = {
            'targets': target.targets
        }
        self.app = app
        register_api(self.app)

    def run(self):
        # 中可以接受两个参数，分别是threaded=True和processes=1，用于开启线程支持和进程支持。
        self.app.run(host=self.host, port=self.port, debug=self.debug)
