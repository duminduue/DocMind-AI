"""PDF upload validation utilities for DocMind AI."""

from __future__ import annotations

from typing import Any

import fitz


MAX_FILE_SIZE_MB = 20
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def validate_pdf(uploaded_file: Any) -> tuple[bool, str]:
    """Validate an uploaded PDF before it is accepted by the application.

    The function expects an uploaded-file object with name and getvalue()
    attributes, such as Streamlit's UploadedFile.

    Returns:
        A pair containing the validation result and a user-friendly message.
    """
    if uploaded_file is None:
        return False, "No file was provided."

    file_name = getattr(uploaded_file, "name", "")
    if not isinstance(file_name, str) or not file_name.lower().endswith(".pdf"):
        return False, "Only files with a .pdf extension are supported."

    try:
        file_bytes = uploaded_file.getvalue()
    except Exception:
        return False, "The uploaded file could not be read."

    if not file_bytes:
        return False, "The uploaded file is empty."

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        return (
            False,
            f"File is too large. The maximum allowed size is {MAX_FILE_SIZE_MB} MB.",
        )

    # PDF readers allow the header to appear within the first 1,024 bytes.
    if b"%PDF-" not in file_bytes[:1024]:
        return False, "The file does not contain a valid PDF header."

    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as document:
            if document.needs_pass:
                return False, "Password-protected PDFs are not supported."

            if document.page_count == 0:
                return False, "The PDF contains no pages."

    except (fitz.FileDataError, fitz.EmptyFileError):
        return False, "The PDF is damaged or cannot be opened."
    except Exception:
        return False, "The PDF could not be validated."

    return True, "PDF validated successfully."
