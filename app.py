import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io

# Page config
st.set_page_config(
    page_title="AI Data Visualization Assistant",
    page_icon="📊",
    layout="wide"
)

# Header
st.title("📊 AI Data Visualization Assistant")
st.markdown("*Upload a CSV dataset to automatically generate insights and visualizations.*")
st.markdown("---")

# Module 1: File Upload
st.header("📁 Upload Your Dataset")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Module 2: Dataset Preview
    df = pd.read_csv(uploaded_file)

    st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
    st.markdown("---")

    st.header("🔍 Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

    # Module 3: Dataset Information
    st.markdown("---")
    st.header("ℹ️ Dataset Information")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", df.shape[0])
    with col2:
        st.metric("Total Columns", df.shape[1])
    with col3:
        st.metric("Missing Values", int(df.isnull().sum().sum()))

    # Show missing values per column
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        st.subheader("Missing Values per Column")
        st.bar_chart(missing)
    else:
        st.info("✅ No missing values found in the dataset.")

    # Module 4: Statistical Summary
    st.markdown("---")
    st.header("📈 Statistical Summary")
    numeric_df = df.select_dtypes(include='number')
    if not numeric_df.empty:
        st.dataframe(numeric_df.describe().round(2), use_container_width=True)
    else:
        st.warning("No numeric columns found for statistical summary.")

    # Module 5: Data Visualization
    st.markdown("---")
    st.header("📉 Data Visualizations")

    if not numeric_df.empty:
        columns = numeric_df.columns.tolist()
        selected_col = st.selectbox("Select a column to visualize:", columns)

        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader(f"Line Chart – {selected_col}")
            fig1, ax1 = plt.subplots(figsize=(6, 3))
            ax1.plot(numeric_df[selected_col].values, color='#1f77b4', linewidth=2)
            ax1.set_xlabel("Index")
            ax1.set_ylabel(selected_col)
            ax1.set_title(f"{selected_col} – Line Chart")
            ax1.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(fig1)
            plt.close(fig1)

        with col_b:
            st.subheader(f"Bar Chart – {selected_col}")
            fig2, ax2 = plt.subplots(figsize=(6, 3))
            sample = numeric_df[selected_col].head(20)
            ax2.bar(range(len(sample)), sample.values, color='#2ca02c', alpha=0.8)
            ax2.set_xlabel("Index")
            ax2.set_ylabel(selected_col)
            ax2.set_title(f"{selected_col} – Bar Chart")
            ax2.grid(True, axis='y', linestyle='--', alpha=0.5)
            st.pyplot(fig2)
            plt.close(fig2)

        # Histogram
        st.subheader(f"Distribution – {selected_col}")
        fig3, ax3 = plt.subplots(figsize=(8, 3))
        ax3.hist(numeric_df[selected_col].dropna(), bins=20, color='#ff7f0e', edgecolor='white')
        ax3.set_xlabel(selected_col)
        ax3.set_ylabel("Frequency")
        ax3.set_title(f"Distribution of {selected_col}")
        st.pyplot(fig3)
        plt.close(fig3)

    # Module 6: AI Insights
    st.markdown("---")
    st.header("🤖 AI Insights")

    if not numeric_df.empty:
        for col in numeric_df.columns:
            col_data = numeric_df[col].dropna()
            if len(col_data) == 0:
                continue
            mean_val = col_data.mean()
            max_val = col_data.max()
            min_val = col_data.min()
            std_val = col_data.std()
            max_idx = col_data.idxmax()
            min_idx = col_data.idxmin()

            with st.expander(f"📌 Insights for **{col}**"):
                st.markdown(f"""
- **Average Value:** {mean_val:.2f}
- **Maximum Value:** {max_val:.2f} *(at row {max_idx})*
- **Minimum Value:** {min_val:.2f} *(at row {min_idx})*
- **Standard Deviation:** {std_val:.2f}
- **Trend:** {'📈 Values are spread widely' if std_val > mean_val * 0.3 else '📊 Values are relatively consistent'}
- **Data Quality:** {'⚠️ Contains missing values' if df[col].isnull().sum() > 0 else '✅ No missing values'}
                """)
    else:
        st.info("No numeric columns available for AI insights.")

    st.markdown("---")
    st.caption("AI Data Visualization Assistant — Built with Python, Streamlit, Pandas & Matplotlib")

else:
    st.info("👆 Please upload a CSV file to get started.")
    st.markdown("""
    ### What this app does:
    - 📋 **Preview** your uploaded dataset
    - ℹ️ **Analyze** rows, columns, and missing values
    - 📈 **Generate** statistical summaries
    - 📉 **Create** line charts, bar charts, and histograms
    - 🤖 **Provide** AI-powered insights about your data
    """)
