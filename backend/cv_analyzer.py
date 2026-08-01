import pdfplumber


def extract_text(pdf_path):
    """
    Extract text from a PDF file.
    """

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


if __name__ == "__main__":

    cv_path = "uploads/SampleCV2.pdf"


    text = extract_text(cv_path)

    print(text)