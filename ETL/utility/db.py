from sqlalchemy import create_engine, text
import pandas

def open_conn(schema='three_ships'):
    engine = create_engine('postgresql+psycopg2://docker:postgres@localhost:5499/{0}'.format(schema), pool_recycle=3600, connect_args={'options': '-csearch_path=public'})
    return engine

def exec_sql(schema=None, cmd=None):
    engine = open_conn()
    with engine.connect() as conn:
        conn.execute(text('{0}'.format(cmd)))

def read_sql(cmd=None):
    engine = open_conn()
    query = text(cmd)
    df = pandas.read_sql_query(query,engine.connect())
    return df

def truncate_tbl(tbl=None):
    db.exec_sql(schema='public',cmd="truncate std_{};commit;".format(tbl))