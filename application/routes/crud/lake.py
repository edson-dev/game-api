from fastapi import APIRouter, FastAPI, Request
from routes.interfaces.crud import CRUD
import json
import pandas
import duckdb
class Lake(CRUD):
    def __init__(self, app: FastAPI, repository, access_point="crud", dependencies=None):
        self.router = APIRouter()
        self.init_app(self.router, repository)
        app.include_router(prefix=f"/{access_point}",
                           router=self.router,
                           tags=[access_point],
                           dependencies=dependencies)


    def init_app(self, router, repository):
        @router.get("/{schema}")
        async def describe(schema: str, table: str):
            duckdb.connect('.db').sql(f'CREATE SCHEMA {schema}')

        @router.get("/{schema}/{table}")
        async def read_all(schema: str, table: str, query: str = '', offset: int = 0, limit: int = 10):
            with duckdb.connect('.db') as connection:
                result = connection.sql(
                    f"FROM {schema}.{table} {f'WHERE {query}' if query else ''} LIMIT {limit} OFFSET {offset}").execute()
                return json.loads(result.fetchdf().to_json(orient='records', date_format='iso'))

        @router.get("/{schema}/{table}/{id}")
        async def read_one(schema: str, table: str,id , query: str = '', skip: int = 0, limit: int = 10):
            query = query+f"id={id}"
            with duckdb.connect('.db') as connection:
                result = connection.sql(
                    f"FROM {schema}.{table} {f'WHERE {query}' if query else ''} LIMIT {limit} OFFSET {skip}").execute()
                return json.loads(result.fetchdf().to_json(orient='records', date_format='iso'))


        @router.post("/{schema}/{table}")
        async def create(request: Request, schema: str, table: str):
            itens = await request.json()
            with duckdb.connect('.db') as connection:
                for i in itens:
                    q=f"INSERT INTO {schema}.{table}({','.join(i.keys())}) VALUES ({','.join(i.values())})"
                    result = connection.sql(q)
                    return ''

        @router.post("/{schema}/{table}/{id}")
        @router.patch("/{schema}/{table}/{id}")
        @router.put("/{schema}/{table}/{id}")
        async def update(request: Request, schema: str, table: str,id):
            itens = await request.json()
            with duckdb.connect('.db') as connection:
                for i in itens:
                    q = f"UPDATE {schema}.{table} SET {','.join([f'{str(i)}={str(j)}' for i, j in zip(i.keys(),i.values())])} WHERE id={id}"
                    result = connection.sql(q)
                    return ''
        @router.delete("/{schema}/{table}")
        async def delete(schema: str, table: str, query: str = ''):
            with duckdb.connect('.db') as connection:
                result = connection.sql(f"DELETE FROM {schema}.{table} {f'WHERE {query}' if query else ''}")
                return ""

        @router.put("/{schema}/{table}")
        async def insert_many(request: Request, schema: str, table: str):
            itens = await request.json()
            df_in = pandas.DataFrame(itens)
            with duckdb.connect('.db') as connection:
                df = connection.sql(f"FROM {schema}.{table}").df().duplicated(keep=False)
                delta = df_in[~df_in.isin(df)].dropna()
                result = connection.sql(f"INSERT INTO {schema}.{table} SELECT * FROM delta")
                return json.loads(delta.to_json(orient='records'))
        @router.patch("/{schema}/{table}")
        async def save(schema: str, table: str):
            q = f"""
                INSTALL httpfs;
                LOAD httpfs;
                SET s3_endpoint='storage.googleapis.com';
                COPY {schema}.{table} TO 's3://data-hub-393917/{schema}/{table}.parquet';
                """
            with duckdb.connect('.db') as connection:
                result = connection.sql(q)
                return ""


