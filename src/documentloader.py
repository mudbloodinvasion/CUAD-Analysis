from pathlib import Path
from pypdf import PdfReader


def load_document(file_path: str) -> str:
    """
    Extract text from a PDF or TXT file.

    For PDFs:
    - Extracts text from every page
    - Stores page-by-page extraction information
    - Reports pages with and without extractable text
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = path.suffix.lower()

    # --------------------------------------------------
    # TXT FILE
    # --------------------------------------------------

    if extension == ".txt":

        text = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        # Store extraction information
        load_document.last_report = {
            "file_type": "TXT",
            "total_pages": 1,
            "pages_with_text": 1 if text.strip() else 0,
            "pages_without_text": 0 if text.strip() else 1,
            "pages": [
                {
                    "page_number": 1,
                    "characters": len(text),
                    "text": text
                }
            ]
        }

        return text

    # --------------------------------------------------
    # PDF FILE
    # --------------------------------------------------

    if extension == ".pdf":

        reader = PdfReader(
            str(path)
        )

        total_pages = len(
            reader.pages
        )

        pages = []
        extracted_text = []

        pages_with_text = 0
        pages_without_text = 0

        # ----------------------------------------------
        # EXTRACT EVERY PAGE
        # ----------------------------------------------

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            try:

                text = page.extract_text()

            except Exception as e:

                text = ""

                print(
                    f"Warning: Could not extract "
                    f"page {page_number}: {e}"
                )

            if text is None:
                text = ""

            text = text.strip()

            # ------------------------------------------
            # PAGE REPORT
            # ------------------------------------------

            if text:

                pages_with_text += 1

                extracted_text.append(
                    text
                )

            else:

                pages_without_text += 1

            pages.append({

                "page_number": page_number,

                "characters": len(text),

                "has_text": bool(text),

                "text": text
            })

        # ----------------------------------------------
        # SAVE EXTRACTION REPORT
        # ----------------------------------------------

        load_document.last_report = {

            "file_type": "PDF",

            "total_pages": total_pages,

            "pages_with_text": pages_with_text,

            "pages_without_text": pages_without_text,

            "pages": pages
        }

        # ----------------------------------------------
        # COMBINE ALL EXTRACTED TEXT
        # ----------------------------------------------

        return "\n\n".join(
            extracted_text
        )

    # --------------------------------------------------
    # UNSUPPORTED FILE
    # --------------------------------------------------

    raise ValueError(
        "Unsupported file type. "
        "Only PDF and TXT files are supported."
    )


# ------------------------------------------------------
# GET LAST EXTRACTION REPORT
# ------------------------------------------------------

def get_extraction_report():
    """
    Return the report generated during the last
    document extraction.
    """

    return getattr(
        load_document,
        "last_report",
        None
    )