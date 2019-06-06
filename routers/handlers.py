import tornado.web


class MainHandler(tornado.web.RequestHandler):
    # standalone = True
    # lookup_field = "id"
    # lookup_value = "\d+"
    # lookup_url_kwargs = ("cid", "pid")
    # lookup_value_regexs = ("\d+", "\S+")
    def initialize(self, **kwargs):
        mapping = kwargs.get("mapping")
        if mapping:
            for method, action in mapping.items():
                handler = getattr(self, action)
                setattr(self, method, handler)

    # def initialize(self, mapping):
    # for method, action in mapping.items():
    # handler = getattr(self, action)
    # setattr(self, method, handler)

    # def list(self, cluster_pk):
        # self.write("list")

    def retrieve(self, cluster_id, pod_id):
        self.write("retrieve")

    def create(self, cluster_pk):
        self.write("create")

    def update(self, cluster_pk, pod_pk):
        self.write("update")

    def partial_update(self, cluster_pk, pod_pk):
        self.write("partial_update")

    def destroy(self, cluster_pk, pod_pk):
        self.write("destory")
