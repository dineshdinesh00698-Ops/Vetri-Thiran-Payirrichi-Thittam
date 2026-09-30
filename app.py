import os
import html
import requests
import streamlit as st
from utils.formatters import format_docx, format_pdf, sanitize_text

API_URL = os.getenv("LEGALEASE_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
.main-title {text-align:center; font-size:42px; font-weight:700;}
.subtitle {text-align:center; color:#777; margin-bottom:25px;}
.preview {background:#151515; color:#f2f2f2; padding:25px; border-radius:12px;
          max-height:550px; overflow:auto; white-space:pre-wrap; font-family:Georgia,serif;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Legal Document Generator</div>', unsafe_allow_html=True)

with st.form("legal_form"):
    document_type = st.text_input("Document Type", "Employment Contract")
    parties = st.text_area("Parties Involved",
                           "Employer: ABC Company; Employee: John Doe")
    terms = st.text_area(
        "Terms & Conditions",
        "Role and responsibilities; Compensation and payment terms; Confidentiality; Termination notice"
    )
    dates = st.text_input("Effective Date", "30/09/2026")
    submitted = st.form_submit_button("Generate Document")

if submitted:
    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "dates": dates
    }
    try:
        response = requests.post(f"{API_URL}/generate", json=payload, timeout=120)
        response.raise_for_status()
        st.session_state["document"] = response.json()["document"]
        st.success("Document generated successfully.")
    except requests.RequestException as exc:
        st.error(f"Backend connection error: {exc}")

if "document" in st.session_state:
    st.subheader("Preview")
    document = st.session_state["document"]

    st.markdown(
        f'<div class="preview">{html.escape(document)}</div>',
        unsafe_allow_html=True
    )

    st.subheader("Edit Document")
    edited = st.text_area("Editable document", document, height=450)
    st.session_state["document"] = edited

    clean = sanitize_text(edited)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            "Download TXT",
            data=clean,
            file_name="LegalEase_Document.txt",
            mime="text/plain"
        )

    with col2:
        docx_bytes = format_docx(clean, document_type)
        st.download_button(
            "Download DOCX",
            data=docx_bytes,
            file_name="LegalEase_Document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    with col3:
        pdf_bytes = format_pdf(clean, document_type)
        st.download_button(
            "Download PDF",
            data=pdf_bytes,
            file_name="LegalEase_Document.pdf",
            mime="application/pdf"
        )
