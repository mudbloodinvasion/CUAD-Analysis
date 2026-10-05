import streamlit as st
import html
from src.documentloader import (
    load_document,
    get_extraction_report
)

from src.pipeline import ContractRiskPipeline
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Contract Risk Analysis System",
    page_icon="📄",
    layout="wide"
)
st.markdown(
    """
    <style>
    .stApp { background: #fff0f6; }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1 { color: #ad1457 !important; font-weight: 800 !important; }
    h2 { color: #ad1457 !important; font-weight: 750 !important; }
    h3 { color: #c2185b !important; font-weight: 700 !important; }

    p, li, label, .stMarkdown,
    [data-testid="stCaptionContainer"] {
        color: #4a2633 !important;
    }
    .stButton > button {
        background-color: #e91e63 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.25rem !important;
        font-weight: 700 !important;
    }
    .stButton > button:hover {
        background-color: #c2185b !important;
        color: #ffffff !important;
    }

    [data-testid="stFileUploader"] {
        background-color: #ffe4ef !important;
        border: 2px dashed #e91e63 !important;
        border-radius: 14px !important;
        padding: 12px !important;
    }
    [data-testid="stFileUploader"] * {
        color: #4a2633 !important;
    }
    [data-testid="stTextInput"] input {
        background-color: #fff7fa !important;
        color: #4a2633 !important;
        -webkit-text-fill-color: #4a2633 !important;
        caret-color: #e91e63 !important;
        border: 1px solid #f48fb1 !important;
        border-radius: 9px !important;
    }
    [data-testid="stTextInput"] input::placeholder {
        color: #9e6b7d !important;
        -webkit-text-fill-color: #9e6b7d !important;
        opacity: 1 !important;
    }
    [data-testid="stTextInput"] input:focus {
        background-color: #ffffff !important;
        color: #4a2633 !important;
        -webkit-text-fill-color: #4a2633 !important;
        border-color: #e91e63 !important;
        box-shadow: 0 0 0 1px #e91e63 !important;
    }
    textarea {
        background-color: #fff7fa !important;
        color: #4a2633 !important;
        -webkit-text-fill-color: #4a2633 !important;
        caret-color: #e91e63 !important;
        border-color: #f48fb1 !important;
    }
    textarea::placeholder {
        color: #9e6b7d !important;
        -webkit-text-fill-color: #9e6b7d !important;
        opacity: 1 !important;
    }
    [data-testid="stExpander"] {
        background-color: #fff7fa !important;
        border: 1px solid #f48fb1 !important;
        border-radius: 11px !important;
    }
    .extracted-page-text {
        background-color: #fff7fa !important;
        color: #4a2633 !important;
        border: 1px solid #f8bbd0 !important;
        border-radius: 8px !important;
        padding: 14px 16px !important;
        white-space: pre-wrap !important;
        overflow-wrap: anywhere !important;
        word-break: normal !important;
        line-height: 1.55 !important;
        font-family: inherit !important;
        font-size: 0.95rem !important;
        max-height: 600px !important;
        overflow-y: auto !important;
    }

    [data-testid="stExpander"] pre,
    [data-testid="stExpander"] code,
    pre {
        background-color: #fff7fa !important;
        color: #4a2633 !important;
        -webkit-text-fill-color: #4a2633 !important;
        border: 1px solid #f8bbd0 !important;
        border-radius: 8px !important;
        white-space: pre-wrap !important;
    }

    [data-testid="stExpander"] summary {
        color: #ad1457 !important;
        font-weight: 650 !important;
    }

    [data-testid="stMetric"] {
        background-color: #ffe4ef !important;
        border: 1px solid #f48fb1 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    [data-testid="stMetricLabel"] { color: #7a4055 !important; }
    [data-testid="stMetricValue"] { color: #ad1457 !important; }
    [data-testid="stAlert"] { border-radius: 10px !important; }
    pre, code { color: #4a2633 !important; }
    hr { border-color: #f8bbd0 !important; }
    a { color: #c2185b !important; }
    </style>
    """,
    unsafe_allow_html=True
)
st.title(
    "📄 Contract Risk Analysis System"
)
st.write(
    """
    AI-powered commercial contract analysis using:
    **CUAD + Sentence Transformers + FAISS + Gemini**
    """
)
# LOAD PIPELIN
@st.cache_resource
def load_pipeline():
    return ContractRiskPipeline()
try:
    pipeline = load_pipeline()
except Exception as e:
    st.error(
        "Failed to initialize the analysis pipeline."
    )
    st.exception(e)
    st.stop()
