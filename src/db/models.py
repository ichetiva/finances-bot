from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String, DateTime, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    wallets = relationship(
        "Wallet",
        order_by="desc(Wallet.balance)",
        primaryjoin="User.id == Wallet.user_id",
    )


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    name = Column(String(100))
    balance = Column(Float, default=0)
    currency = Column(String(10))
    transactions = relationship(
        "Transaction",
        order_by="desc(Transaction.created_at)",
        primaryjoin="Transaction.wallet_id == Wallet.id",
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    value = Column(Float, nullable=False)
    comment = Column(String(500), default=None)
    created_at = Column(DateTime, default=func.now())
