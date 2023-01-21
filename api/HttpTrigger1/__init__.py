
from sqlalchemy import create_engine
import json
import os
import pandas as pd
import psycopg2
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        ENV = req.params.get('ENV')
        conn_str = os.environ[f'CONN_STR_{ENV}'] 
        engine = create_engine(conn_str, echo=False)
        engine.connect()
        sql = f'''select * from employees;'''
        result = engine.execute(sql)
        result_list = [n for n in result]
        df = pd.DataFrame(result_list, columns=list(result.keys()))
        records_json = json.loads(df.to_json(orient='records'))
        return func.HttpResponse(str(records_json))
    except Exception as e:
        print(e)
        return func.HttpResponse(str(e), status_code=500)
