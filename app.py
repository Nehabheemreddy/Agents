import streamlit as st
from src.pipeline.pipeline import run_research_pipeline

st.set_page_config(page_title="Multi-Agent Research", page_icon="🔎")
st.title("🔎 Multi-Agent Research System")
st.write("Search → Read → Write → Review")

topic = st.text_input("Enter a research topic")

if st.button("Run Research") and topic:
    with st.spinner("Agents are working..."):
        state = run_research_pipeline(topic)

    st.subheader("📄 Report")
    st.markdown(state["report"])

    st.subheader("🧐 Critic Feedback")
    st.write(state["feedback"])

    st.download_button("Download Report", state["report"], file_name="report.md")

    with st.expander("Search Results"):
        st.write(state["search_results"])
    with st.expander("Scraped Content"):
        st.write(state["scraped_content"])