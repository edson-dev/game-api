from replit import db
import dataset

db['edson'] = {"test": "success"}

repository = dataset.connect("postgresql://elyybwtxwkqoea:61fb5e9b9a37a1939817e6acd3d99d266280074da917d797782de2c53f2d5eb0@ec2-54-156-151-232.compute-1.amazonaws.com:5432/dd5ndqsfuf0s5j")

def init_app(app, access_point="/api",encoding='utf-8'):
  @app.get(access_point + "/", tags=[access_point])
  async def get_table_itens():
        return db