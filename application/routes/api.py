from replit import db
import dataset
from dotenv import load_dotenv
import os
from fastapi import UploadFile, File, Request

load_dotenv()
db = {}
db['edson'] = {"test": "success"}

repository = dataset.connect(os.getenv("POSTGRESQL"))


def init_app(app, access_point="/api", encoding='utf-8'):
  @app.get(access_point + "/", tags=[access_point])
  async def get_table_itens():
        return db

  @app.get(access_point + "/{name}/create_table", tags=[access_point])
  async def create_table(name: str):
      # define table attributes
      if not repository[name].exists:
          table = repository.create_table(name,
                                  primary_id='id',
                                  primary_type=repository.types.integer)
          repository.commit()
      else:
          table = repository[name]
      return list(table.all())

  @app.get(access_point + "/{name}/delete_table", tags=[access_point])
  async def delete_table(name: str):
      # define table attributes
      if repository[name].exists:
          table = repository[name]
          table.drop()
      return {"success": "true"}


  @app.get(access_point + "/{name}", tags=[access_point])
  async def get_itens(name: str):
      table = repository[name]
      return list(table.all())

  @app.post(access_point + "/{name}", tags=[access_point])
  async def insert_itens(name: str, request: Request):
      table = repository[name]
      try:
          table.insert(dict(await request.json()))
      except:
          ...
      return list(table.all())

  @app.put(access_point + "/{name}", tags=[access_point])
  async def upsert_itens(name: str, request: Request):
      table = repository[name]
      table.update(dict(await request.json()), ['id'])
      return list(table.all())

  @app.delete(access_point + "/{name}", tags=[access_point])
  async def delete_itens(name: str, request: Request):
      table = repository[name]
      clause = dict(await request.json())
      table.delete(id=clause['id'])
      return list(table.all())