# FILE UPLOAD
uploaded_file = st.file_uploader(
    "Upload a contract",
    type=["pdf", "txt"]
)
# PROCESS UPLOADED CONTRACT
if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )
    # DETERMINE FILE TYPE
    file_extension = (
        uploaded_file.name
        .split(".")[-1]
        .lower()
    )

    temp_path = (
        f"temp_contract.{file_extension}"
    )
    # SAVE TEMPORARY fILE
    with open(
        temp_path,
        "wb"
    ) as file:
        file.write(
            uploaded_file.getbuffer()
        )
    # EXTRACT DOCUMENT
  try:
        contract_text = load_document(
            temp_path
        )
    except Exception as e:
        st.error(
            "Could not extract text from the contract."
        )
        st.exception(e)
        st.stop()
    # DOCUMENT EXTRACTION REPORT
    st.divider()
    st.header(
        "📄 Document Extraction Report"
    )
    extraction_report = (
        get_extraction_report()
    )
    if extraction_report:
        # SUMMARY METRICS
       total_pages = (
            extraction_report[
                "total_pages"
            ]
        )
        pages_with_text = (
            extraction_report[
                "pages_with_text"
            ]
        )
        pages_without_text = (
            extraction_report[
                "pages_without_text"
            ]
        )
        col1, col2, col3 = st.columns(3)
        with col1:

            st.metric(
                "Total Pages",
                total_pages
            )
        with col2:

            st.metric(
                "Pages Extracted",
                pages_with_text
            )
        with col3:

            st.metric(
                "Pages Without Text",
                pages_without_text
            )
        # EXTRACTION STATUS-
        if pages_without_text == 0:

            st.success(
                "✅ Text was successfully extracted "
                "from every page."
            )

        else:

            st.warning(
                f"⚠️ {pages_without_text} page(s) "
                "had no extractable text."
            )
        # PAGE-BY-PAGE TEXT
        st.subheader(
            "📑 Page-by-Page Extracted Text"
        )
        for page in extraction_report[
            "pages"
        ]:
            page_number = page[
                "page_number"
            ]
            characters = page[
                "characters"
            ]
            has_text = page[
                "has_text"
            ]
            with st.expander(
                f"Page {page_number} — "
                f"{characters:,} characters"
            ):
                if has_text:

                    st.markdown(
                        f"""<div class=\"extracted-page-text\">{html.escape(page["text"])}</div>""",
                        unsafe_allow_html=True
                    )
                else:
                 st.warning(
                        "No extractable text was "
                        "found on this page. "
                        "It may be a scanned/image page."
                    )
    else:
        st.warning(
            "Extraction report is not available."
        )

    # ANALYZE CONTRACT
    st.divider()
    st.header(
        "🔍 Contract Analysis"
    )
    st.write(
        "The system will analyze the contract against "
        "the 41 CUAD clause categories."
    )
    if st.button(
        "🔍 Analyze Contract",
        type="primary"
    ):
        with st.spinner(
            "Analyzing contract with Gemini..."
        ):
            try:
                result = (
                    pipeline.analyze_contract(
                        contract_text
                    )
                )
                st.session_state[
                    "analysis"
                ] = result

                st.success(
                    "✅ Contract analysis completed!"
                )
            except Exception as e:
                st.error(
                    "Contract analysis failed."
                )
               st.exception(e)
