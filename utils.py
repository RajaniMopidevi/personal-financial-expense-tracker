import pandas as pd
import os

FILE_NAME = "expenses.csv"

def initialize_data():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
        df.to_csv(FILE_NAME, index=False)

def load_data():
    df = pd.read_csv(FILE_NAME)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.sort_values("Date", ascending=True).reset_index(drop=True)
    df["Date_display"] = df["Date"].dt.date
    return df


def add_expense(df, new_expense):
    new_expense["Date"] = pd.to_datetime(new_expense["Date"])
    df = pd.concat([df, pd.DataFrame([new_expense])], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)
    return df


def delete_expense(df, index):
    df = df.drop(index).reset_index(drop=True)
    df.to_csv(FILE_NAME, index=False)
    return df
