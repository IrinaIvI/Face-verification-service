from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, Table, ARRAY, Numeric, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry
from app.database import engine

mapper_registry = registry()

metadata = MetaData(schema="ivashko_schema")
Base = declarative_base(metadata=metadata)

class UserFaceData(Base):
    __tablename__ = "userfacedata_ivashko"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('ivashko_schema.users_ivashko.id'))
    vector = Column(ARRAY(Numeric(8, 7)), nullable=False)
    created_at = Column(TIMESTAMP, default=None)
    updated_at = Column(TIMESTAMP, default=None)

users_table = Table('users_ivashko', Base.metadata, autoload_with=engine, schema='ivashko_schema')

class Users:
    pass

mapper_registry.map_imperatively(Users, users_table)
