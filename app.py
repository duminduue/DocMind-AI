import streamlit as st

from modules.pdf_handler import MAX_FILE_SIZE_MB, validate_pdf


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="DocMind AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("📚 DocMind AI")
st.sidebar.caption("Document Intelligence Platform")
st.sidebar.divider()
st.sidebar.subheader("Navigation")
st.sidebar.info("Dashboard")
st.sidebar.divider()
st.sidebar.caption("Version 1.0.0")

# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

st.title("📚 DocMind AI")
st.subheader("AI-Powered PDF Document Intelligence")
st.write(
    "Upload your PDF documents, explore their content, and "
    "get AI-powered answers using your own documents."
)

st.divider()

# --------------------------------------------------
# PDF UPLOAD AND VALIDATION
# --------------------------------------------------

st.header("Upload PDF Documents")
st.write(
    f"Choose one or more PDF files. Each file must be no larger "
    f"than {MAX_FILE_SIZE_MB} MB."
)

uploaded_files = st.file_uploader(
    "Select PDF documents",
    type=["pdf"],
    accept_multiple_files=True,
    help=f"PDF files only. Maximum file size: {MAX_FILE_SIZE_MB} MB per file.",
)

valid_documents = []
invalid_documents = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        is_valid, message = validate_pdf(uploaded_file)

        if is_valid:
            valid_documents.append(uploaded_file)
        else:
            invalid_documents.append((uploaded_file.name, message))

    st.divider()
    st.subheader("Upload Results")

    for uploaded_file in valid_documents:
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)

        with st.container(border=True):
            col_name, col_size, col_status = st.columns([3, 1, 1])

            with col_name:
                st.write(f"📄 **{uploaded_file.name}**")

            with col_size:
                st.caption(f"{file_size_mb:.2f} MB")

            with col_status:
                st.success("Valid PDF")

    for file_name, message in invalid_documents:
        st.error(f"{file_name}: {message}")

    if valid_documents:
        st.success(
            f"{len(valid_documents)} PDF file(s) passed validation. "
            "Document text extraction will be added in the next phase."
        )

# --------------------------------------------------
# DASHBOARD METRICS
# --------------------------------------------------

st.divider()
st.header("Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Valid Uploaded Documents",
        value=len(valid_documents),
    )

with col2:
    st.metric(
        label="Questions Asked",
        value=0,
    )

with col3:
    st.metric(
        label="Processed Documents",
        value=0,
    )

# --------------------------------------------------
# CURRENT DEVELOPMENT STATUS
# --------------------------------------------------

st.divider()
st.header("About DocMind AI")

st.info(
    "PDF upload and basic file validation are now available. "
    "Text extraction, document storage, semantic search, and "
    "AI question answering will be introduced in later phases."
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()
st.caption(
    "DocMind AI | AI PDF Content Finder | "
    "Developed with Python and Streamlit"
)
