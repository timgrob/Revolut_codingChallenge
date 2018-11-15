from sqlalchemy import Column, Integer, String, Boolean

from base import Base

class CurrencyDetails(Base):
    __tablename__ = 'currency_details'

    ccy = Column(String(10), primary_key=True)
    iso_code = Column(Integer)
    exponent = Column(Integer)
    is_crypto = Column(Boolean, nullable=False)

    def __init__(self,ccy,iso_code,exponent,is_crypto):
        self.ccy = ccy
        self.iso_code = iso_code
        self.exponent = exponent
        self.is_crypto = is_crypto