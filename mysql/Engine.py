from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/stg?charset=utf8mb4"
# DATABASE_URL = "mysql+pymysql://avnadmin:AVNS_eJJurApFvKL2ETNLHsN@mysql-black-jack-black-jack-21.f.aivencloud.com:12039/stg?ssl-mode=REQUIRED"

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
