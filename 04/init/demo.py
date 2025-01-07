from sqlalchemy import String, Numeric, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Portfolio(Base):
    __tablename__ = "portfolio"
    id: Mapped[int] = mapped_column(primary_key=True)
    coin: Mapped[str] = mapped_column(String(32))
    currency: Mapped[str] = mapped_column(String(3))
    amount: Mapped[float] = mapped_column(Numeric(5,2))

    def __repr__(self) -> str:
        return f"<Portfolio coin: {self.coin} - currency: {self.currency} - amount: {self.amount}>"


engine = create_engine("sqlite:///portfolio.db")
Base.metadata.create_all(engine)

bitcoin = Portfolio(coin="bitcoin",currency="eur",amount=1.0)
ethereum = Portfolio(coin="ethereum",currency="usd",amount=10.0)
solana = Portfolio(coin="solana",currency="gbp",amount=100.0)
dogecoin = Portfolio(coin="dogecoin",currency="eur",amount=66.0)

# session will be destroy after with statement is finish
with Session(engine) as session:
    # session.add(bitcoin)
    # session.add_all([ethereum,solana,dogecoin])
    # session.commit()

    stmt = select(Portfolio).where(Portfolio.coin == "bitcoin")
    # because there is only one statment return
    coin = session.execute(stmt).scalar_one()
    #print(f"{coin.coin} - {coin.currency} - {coin.amount}")
    print(coin)
    
    # get data by Id
    coin = session.get(Portfolio, 2)
    print(coin)

    stmt_where = select(Portfolio).where(Portfolio.amount > 55)
    coins = session.execute(stmt_where).scalars().all()
    for coin in coins:
        print(coin)