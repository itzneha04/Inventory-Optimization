# inventory_optimization.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Config
INPUT_CSV = "products.csv"
OUTPUT_CSV = "inventory_results.csv"
OUTPUT_XLSX = "inventory_results.xlsx"

def load_and_compute(csv_path=INPUT_CSV):
    df = pd.read_csv(csv_path)
    # Annual demand
    df["Annual_Demand"] = df["Demand_per_day"] * 365
    # EOQ: sqrt((2 * Annual_Demand * Order_cost) / Holding_cost_per_unit)
    df["EOQ"] = np.sqrt((2 * df["Annual_Demand"] * df["Order_cost"]) / df["Holding_cost_per_unit"])
    # ROP: Demand_per_day * Lead_time_days + Safety_stock
    df["ROP"] = (df["Demand_per_day"] * df["Lead_time_days"]) + df["Safety_stock"]
    return df

def save_outputs(df):
    # CSV
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved CSV: {OUTPUT_CSV}")

    # Excel with a chart for Top 20 by Annual_Demand
    top20 = df.sort_values("Annual_Demand", ascending=False).head(20)
    with pd.ExcelWriter(OUTPUT_XLSX, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="All_Data", index=False)
        top20.to_excel(writer, sheet_name="Top20", index=False)

        workbook = writer.book
        worksheet = writer.sheets["Top20"]

        # Chart: EOQ vs ROP for top 20
        chart = workbook.add_chart({"type": "column"})
        # categories (Products): A2:A21
        categories = "=Top20!$A$2:$A$21"
        eoq_values = "=Top20!$H$2:$H$21"   # EOQ column (H)
        rop_values = "=Top20!$I$2:$I$21"   # ROP column (I)

        chart.add_series({"name": "EOQ", "categories": categories, "values": eoq_values})
        chart.add_series({"name": "ROP", "categories": categories, "values": rop_values})
        chart.set_title({"name": "EOQ vs ROP (Top 20 by Annual Demand)"})
        chart.set_x_axis({"name": "Product"})
        chart.set_y_axis({"name": "Units"})

        worksheet.insert_chart("K2", chart, {"x_scale": 1.5, "y_scale": 1.2})

    print(f"Saved Excel with chart: {OUTPUT_XLSX}")

def plot_top10(df):
    top10 = df.sort_values("Annual_Demand", ascending=False).head(10)
    x = np.arange(len(top10))
    width = 0.35
    plt.figure(figsize=(12,6))
    plt.bar(x - width/2, top10["EOQ"], width=width, label="EOQ")
    plt.bar(x + width/2, top10["ROP"], width=width, label="ROP")
    plt.xticks(x, top10["Product"], rotation=45, ha="right")
    plt.ylabel("Units")
    plt.title("EOQ vs ROP - Top 10 Products")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if not os.path.exists(INPUT_CSV):
        raise FileNotFoundError(f"{INPUT_CSV} not found. Run generate_dataset.py first.")
    df = load_and_compute(INPUT_CSV)
    # Display top results in terminal
    print(df[["Product", "Annual_Demand", "EOQ", "ROP"]].sort_values("Annual_Demand", ascending=False).head(10).to_string(index=False))
    # Save outputs
    save_outputs(df)
    # Show a quick plot
    plot_top10(df)