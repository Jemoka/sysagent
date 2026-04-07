import pdfplumber


def _extract_pdf(path):
    with pdfplumber.open(path) as pdf:
        return "\n\n==========\n\n".join(
            f"# page {idx}\n" + (page.extract_text() or "")
            for idx, page in enumerate(pdf.pages, start=1)
        )


def _pdf_page_count(path):
    with pdfplumber.open(path) as pdf:
        return len(pdf.pages)


def _extract_pdf_page(path, page_num):
    """Extract text from a single page (0-indexed)."""
    with pdfplumber.open(path) as pdf:
        return pdf.pages[page_num].extract_text() or ""
