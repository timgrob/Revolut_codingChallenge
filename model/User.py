from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True)
    created_date = Column(DateTime, nullable=False)
    has_email = Column(String(255), nullable=False)
    phone_country = Column(String(300))
    terms_version = Column(Date)
    country = Column(String(2))
    state = Column(String(25), nullable=False)
    birth_year = Column(Integer)
    kyc = Column(String(20))
    failed_sign_in_attempts = Column(Integer)
    is_fraudster = Column(Boolean, nullable=False, default=False)
    # transactions = relationship("Transaction")

    def __init__(self, uuid, created_date, has_email, phone_country, terms_version, country, state, birth_year, kyc, failed_sign_in_attempts, is_fraudster):
        self.id = uuid
        self.created_date = created_date
        self.has_email = has_email
        self.phone_country = phone_country
        self.terms_version = terms_version
        self.country = country
        self.state = state
        self.birth_year = birth_year
        self.kyc = kyc
        self.failed_sign_in_attempts = failed_sign_in_attempts
        self.is_fraudster = is_fraudster
