from interfaces.repository_interface import RepositoryInterface


class RepositoryNOSQL(RepositoryInterface):
    def __init__(self, app, access_point="/repository"):
        self.init_app(app, access_point)

    def init_app(self, app, access_point="/repository"):
        @app.get(access_point, tags=[access_point])
        def read_root():
            return {"Hello": "World"}

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
