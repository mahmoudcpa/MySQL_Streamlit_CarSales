import random

def generate_insights(df):
    if not df.empty:
        best_selling_model = df.groupby("model")["total_sales"].sum().idxmax()
        total = df["total_sales"].sum()
        avg_order = df["total_sales"].mean()

        insights = [
            f"Grand Total Sales: LE{total:,.0f}",
            f"Best-selling Model: {best_selling_model}",
            f"Average Order Value: LE{avg_order:,.0f}"
        ]
        return random.choice(insights)
    return "No data available"
