import pandas as pd
import os
import random
import streamlit as st

@st.cache_data
def load_data(file="products.csv"):
    try:
        # Case 1: If file does not exist
        if not os.path.exists(file):
            st.warning(f"⚠️ {file} not found. Generating sample dataset...")
            return generate_sample_data()

        # Try reading the file
        df = pd.read_csv(file)

        # Case 2: If file is empty
        if df.empty:
            st.warning(f"⚠️ {file} is empty. Generating sample dataset...")
            return generate_sample_data()

        return df

    except Exception as e:
        st.error(f"❌ Error reading {file}: {e}")
        st.info("Generating sample dataset instead...")
        return generate_sample_data()

def generate_sample_data(rows=1000):
    categories = ["Electronics", "Accessories", "Bags", "Furniture", "Clothing"]
    data = []

    for i in range(1, rows+1):
        data.append({
            "ProductID": i,
            "ProductName": f"Product_{i}",
            "Category": random.choice(categories),
            "Stock": random.randint(10, 500),
            "Price": round(random.uniform(100, 50000), 2)
        })

    df = pd.DataFrame(data)
    # Save so next time we don’t need to regenerate
    df.to_csv("products.csv", index=False)
    return df

# ---------------- Streamlit App ----------------
st.title("📦 Inventory Optimization Dashboard")

df = load_data("products.csv")
st.success(f"✅ Loaded {len(df)} products")

st.dataframe(df.head(20))