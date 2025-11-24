import streamlit as st
import pandas as pd
import re
from data_collection import collect_papers
from summarizer import summarize_csv
from insight_agent import generate_insights
from writer_agent import generate_related_work

st.set_page_config(page_title="📚 Academic Research Agent", layout="wide")
st.title("📚 ScholarBot - a Multi-Agent System for Dynamic Academic Research and writing")

topic = st.text_input("Enter Research Topic:")
# file_name = f"{topic}_papers.csv"
safe_query = re.sub(r"[^\w\-]", "_", topic)
file_name = f"{safe_query}_papers.csv"


# Step 1: Collect
if st.button("Step 1: Collect Papers"):
    with st.spinner("⏳ Collecting papers..."):
        collect_papers(topic)
    st.success("Papers collected!")
    
        # ✅ Display collected papers in the UI
    try:
        df_collected = pd.read_csv(file_name)
        st.subheader("📄 Collected Papers")

        if 'url' in df_collected.columns:
            # Convert the 'url' column to clickable markdown links
            df_collected['url'] = df_collected['url'].apply(lambda x: f"[Link]({x})" if pd.notnull(x) else "")
        # Display using markdown table (to support links)
        st.markdown(df_collected.to_markdown(index=False), unsafe_allow_html=True)
        #st.dataframe(df_collected, use_container_width=True)
    except FileNotFoundError:
        st.warning("⚠ CSV file not found after collection.")

# Step 2: Summarize
if st.button("Step 2: Summarize"):
    summarize_csv(file_name)
    st.success("Summarization completed!")

    # ✅ Display summaries inside UI
    summarized_file = file_name.replace(".csv", "_summarized.csv")
    try:
        df_summary = pd.read_csv(summarized_file)
        st.subheader("📄 Summaries")
        for idx, row in df_summary.iterrows():
            with st.expander(f"{idx+1}. {row['title']}"):
                st.write(row['summary'])
    except FileNotFoundError:
        st.warning("No summarized file found yet.")

# Step 3: Generate Insights
if st.button("Step 3: Generate Insights"):
    summarize_file = file_name.replace(".csv", "_summarized.csv")
    generate_insights(summarize_file)
    st.success("Insights generated!")

    insights_file = summarize_file.replace(".csv", "_insights.csv")
    try:
        df_insights = pd.read_csv(insights_file)
        st.subheader("💡 Insights & Hypotheses")
        for idx, row in df_insights.iterrows():
            with st.expander(f"{idx+1}. {row['title']}"):
                st.write(row['insights_hypotheses'])
    except FileNotFoundError:
        st.warning("No insights file found.")
# Step 4: Related Work
if st.button("Step 4: Generate Related Work"):
    insights_file = file_name.replace(".csv", "_summarized_insights.csv")
    generate_related_work(insights_file)
    st.success("Related Work Section Created!")

    # ✅ Display Markdown content
    try:
        with open("related_work.md", "r", encoding="utf-8") as f:
            related_text = f.read()
        st.subheader("🧠 Related Work Section")
        st.markdown(related_text)
    except FileNotFoundError:
        st.warning("No related work section found.")
if 'df_summary' in locals():
    st.download_button(
        label="📥 Download Summaries CSV",
        data=df_summary.to_csv(index=False).encode('utf-8'),
        file_name=f"{topic}_summarized.csv",
        mime='text/csv'
    )
st.markdown(
    """
    <style>
        .stApp {
            background-color: #E6E6FA; /* Soft Lavender Purple for the main app background */
        }
        /* Target the internal class for the header/top bar */
        .stApp > header {
            background-color: #E6E6FA; /* Apply Soft Lavender Purple to the top bar as well */
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("---")
st.markdown(
    "<center>🚀 Built with ❤️ using Streamlit | ScholarBot</center>",
    unsafe_allow_html=True
)