# DISPLAY ANALYSIS RESULTS
if "analysis" in st.session_state:
    result = st.session_state[
        "analysis"
    ]
    report = result.get(
        "contract_report",
        {}
    )
    if not isinstance(report, dict):
        report = {
            "contract_summary": str(report),
            "overall_risk": "UNKNOWN",
            "key_risks": [],
            "important_obligations": [],
            "important_dates": [],
            "human_review_priorities": [],
            "overall_reasoning": ""
        }
    # CONTRACT RISK REPORT
    st.divider()

    st.header(
        "📊 Contract Risk Report"
    )
    overall_risk = report.get(
        "overall_risk",
        "UNKNOWN"
    )

    st.subheader(
        "Overall Risk"
    )

    st.metric(
        "Risk Level",
        overall_risk
    )
    st.subheader(
        "📋 Contract Summary"             #CONTRACT SUMMARY
    )
    st.write(
        report.get(
            "contract_summary",
            "No summary available."
        )
    )

    st.subheader(                           #KEY RISKS
        "⚠️ Key Risks"
    )

    key_risks = report.get(
        "key_risks",
        []
    )
    if key_risks:

        for risk in key_risks:

            if isinstance(
                risk,
                dict
            ):
                category = risk.get(
                    "category",
                    "Risk"
                )
                reason = risk.get(
                    "reason",
                    risk.get(
                        "risk_reason",
                        str(risk)
                    )
                )
                st.write(
                    f"**{category}**"
                )
                st.write(
                    reason
                )
            else:

                st.write(
                    f"• {risk}"
                )
    else:
        st.write(
            "No major risks reported."
        )
    st.subheader(
        "📌 Important Obligations"
    )
    obligations = report.get(
        "important_obligations",
        []
    )
    if obligations:

        for obligation in obligations:
            st.write(
                f"• {obligation}"
            )
    else:
        st.write(
            "No obligations identified."
        )
    st.subheader(
        "📅 Important Dates"
    )

    dates = report.get(
        "important_dates",
        []
    )
    if dates:
        for date in dates:
            st.write(
                f"• {date}"
            )
    else:
        st.write(
            "No important dates identified."
        )
    st.subheader(
        "👤 Human Review Priorities"
    )
    priorities = report.get(
        "human_review_priorities",
        []
    )
    if priorities:
        for priority in priorities:
            st.write(
                f"• {priority}"
            )
    else:
        st.write(
            "No specific review priorities identified."
        )
    st.subheader(
        "🧠 Overall Reasoning"
    )
    st.write(
        report.get(
            "overall_reasoning",
            "No reasoning available."
        )
    )
    st.divider()
    st.header(
        "🔎 Clause-Level Analysis"
    )
    clause_results = result.get(
        "clause_results",
        []
    )
    if not clause_results:
        st.warning(
            "No clause-level results were returned."
        )
    else:
        for item in clause_results:
            category = item.get(
                "category",
                "Unknown Category"
            )
            clause = item.get(
                "clause_analysis",
                {}
            )
            risk = item.get(
                "risk_analysis",
                {}
            )
            with st.expander(
                f"📑 {category}"
            ):
                present = clause.get(
                    "present",
                    False
                )
                st.write(
                    f"**Clause Present:** {present}"
                )
                evidence = clause.get(
                    "evidence",
                    ""
                )
                if evidence:

                    st.write(
                        "**Evidence:**"
                    )
                    st.info(
                        evidence
                    )
                summary = clause.get(
                    "summary",
                    ""
                )
                if summary:
                    st.write(
                        "**Clause Summary:**"
                    )
                    st.write(
                        summary
                    )
                confidence = clause.get(
                    "confidence",
                    0
                )
                st.write(
                    f"**Classification Confidence:** "
                    f"{confidence}"
                )
                risk_level = risk.get(
                    "risk_level",
                    "NONE"
                )
                st.write(
                    f"**Risk Level:** {risk_level}"
                )
                risk_reason = risk.get(
                    "risk_reason",
                    ""
                )
                if risk_reason:
                    st.write(
                        "**Risk Reason:**"
                    )
                    st.write(
                        risk_reason
                    )
                problematic = risk.get(
                    "problematic_elements",
                    []
                )
                if problematic:
                    st.write(
                        "**Potential Issues:**"
                    )
                   for issue in problematic:
                        st.write(
                            f"• {issue}"
                        )
                recommendation = risk.get(
                    "review_recommendation",
                    ""
                )
                if recommendation:
                    st.write(
                        "**Review Recommendation:**"
                    )
                    st.write(
                        recommendation
                    )
    st.divider()
    st.header(
        "💬 Ask the Contract"
    )
    question = st.text_input(
        "Ask a question about this contract:",
        placeholder=(
            "e.g. What happens if the agreement "
            "is terminated?"
        )
    )
    if st.button(
        "Ask Question"
    ):
        if not question.strip():

            st.warning(
                "Please enter a question."
            )
        else:
            with st.spinner(
                "Searching the contract..."
            ):
                try:
                   answer = (
                        pipeline.answer_question(
                            question
                        )
                    )
                    if "error" in answer:
                        st.error(
                            answer["error"]
                        )
                    else:
                        st.subheader(
                            "Answer"
                        )
                        st.write(
                            answer.get(
                                "answer",
                                ""
                            )
                        )
                        st.subheader(
                            "Evidence"
                        )
                        st.info(
                            answer.get(
                                "evidence",
                                ""
                            )
                        )
                        confidence = answer.get(
                            "confidence",
                            0
                        )
                        try:
                            confidence = float(confidence)
                        except (TypeError, ValueError):
                            confidence = 0.0
                        st.write(
                            f"Confidence: "
                            f"{confidence:.2f}"
                        )
                except Exception as e:
                    st.error(
                        "Question answering failed."
                    )
                    st.exception(e)
