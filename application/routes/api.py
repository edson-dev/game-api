from replit import db
import dataset

db['edson'] = {"test": "success"}


def init_app(app, access_point="/api",encoding='utf-8'):
  @app.get(access_point + "/", tags=[access_point])
  async def get_table_itens():
        return db