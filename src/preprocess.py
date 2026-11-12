import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd

#=============================================
# Importing the dataset from CSV file
#=============================================

root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True) 

file_path = filedialog.askopenfilename(
    title="Selecione o arquivo CSV",
    filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
)

df = pd.read_csv(file_path)

print("--- Diagnóstico Inicial ---")
print(df.head())
print(df.shape)
print(df.dtypes)
print("-" * 30)

#=============================================
# Data treatment prior calculations
#=============================================

df["data"] = pd.to_datetime(df["data"], errors="coerce")

df["mes"] = df["data"].dt.to_period("M").astype(str)

df["status"] = df["status"].str.strip().str.lower()

df = df.drop_duplicates()

df["receita"] = df["quantidade"] * df["preco_unitario"]

#=============================================
# Treated Data export
#=============================================

os.makedirs("data_processed", exist_ok=True)

df.to_csv("data_processed/sales_clean.csv", index=False, decimal=",", sep=";")
print("\n[Sucesso] Arquivo 'sales_clean.csv' exportado com sucesso para a pasta 'data_processed'.")