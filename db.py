from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import List, Optional

Base = declarative_base()


class Operation(Base):
    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    title = Column(String)
    description = Column(String)
    amount = Column(Float)
    currency = Column(String)
    image_url = Column(String)
    card_number = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    card_number = Column(String)
    balance = Column(Float)


class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    transfer = Column(Float)
    spending = Column(Float)
    enemy = Column(String)


class Database:
    def __init__(self, db_name: str = "finance"):
        self.engine = create_engine(f"sqlite:///{db_name}.db")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def insert_operation(self, operation: Operation):
        self.session.add(operation)
        card = self.session.query(Card).filter(Card.id == 1).first()
        if card:
            card.balance = card.balance - float(operation.amount)
        self.session.commit()

    def get_history(self) -> List[Operation]:
        return self.session.query(Operation).all()

    def insert_card(self, card: Card):
        self.session.add(card)
        self.session.commit()

    def update_settings(self, settings: Settings):
        existing_settings = self.session.query(Settings).first()
        if existing_settings:
            existing_settings.transfer = settings.transfer
            existing_settings.spending = settings.spending
        else:
            self.session.add(settings)
        self.session.commit()

    def get_settings(self) -> Optional[Settings]:
        s = self.session.query(Settings).first()
        if not s:
            s = self.session.add(Settings(transfer=5463524.3241, spending=5463524.3241 + 45642.123))
            self.session.commit()
        return s

    def get_card(self, id):
        if len(self.session.query(Card).all()) == 0:
            self.session.add(Card(id=1, card_number='220025489471242', balance=34512341.342))
            self.session.commit()
        card = self.session.query(Card).filter(Card.id == id).first()
        return card

    def get_card_balance(self, id: int) -> Optional[float]:
        if len(self.session.query(Card).all()) == 0:
            self.session.add(Card(id=1, card_number='220025489471242', balance=34512341.342))
            self.session.commit()
        card = self.session.query(Card).filter(Card.id == id).first()
        return card.balance if card else 0
