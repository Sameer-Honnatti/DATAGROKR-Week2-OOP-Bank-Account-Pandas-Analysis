import pandas as pd
import numpy as np

class BankDataAnalyzer:
    def __init__(self, customers_file, transactions_file):
        self.customers_file = customers_file
        self.transactions_file = transactions_file
        self.customers = pd.read_csv(customers_file)
        self.transactions = pd.read_csv(transactions_file)
        self.merged_data = pd.DataFrame()

    def merge_data(self):
        self.merged_data = pd.merge(
            self.transactions,
            self.customers,
            on="customer_id",
            how="inner"
        )
        return self.merged_data

    def transaction_summary(self):
        if self.merged_data.empty:
            self.merge_data()

        summary = self.merged_data.groupby(
            "transaction_type"
        )["amount"].agg(["count", "sum", "mean"]).reset_index()

        return summary

    def customer_summary(self):
        if self.merged_data.empty:
            self.merge_data()

        summary = self.merged_data.groupby(
            ["customer_id", "customer_name"]
        )["amount"].agg(["count", "sum", "mean"]).reset_index()

        return summary

    def branch_summary(self):
        if self.merged_data.empty:
            self.merge_data()

        return self.merged_data.groupby(
            "branch"
        )["amount"].sum().reset_index()

    def numpy_statistics(self):
        amounts = self.transactions["amount"].to_numpy()

        return {
            "total": np.sum(amounts),
            "average": np.mean(amounts),
            "maximum": np.max(amounts),
            "minimum": np.min(amounts),
            "standard_deviation": np.std(amounts)
        }

    def high_value_transactions(self, threshold=50000):
        filtered = self.transactions[
            self.transactions["amount"] > threshold
        ]

        return filtered

    def transformed_amounts(self):
        amounts = self.transactions["amount"].tolist()

        doubled = list(map(lambda x: x * 2, amounts))

        return doubled

    def filtered_customers(self):
        records = self.customer_summary().to_dict("records")

        high_value = list(
            filter(lambda record: record["sum"] > 50000, records)
        )

        return high_value

    def account_type_statistics(self):
        if self.merged_data.empty:
            self.merge_data()

        account_totals = self.merged_data.groupby(
            "account_type"
        )["amount"].sum().to_dict()

        return {
            account_type: round(total, 2)
            for account_type, total in account_totals.items()
        }

    def top_customers(self, count=5):
        summary = self.customer_summary()

        summary = summary.sort_values(
            by="sum",
            ascending=False
        )

        return summary.head(count)

    def sorted_transactions(self):
        records = self.transactions.to_dict("records")

        return sorted(
            records,
            key=lambda record: record["amount"],
            reverse=True
        )