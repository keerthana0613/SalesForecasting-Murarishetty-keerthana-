import streamlit as st
import pandas as pd
import plotly.express as px


# Load data
df = pd.read_csv(
    "train.csv"
)

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d/%m/%Y"
)


# Sidebar
st.sidebar.title("Sales Analytics Dashboard")

page = st.sidebar.selectbox(
    "Select Page",
    [
        "Sales Overview",
        "Forecast Explorer",
        "Anomaly Report",
        "Product Demand Segments"
    ]
)


# ==========================
# PAGE 1: SALES OVERVIEW
# ==========================

if page == "Sales Overview":

    st.title("Sales Overview Dashboard")

    # Yearly sales
    yearly = (
        df.groupby(
            df["Order Date"].dt.year
        )["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        yearly,
        x="Order Date",
        y="Sales",
        title="Total Sales by Year"
    )

    st.plotly_chart(
        fig,
        key="yearly_sales_chart"
    )


    # Monthly sales trend
    monthly = (
        df.groupby(
            pd.Grouper(
                key="Order Date",
                freq="ME"
            )
        )["Sales"]
        .sum()
        .reset_index()
    )


    fig2 = px.line(
        monthly,
        x="Order Date",
        y="Sales",
        title="Monthly Sales Trend"
    )

    st.plotly_chart(
        fig2,
        key="monthly_sales_chart"
    )


    # Filters
    region = st.selectbox(
        "Select Region",
        df["Region"].unique()
    )

    category = st.selectbox(
        "Select Category",
        df["Category"].unique()
    )


    filtered = df[
        (df["Region"] == region) &
        (df["Category"] == category)
    ]

    st.write(
        "Sales:",
        filtered["Sales"].sum()
    )



# ==========================
# PAGE 2: FORECAST EXPLORER
# ==========================

elif page == "Forecast Explorer":

    st.title("Forecast Explorer")

    option = st.selectbox(
        "Select Forecast Type",
        ["Category", "Region"]
    )


    months = st.slider(
        "Forecast Horizon",
        1,
        3,
        3
    )


    forecast = pd.read_csv(
        "SARIMA_forecast_results.csv"
    )


    st.line_chart(
        forecast.head(months)
    )


    st.subheader(
        "Model Performance"
    )

    st.write(
        "MAE: Add your Task 3 MAE value"
    )

    st.write(
        "RMSE: Add your Task 3 RMSE value"
    )



# ==========================
# PAGE 3: ANOMALY REPORT
# ==========================

elif page == "Anomaly Report":

    st.title(
        "Sales Anomaly Report"
    )


    anomalies = pd.read_csv(
        "anomaly_results.csv"
    )


    anomalies["Order Date"] = pd.to_datetime(
        anomalies["Order Date"]
    )


    fig = px.scatter(
        anomalies,
        x="Order Date",
        y="Sales",
        title="Detected Sales Anomalies"
    )


    st.plotly_chart(
        fig,
        key="anomaly_chart"
    )


    st.subheader(
        "Anomaly Dates"
    )

    st.dataframe(
        anomalies
    )



# ==========================
# PAGE 4: PRODUCT SEGMENTS
# ==========================

elif page == "Product Demand Segments":

    st.title(
        "Product Demand Segmentation"
    )


    clusters = pd.read_csv(
        "cluster_results.csv"
    )


    st.dataframe(
        clusters.head()
    )


    if "PCA1" in clusters.columns and "PCA2" in clusters.columns:

        fig = px.scatter(
            clusters,
            x="PCA1",
            y="PCA2",
            color="Demand_Group",
            hover_name="Sub-Category",
            title="Product Clusters"
        )


        st.plotly_chart(
            fig,
            key="cluster_chart"
        )

    else:

        st.error(
            "PCA1 and PCA2 columns are missing in cluster_results.csv"
        )


    st.subheader(
        "Sub-category Cluster Table"
    )


    st.dataframe(
        clusters[
            [
                "Sub-Category",
                "Demand_Group"
            ]
        ]
    )
