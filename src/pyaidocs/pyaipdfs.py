#%%
import fitz  # PyMuPDF
from pprint import pprint

#%%
# check if the pdf is password protected
def is_pdf_password_protected(pdf_path):
    doc = fitz.open(pdf_path)
    is_protected = doc.needs_pass
    doc.close()
    return is_protected

def retrieve_info(doc, page_num, tables_=False):
    page = doc[page_num]
    text= page.get_text()
    data= []
    if tables_:
        tabs = page.find_tables( vertical_strategy="text")
        for tab in tabs:
            for line in tab.extract():  # print cell text for each row
                data.append(line)
    return data, text

# Function to format the data nicely
def format_data(data):
    # each element of data is a list, if all are '' skip them

    data = [d for d in data if any(d)]
    # replace '' with ' ' 
    data = [[cell if cell else ' ' for cell in row] for row in data]
    # join 
    data = [' '.join(row) for row in data]
    # return it as text line by line
    return '\n'.join(data)


def pdf_to_text(pdf_path, password, pages=None, tables_=True):

    # Open the PDF file
    doc = fitz.open(pdf_path)  # Open the PDF
    if doc.needs_pass:  # Check if the document is password-protected
        success = doc.authenticate(password)  # Try to authenticate with the password
        if not success:
            return None, None, "The password is incorrect. Please try again."
    text = ""
    # Iterate through each page
    text_pages = []
    tables = []
    pages = pages if pages else range(doc.page_count)
    for page_num in pages:
        data, text = retrieve_info(doc, page_num, tables_=tables_)
        # ask to get the table cleaned
        if tables_:
            data = format_data(data)
            tables.append(data)

        text_pages.append(text)
    doc.close()  # Remember to close the document

    return text_pages, tables, "The PDF has been processed."


