import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://admin:admin123@localhost:5432/lab"
)

df = pd.read_sql(
    "SELECT * FROM vendas",
    engine
)

print(df)

df.to_parquet(
    "data/processed/vendas.parquet",
    index=False
)

print("Arquivo data/processed/vendas.parquet criado!")