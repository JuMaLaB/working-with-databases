from typing import List

from sqlalchemy import String, Numeric, create_engine, select, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship

class Base(DeclarativeBase):
    pass
    
class Investment(Base):
    __tablename__ = "investment"

    id: Mapped[int] = mapped_column(primary_key=True)
    coin: Mapped[str] = mapped_column(String(32))
    currency: Mapped[str] = mapped_column(String(3))
    amount: Mapped[float] = mapped_column(Numeric(5, 2))

    # adding the FK and porps to relationship to access it directly
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolio.id"))
    portfolio: Mapped["Portfolio"] = relationship(back_populates="investments")

    def __repr__(self) -> str:
        return f"<Investment coin: {self.coin}, currency: {self.currency}, amount: {self.amount}>"

class Portfolio(Base):
    __tablename__ = "portfolio"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text())

    # adding porps to relationship to access it directly
    investments: Mapped[List["Investment"]] = relationship(back_populates="portfolio")

    def __repr__(self) -> str:
        return f"<Portfolio name: {self.name} with {len(self.investments)} investment(s)>"
    
engine = create_engine("sqlite:///relationships.db")
Base.metadata.create_all(engine)

bitcoin = Investment(coin="bitcoin",currency="eur",amount=1.0)
ethereum = Investment(coin="ethereum",currency="usd",amount=10.0)
solana = Investment(coin="solana",currency="gbp",amount=100.0)
dogecoin = Investment(coin="dogecoin",currency="eur",amount=66.0)

portfilio_1 = Portfolio(name="Portfolio 1", description="Description 1")
bitcoin.portfolio = portfilio_1

portfilio_2 = Portfolio(name="Portfolio 2", description="Description 2")
portfilio_2.investments.extend([ethereum, solana, dogecoin])

portfilio_3 = Portfolio(name="Portfolio 3", description="Description 3")
bitcoin_2 = Investment(coin="bitcoin",currency="eur",amount=12.0)
bitcoin_2.portfolio = portfilio_3

# session will be destroy after with statement is finish
with Session(engine) as session:
    #session.add(bitcoin)
    #session.commit()

    #session.add(portfilio_2)
    #session.commit()

    portfolio = session.get(Portfolio, 2)
    print(portfolio)
    for investment in portfolio.investments:
        print(investment)
    
    print(" -------------------- ")

    investment = session.get(Investment, 1)
    print(investment)
    print(investment.portfolio)

    print(" ---------- stmt ---------- ")

    stmt = select(Investment).join(Portfolio)
    print(stmt)

    print(" ---------- subq ---------- ")

    #session.add(bitcoin_2)
    #session.commit()

    subq = select(Investment).where(Investment.coin == "bitcoin").subquery()
    # c = column of the subq
    stmt = select(Portfolio).join(subq, Portfolio.id == subq.c.portfolio_id)
    print(stmt)

    """ 
    SELECT portfolio.id, portfolio.name, portfolio.description FROM portfolio 
    JOIN (
        SELECT 
            investment.id AS id,
            investment.coin AS coin,
            investment.currency AS currency,
            investment.amount AS amount, 
            investment.portfolio_id AS portfolio_id
        FROM investment
        WHERE investment.coin = :coin_1) AS anon_1 
    ON portfolio.id = anon_1.portfolio_id 
    """

    portfolios = session.execute(stmt).scalars().all()
    print(portfolios)