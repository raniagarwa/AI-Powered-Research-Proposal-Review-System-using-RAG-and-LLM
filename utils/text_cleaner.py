import re

def clean_text(text):
    """
    Clean extracted PDF text.
    """

    # Remove extra spaces
    text = re.sub(r"[ ]+", " ", text)

    # Remove multiple blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text