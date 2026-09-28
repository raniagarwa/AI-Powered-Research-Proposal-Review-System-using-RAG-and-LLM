import fitz

def extract_text(uploaded_file):
    """
    Extract text from an uploaded PDF file.
    """

    pdf = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

    return text