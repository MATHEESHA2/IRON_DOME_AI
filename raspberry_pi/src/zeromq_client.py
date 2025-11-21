import zmq, json
class ZMQClient:
    def __init__(self, server_addr='tcp://127.0.0.1:5555'):
        self.ctx = zmq.Context()
        self.sock = self.ctx.socket(zmq.REQ)
        self.sock.connect(server_addr)

    async def send_frame(self, frame_bytes, metadata=None):
        meta = metadata or {}
        self.sock.send_multipart([json.dumps(meta).encode('utf-8'), frame_bytes])
        resp = self.sock.recv()
        try:
            return json.loads(resp.decode('utf-8'))
        except Exception:
            return {}
