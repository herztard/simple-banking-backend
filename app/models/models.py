from sqlalchemy import (
    Column, Integer, String, DateTime, Numeric, ForeignKey
)

from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    accounts = relationship("Account", back_populates="users")


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    balance = Column(Numeric(12, 2), default=0)
    name = Column(String, nullable=False, default="Visa Card")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="accounts")

    sent_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.sender_account_id",
        back_populates="sender_account"
    )
    received_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.receiver_account_id",
        back_populates="receiver_account"
    )


class Card(Base):
    __tablename__ = "cards"

    card_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    name = Column(String, nullable=True)
    card_number = Column(String, nullable=False)
    expiry_date = Column(String, nullable=False)
    cvc = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expire_at = Column(DateTime, default=datetime.utcnow()+timedelta(days=1460))

    # If you want to relate a card to an account or user, you can add a ForeignKey
    # For example: account_id = Column(Integer, ForeignKey("accounts.account_id"))
    account = relationship("Account", back_populates="cards")


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    sender_account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    receiver_account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sender_account = relationship("Account", foreign_keys=[sender_account_id], back_populates="sent_transactions")
    receiver_account = relationship("Account", foreign_keys=[receiver_account_id], back_populates="received_transactions")
