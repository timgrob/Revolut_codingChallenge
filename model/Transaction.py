from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from base import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID, ForeignKey('users.id'))
    type = Column(String(20), nullable=False)
    source = Column(String(20), nullable=False)
    entry_method = Column(String(4), nullable=False)
    merchant_country = Column(String)
    merchant_category = Column(String(100))
    created_date = Column(DateTime, nullable=False)
    state = Column(String(25), nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String(3), nullable=False)

    def __init__(self,uuid,user_id,transactionType,source,entry_method,merchant_country,merchant_category,created_date,state,amount,currency):
        self.id = uuid
        self.user_id = user_id
        self.type = transactionType
        self.source = source
        self.entry_method = entry_method
        self.merchant_country = merchant_country
        self.merchant_category = merchant_category
        self.created_date = created_date
        self.state = state
        self.amount = amount
        self.currency = currency


