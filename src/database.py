import os
import dotenv
from sqlalchemy import create_engine


def database_connection_url():
    dotenv.load_dotenv()

    postgres_uri = os.environ.get("POSTGRES_URI")
    if postgres_uri is None:
        raise RuntimeError("No Postgres URI key provided")

    return postgres_uri


engine = create_engine(database_connection_url(), pool_pre_ping=True)
