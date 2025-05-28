import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure page
st.set_page_config(
    page_title="RFM Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .st-emotion-cache-1v0mbdj {
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('rfm_clusters.csv')

rfm = load_data()

# Sidebar - Filters
st.sidebar.title("Filters")
selected_segment = st.sidebar.selectbox(
    "Customer Segment",
    options=rfm['Segment'].unique(),
    index=0
)

# Main content
st.title("Customer Segmentation Dashboard")
st.markdown("Analyzing customer behavior with RFM (Recency, Frequency, Monetary) metrics")

# Key metrics cards
st.header(f"Segment: {selected_segment}")
segment_data = rfm[rfm['Segment'] == selected_segment]

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.metric("Median Recency", f"{segment_data['Recency'].median():.0f} days", 
              help="Days since last purchase (lower is better)")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.metric("Median Frequency", f"{segment_data['Frequency'].median():.0f} orders",
              help="Number of purchases (higher is better)")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.metric("Median Spending", f"${segment_data['Monetary'].median():,.0f}",
              help="Total revenue from customer (higher is better)")
    st.markdown('</div>', unsafe_allow_html=True)

# Visualizations
st.subheader("Distribution Analysis")
tab1, tab2, tab3 = st.tabs(["Recency", "Frequency", "Monetary"])

with tab1:
    fig, ax = plt.subplots()
    sns.histplot(segment_data['Recency'], kde=True, bins=20, color='#1f77b4')
    plt.title(f'Recency Distribution - {selected_segment}')
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots()
    sns.histplot(segment_data['Frequency'], kde=True, bins=20, color='#ff7f0e')
    plt.title(f'Frequency Distribution - {selected_segment}')
    st.pyplot(fig)

with tab3:
    fig, ax = plt.subplots()
    sns.histplot(segment_data['Monetary'], kde=True, bins=20, color='#2ca02c')
    plt.title(f'Monetary Distribution - {selected_segment}')
    st.pyplot(fig)

# Data export
st.sidebar.header("Data Export")
if st.sidebar.button("Export Customer IDs"):
    csv = segment_data['CustomerID'].to_csv(index=False)
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{selected_segment}_customers.csv",
        mime="text/csv"
    )

# Cluster comparison
st.subheader("Segment Comparison")
fig = plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=rfm,
    x='Frequency',
    y='Monetary',
    hue='Segment',
    palette='viridis',
    size='Recency',
    sizes=(20, 200),
    alpha=0.7
)
plt.title("Customer Segments in RFM Space")
plt.xscale('log')
plt.yscale('log')
st.pyplot(fig)