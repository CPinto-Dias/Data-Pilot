from decimal import Decimal
import pandas as pd

def completed_orders(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["status"] == "concluido"].copy()

def total_revenue(df: pd.DataFrame) -> Decimal:
    validos = completed_orders(df)
    return Decimal(df["receita"].sum())

def total_orders(df: pd.DataFrame) -> int:
    return completed_orders(df)["pedido_id"].nunique()

def products_sold(df: pd.DataFrame) -> int:
    return completed_orders(df)["quantidade"].sum()

def unique_clients(df: pd.DataFrame) -> int:
    return completed_orders(df)["cliente_id"].nunique()

def average_ticket_value(df: pd.DataFrame) -> Decimal:
    orders = total_orders(df)
    if orders == 0:
        return Decimal(0)
    return total_revenue(df) / orders

def cancellation_rate(df: pd.DataFrame) -> float:
    total = df["pedido_id"].nunique()
    canceled = df.loc[df["status"] == "cancelado"]["pedido_id"].nunique()
    return (canceled / total * 100)if total > 0 else 0.0

def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    validos = completed_orders(df)
    return validos.groupby("mes", as_index=False)["receita"].sum().sort_values(by="mes")

def top5_clients(df: pd.DataFrame) -> pd.DataFrame:
    validos = completed_orders(df)
    return validos.groupby("cliente_id", as_index=False)["receita"].sum().sort_values(by="receita", ascending=False).head(5)       

def top5_products(df: pd.DataFrame) -> pd.DataFrame:
    validos = completed_orders(df)
    return validos.groupby("produto", as_index=False)["receita"].sum().sort_values(by="receita", ascending=False).head(5)