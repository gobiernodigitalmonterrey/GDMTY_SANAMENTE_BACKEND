from google.cloud import redis_v1

class GoogleRedisClient:
    def __init__(self, host, port, password, project_id, credential_path=None):
        self.host = host
        self.port = port
        self.password = password
        self.project_id = project_id
        self.credential_path = credential_path
        self.redis_client = None

    def connect(self):
        if self.credential_path:
            client = redis_v1.CloudRedisClient.from_service_account_json(self.credential_path)
        else:
            client = redis_v1.CloudRedisClient()
        self.redis_client = redis_v1.Redis(host=self.host, port=self.port, password=self.password, client=client)

    def get_client(self):
        if not hasattr(self, 'redis_client'):
            self.connect()
        return self.redis_client