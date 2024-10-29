import os
import dotenv
from sqlalchemy import create_engine

def database_connection_url():
    dotenv.load_dotenv()

    return os.environ.get("POSTGRES_URI")
#Remember to uncomment this in order to work with render and supabase
#engine = create_engine(database_connection_url(), pool_pre_ping=True)

