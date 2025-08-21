# generate_dataset.py
import pandas as pd
import numpy as np
import argparse

def generate_csv(n_products=200, out_file="products.csv"):
    np.random.seed(42)
    products = [f"Product_{i}" for i in range(1, n_products + 1)]
    demand_per_day = np.random.randint(20, 500, size=n_products)
    lead_time_days = np.random.randint(1, 30, size=n_products)
    safety_stock = np.random.randint(10, 200, size=n_products)
    holding_cost = np.round(np.random.uniform(0.5, 5.0, size=n_products), 2)
    order_cost = np.random.randint(100, 1500, size=n_products)

    df = pd.DataFrame({
        "Product": products,
        "Demand_per_day": demand_per_day,
        "Lead_time_days": lead_time_days,
        "Safety_stock": safety_stock,
        "Holding_cost_per_unit": holding_cost,
        "Order_cost": order_cost
    })

    df.to_csv(out_file, index=False)
    print(f"✅ Dataset generated: {out_file} with {n_products} products")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate products.csv")
    parser.add_argument("--n", type=int, default=200, help="Number of products")
    parser.add_argument("--out", type=str, default="products.csv", help="Output CSV filename")
    args = parser.parse_args()
    generate_csv(args.n, args.out)