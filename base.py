from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from configs import settings

engine = create_engine(settings.DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def generateDatabaseSchema():
    from model import User
    from model import Transaction
    from model import FxRates
    from model import CurrencyDetails
    Base.metadata.create_all(engine)