import streamlit as st
import pandas as pd

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="Social Media Engagement Dashboard",
    layout="wide"
)

# ----------------------------
# Load dataset
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("social_media_3platforms_3years.csv")

    # Date processing
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["hour"] = df["date"].dt.hour   # for optimal posting time

    # Engagement calculation
    df["engagement"] = df["likes"] + df["comments"] + df["shares"]

    # Campaign cost (assumed)
    df["campaign_cost"] = 5000

    # Campaign ROI calculation
    df["roi"] = ((df["engagement"] - df["campaign_cost"]) / df["campaign_cost"]) * 100

    return df

df = load_data()

# ----------------------------
# Dashboard title
# ----------------------------
st.title("📊 Social Media Engagement Analytics Dashboard")
st.write("Analyze social media performance using Year and Month filters.")

# ----------------------------
# User input controls
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    selected_year = st.selectbox(
        "Select Year",
        sorted(df["year"].unique())
    )

with col2:
    selected_month = st.selectbox(
        "Select Month",
        sorted(df["month"].unique())
    )

# ----------------------------
# Filter data
# ----------------------------
filtered_df = df[
    (df["year"] == selected_year) &
    (df["month"] == selected_month)
]

if filtered_df.empty:
    st.warning("No data available for the selected year and month.")
    st.stop()

# ----------------------------
# Calculations
# ----------------------------
top_platform_views = (
    filtered_df.groupby("platform")["views"]
    .sum()
    .idxmax()
)

top_platform_engagement = (
    filtered_df.groupby("platform")["engagement"]
    .sum()
    .idxmax()
)

top_content_views = (
    filtered_df.groupby("content_type")["views"]
    .sum()
    .idxmax()
)

top_content_engagement = (
    filtered_df.groupby("content_type")["engagement"]
    .sum()
    .idxmax()
)

best_roi_platform = (
    filtered_df.groupby("platform")["roi"]
    .mean()
    .idxmax()
)

# Optimal Posting Time (Hour with highest engagement)
optimal_posting_hour = (
    filtered_df.groupby("hour")["engagement"]
    .mean()
    .idxmax()
)

# ----------------------------
# KPI display
# ----------------------------
st.subheader("🔍 Key Insights")

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

kpi1.metric("📈 Most Viewed Platform", top_platform_views)
kpi2.metric("🔥 Most Engaged Platform", top_platform_engagement)
kpi3.metric("🎥 Most Viewed Content", top_content_views)
kpi4.metric("💬 Most Engaged Content", top_content_engagement)
kpi5.metric("💰 Best ROI Platform", best_roi_platform)
kpi6.metric("⏰ Optimal Posting Hour", f"{optimal_posting_hour}:00")

# ----------------------------
# Charts
# ----------------------------
st.subheader("📊 Visual Analysis")

col3, col4 = st.columns(2)

with col3:
    st.write("Views by Platform")
    st.bar_chart(
        filtered_df.groupby("platform")["views"].sum()
    )

with col4:
    st.write("Engagement by Content Type")
    st.bar_chart(
        filtered_df.groupby("content_type")["engagement"].sum()
    )

st.write("📉 Average Campaign ROI by Platform")
st.bar_chart(
    filtered_df.groupby("platform")["roi"].mean()
)

st.write("⏰ Engagement by Posting Hour")
st.bar_chart(
    filtered_df.groupby("hour")["engagement"].mean()
)

# ----------------------------
# Data table
# ----------------------------
with st.expander("📄 View Filtered Data"):
    st.dataframe(filtered_df)
