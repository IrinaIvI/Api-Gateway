from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

metadata = MetaData(schema="ivashko_schema")
Base = declarative_base(metadata=metadata)
