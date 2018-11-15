from sqlalchemy import Column, String, DateTime, Float

from base import Base


class FxRates(Base):
    __tablename__ = 'fx_rates'

    id = Column(String(50), primary_key=True)
    ts = Column(DateTime)
    base_ccy = Column(String(3))
    ccy = Column(String(10))
    rate = Column(Float)

    def __init__(self,ts,base_ccy,ccy,rate):
        self.id = '{}-{}-{}'.format(base_ccy,ccy,ts)
        self.ts = ts
        self.base_ccy = base_ccy
        self.ccy = ccy
        self.rate = rate
