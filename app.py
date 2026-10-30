
import streamlit as st
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from urllib.parse import urlparse
from datetime import datetime

# Import Gemini AI functions
from ai_engine import create_ai_plan, generate_ai_report


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="ResearchMate AI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. CUSTOM UI
# =====================================================

st.markdown("""
<style>
.main {
    background-color: #F8F9FC;
}

h1 {
    color: #5636A5;
}

h2, h3 {
    color: #49328A;
}

.stButton > button {
    background-color: #6741B9;
    color: white;
    border-radius: 9px;
    border: none;
    height: 45px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #4D2E91;
    color: white;
}

.report-box {
    padding: 15px;
    border-radius: 10px;
    background-color: white;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. HEADER
# =====================================================

st.title("🔎 ResearchMate AI")

st.subheader(
    "Your Intelligent AI Research Assistant"
)

st.write(
    "Research smarter with AI-powered planning, "
    "web search, information extraction and analysis."
)

st.caption(
    "Powered by Google Gemini | Python | Streamlit | DuckDuckGo"
)

st.divider()


# =====================================================
# 4. SIDEBAR
# =====================================================

with st.sidebar:

    st.title("⚙️ Research Settings")

    max_results = st.slider(
        "Maximum search results",
        min_value=3,
        max_value=8,
        value=6
    )

    max_pages = st.slider(
        "Maximum webpages to read",
        min_value=1,
        max_value=5,
        value=3
    )

    st.divider()

    st.subheader("Agent Architecture")

    st.write("🧠 Gemini AI Planner")
    st.write("🔍 DuckDuckGo Search")
    st.write("📄 Webpage Reader")
    st.write("🧹 Information Filtering")
    st.write("📊 AI Report Generator")
    st.write("✅ Pydantic Validation")

    st.divider()

    st.info(
        "Enter a research question to start "
        "the automated research process."
    )


# =====================================================
# 5. RESEARCH PLANNER
# =====================================================

def fallback_plan(question):

    return [
        "Understand the user's research question.",
        "Identify important topics and research dimensions.",
        "Search for relevant information.",
        "Filter and read useful sources.",
        "Generate a structured research report."
    ]


# =====================================================
# 6. TOOL 1: WEB SEARCH
# =====================================================

def web_search(question, max_results):

    results = []

    try:

        with DDGS() as ddgs:

            search_results = ddgs.text(
                question,
                max_results=max_results
            )

            for item in search_results:

                url = item.get("href", "")

                if not url.startswith(
                    ("http://", "https://")
                ):
                    continue

                results.append({
                    "title": item.get(
                        "title", "Untitled"
                    ),
                    "url": url,
                    "snippet": item.get(
                        "body", ""
                    )
                })

    except Exception as error:

        st.warning(
            f"Web search encountered an error: {error}"
        )

    return results


# =====================================================
# 7. TOOL 2: WEBPAGE READER
# =====================================================

def read_webpage(url):

    try:

        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 ResearchMateAI/1.0"
            },
            timeout=12
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type", ""
        )

        if content_type and "text/html" not in content_type:
            return None

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "noscript",
            "iframe"
        ]):
            tag.decompose()

        title = (
            soup.title.get_text(strip=True)
            if soup.title else url
        )

        content = soup.get_text(
            separator=" ",
            strip=True
        )

        return {
            "title": title,
            "url": url,
            "content": content[:4000]
        }

    except requests.RequestException:
        return None

    except Exception:
        return None


# =====================================================
# 8. INFORMATION FILTERING
# =====================================================

def filter_results(results):

    filtered = []
    seen_domains = set()

    for item in results:

        url = item.get("url", "")

        domain = urlparse(url).netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        if not domain:
            continue

        if domain in seen_domains:
            continue

        if not item.get("snippet", "").strip():
            continue

        seen_domains.add(domain)

        filtered.append(item)

    return filtered


# =====================================================
# 9. FORMAT FINAL REPORT
# =====================================================

def format_report(question, plan, ai_report, sources):

    report = f"""
# ResearchMate AI - Research Report

**Generated:** {datetime.now().strftime("%d-%m-%Y %H:%M")}

## 1. User Question

{question}

## 2. Research Plan

"""

    for i, step in enumerate(plan, 1):

        report += f"{i}. {step}\n"

    report += f"""

## 3. Short Answer

{ai_report.short_answer}

## 4. Key Findings

"""

    for finding in ai_report.key_findings:

        report += f"- {finding}\n"

    report += "\n## 5. Sources Used\n\n"

    if sources:

        for i, source in enumerate(sources, 1):

            report += (
                f"{i}. [{source['title']}]"
                f"({source['url']})\n\n"
            )

    else:

        report += "No sources were retrieved.\n"

    report += f"""

## 6. Confidence Level

{ai_report.confidence}

## 7. Assumptions

"""

    for item in ai_report.assumptions:

        report += f"- {item}\n"

    report += "\n## 8. Limitations\n\n"

    for item in ai_report.limitations:

        report += f"- {item}\n"

    report += "\n## 9. Suggested Next Steps\n\n"

    for item in ai_report.next_steps:

        report += f"- {item}\n"

    return report


# =====================================================
# 10. USER INPUT
# =====================================================

st.header("💡 Ask Your Research Question")

question = st.text_area(
    "Enter your question below:",
    placeholder=(
        "Example: Compare the top 3 open-source "
        "vector databases for startups building RAG products."
    ),
    height=110
)


# =====================================================
# 11. START RESEARCH
# =====================================================

if st.button(
    "🚀 Start Research",
    use_container_width=True
):

    if not question.strip():

        st.warning(
            "Please enter a research question."
        )

    else:

        st.session_state["last_question"] = question

        # ---------------------------------------------
        # STEP 1: AI PLANNING
        # ---------------------------------------------

        st.header("1. 🧠 AI Research Planning")

        try:

            with st.spinner(
                "Gemini is creating your research plan..."
            ):

                plan = create_ai_plan(question)

            st.success(
                "AI research plan generated successfully!"
            )

        except Exception as error:

            st.warning(
                f"AI planning unavailable. Using fallback plan. Details: {error}"
            )

            plan = fallback_plan(question)

        for i, step in enumerate(plan, 1):

            st.markdown(
                f"**Step {i}:** {step}"
            )

        st.divider()

        # ---------------------------------------------
        # STEP 2: WEB SEARCH
        # ---------------------------------------------

        st.header("2. 🔍 Web Search")

        with st.spinner(
            "Searching the internet for relevant information..."
        ):

            search_results = web_search(
                question,
                max_results
            )

        st.metric(
            "Search Results Retrieved",
            len(search_results)
        )

        # ---------------------------------------------
        # STEP 3: FILTERING
        # ---------------------------------------------

        st.header("3. 🧹 Information Filtering")

        sources = filter_results(search_results)

        st.metric(
            "Relevant Distinct-Domain Sources",
            len(sources)
        )

        if not sources:

            st.error(
                "No usable sources were found. "
                "Please try another research question."
            )

            st.stop()

        # ---------------------------------------------
        # STEP 4: WEBPAGE EXTRACTION
        # ---------------------------------------------

        st.header("4. 📄 Webpage Content Extraction")

        pages = []

        progress = st.progress(0)

        selected_sources = sources[:max_pages]

        for i, source in enumerate(selected_sources):

            with st.spinner(
                f"Reading source {i+1} of {len(selected_sources)}..."
            ):

                page = read_webpage(
                    source["url"]
                )

                if page and page["content"].strip():

                    pages.append(page)

            progress.progress(
                (i + 1) / len(selected_sources)
            )

        st.metric(
            "Successfully Read Webpages",
            len(pages)
        )

        if not pages:

            st.warning(
                "The search results were found, "
                "but none of the webpages could be accessed. "
                "The agent will use search snippets only."
            )

        st.divider()

        # ---------------------------------------------
        # STEP 5: GEMINI AI SYNTHESIS
        # ---------------------------------------------

        st.header("5. 🤖 AI Research Analysis")

        try:

            with st.spinner(
                "Gemini is analysing the collected evidence..."
            ):

                ai_report = generate_ai_report(
                    question,
                    plan,
                    sources,
                    pages
                )

            st.success(
                "Gemini AI successfully generated the research report!"
            )

            # -----------------------------------------
            # SHORT ANSWER
            # -----------------------------------------

            st.subheader("📝 Short Answer")

            st.write(
                ai_report.short_answer
            )

            # -----------------------------------------
            # KEY FINDINGS
            # -----------------------------------------

            st.subheader("📌 Key Findings")

            for finding in ai_report.key_findings:

                st.markdown(
                    f"- {finding}"
                )

            # -----------------------------------------
            # CONFIDENCE
            # -----------------------------------------

            st.subheader("🎯 Confidence Level")

            st.info(
                ai_report.confidence
            )

            # -----------------------------------------
            # ASSUMPTIONS
            # -----------------------------------------

            st.subheader("📋 Assumptions")

            for item in ai_report.assumptions:

                st.markdown(
                    f"- {item}"
                )

            # -----------------------------------------
            # LIMITATIONS
            # -----------------------------------------

            st.subheader("⚠️ Limitations")

            for item in ai_report.limitations:

                st.markdown(
                    f"- {item}"
                )

            # -----------------------------------------
            # NEXT STEPS
            # -----------------------------------------

            st.subheader("➡️ Suggested Next Steps")

            for item in ai_report.next_steps:

                st.markdown(
                    f"- {item}"
                )

            # -----------------------------------------
            # CREATE REPORT
            # -----------------------------------------

            report = format_report(
                question,
                plan,
                ai_report,
                sources
            )

        except Exception as error:

            st.error(
                f"AI report generation failed: {error}"
            )

            st.info(
                "Please check your Gemini API key, "
                "model availability and internet connection."
            )

            st.stop()

        st.divider()

        # ---------------------------------------------
        # STEP 6: SOURCE DISPLAY
        # ---------------------------------------------

        st.header("6. 📚 Research Sources")

        for i, source in enumerate(sources, 1):

            with st.expander(
                f"Source {i}: {source['title']}"
            ):

                st.write(
                    source["snippet"]
                )

                st.markdown(
                    f"[Open Source]({source['url']})"
                )

        # ---------------------------------------------
        # STEP 7: SYSTEM EVALUATION
        # ---------------------------------------------

        st.header("7. 📊 System Evaluation")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Search Results",
                len(search_results)
            )

        with col2:

            st.metric(
                "Filtered Sources",
                len(sources)
            )

        with col3:

            st.metric(
                "Pages Read",
                len(pages)
            )

        st.caption(
            "Confidence is an AI-generated qualitative assessment, "
            "not a calibrated probability."
        )

        # ---------------------------------------------
        # STEP 8: DOWNLOAD REPORT
        # ---------------------------------------------

        st.header("8. 📥 Download Research Report")

        st.download_button(
            label="Download Complete Research Report",
            data=report,
            file_name="ResearchMate_Research_Report.md",
            mime="text/markdown",
            use_container_width=True
        )

        st.success(
            "Research process completed successfully!"
        )


# =====================================================
# 12. FOOTER
# =====================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:gray;">

    **ResearchMate AI**

    AI-Powered Research and Analysis System

    Built using Python, Gemini AI, Streamlit and Web Research Tools.

    </div>
    """,
    unsafe_allow_html=True
)
