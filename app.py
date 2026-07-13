import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
h1 {
    color: #1f4e79;
}
h2 {
    color: #1f4e79;
}
[data-testid="stMetric"] {
    background-color: white;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
}

.stButton button {
    background-color: #1f77b4;
    color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)
df = pd.read_csv("train.csv")
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d/%m/%Y"
)

st.sidebar.title("📊 Sales Intelligence")
page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Overview",
        "🔮 Forecast Explorer",
        "⚠️ Anomaly Report",
        "📦 Product Segments"
    ]
)

if page == "🏠 Overview":
    st.title("📈 Sales Overview Dashboard")

    total_sales = df["Sales"].sum()
    total_orders = df["Order ID"].nunique()
    categories = df["Category"].nunique()
    regions = df["Region"].nunique()

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("💰 Total Sales",f"{total_sales:,.0f}")
    c2.metric("🛒 Orders",total_orders)
    c3.metric("📂 Categories",categories)
    c4.metric("🌎 Regions",regions)

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
        title="Yearly Sales",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="year"
    )

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
        title="Monthly Sales Trend",
        markers=True
    )


    st.plotly_chart(
        fig2,
        use_container_width=True,
        key="month"
    )
    col1,col2 = st.columns(2)
    with col1:

        region_sales = (
            df.groupby("Region")
            ["Sales"]
            .sum()
            .reset_index()
        )

        fig3 = px.pie(
            region_sales,
            names="Region",
            values="Sales",
            title="Sales by Region"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True,
            key="region"
        )

    with col2:
        cat_sales = (
            df.groupby("Category")
            ["Sales"]
            .sum()
            .reset_index()
        )
        fig4 = px.pie(
            cat_sales,
            names="Category",
            values="Sales",
            title="Sales by Category"
        )
        st.plotly_chart(
            fig4,
            use_container_width=True,
            key="category"
        )

elif page == "🔮 Forecast Explorer":
    st.title("🔮 Forecast Explorer")
    months = st.slider(
        "Forecast Months",
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
    st.success(
        "Best Model: SARIMA"
    )
    s1,s2 = st.columns(2)
        st.metric("MAE", f"{mae:.2f}")
        st.metric("RMSE", f"{rmse:.2f}")
elif page == "⚠️ Anomaly Report":
    st.title("⚠️ Sales Anomaly Detection")
    anomalies = pd.read_csv("anomaly_results.csv")
    anomalies["Order Date"] = pd.to_datetime(anomalies["Order Date"])
    fig = px.scatter(
        anomalies,
        x="Order Date",
        y="Sales",
        color="Isolation_Result",
        title="Detected Sales Anomalies"
    )
    st.plotly_chart(
        fig,
        use_container_width=True,
        key="anomaly"
    )
    st.dataframe(anomalies)

elif page == "📦 Product Segments":
    st.title("📦 Product Demand Segmentation")
    clusters = pd.read_csv("cluster_results.csv")
    fig = px.scatter(
        clusters,
        x="PCA1",
        y="PCA2",
        color="Demand_Group",
        hover_name="Sub-Category",
        title="Product Demand Clusters"
    )
    st.plotly_chart(
        fig,
        use_container_width=True,
        key="clusters"
    )
    st.subheader("Sub-category Groups")
    st.dataframe(
        clusters[
            [
                "Sub-Category",
                "Demand_Group"
            ]
        ]
    )
