import fitz  # PyMuPDF
from pprint import pprint

#%%

# check if the pdf is password protected
def is_pdf_password_protected(pdf_path):
    """Check if the PDF is password protected.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        bool: True if the PDF is password protected, False otherwise.
    """
    doc = fitz.open(pdf_path)
    is_protected = doc.needs_pass
    doc.close()
    return is_protected

def retrieve_info(doc, page_num, tables_=False):
    """Retrieve text and table data from a specific page of the PDF document.

    Args:
        doc (fitz.Document): The opened PDF document object.
        page_num (int): The page number to extract data from.
        tables_ (bool): Flag indicating whether to extract table data. Default is False.

    Returns:
        tuple: A tuple containing:
            - data (list): Extracted table data as a list of lists (rows and columns).
            - text (str): Extracted plain text from the page.
    """
    page = doc[page_num]
    text = page.get_text()
    data = []
    if tables_:
        tabs = page.find_tables(vertical_strategy="text")
        for tab in tabs:
            for line in tab.extract():  # Extract cell text for each row
                data.append(line)
    return data, text

def format_data(data):
    """Format table data by cleaning empty cells and formatting it as text.

    Args:
        data (list): The list of lists containing table data.

    Returns:
        str: Formatted table data as a single string with rows joined by newlines.
    """
    # Filter out rows where all elements are empty
    data = [d for d in data if any(d)]
    # Replace empty strings with a single space
    data = [[cell if cell else ' ' for cell in row] for row in data]
    # Join each row into a single string
    data = [' '.join(row) for row in data]
    # Return the formatted data line by line
    return '\n'.join(data)

def pdf_to_text(pdf_path, password, pages=None, tables_=True):
    """Extract text and optionally table data from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.
        password (str): Password for the PDF file if it is password protected.
        pages (list, optional): List of page numbers to process. Processes all pages if None.
        tables_ (bool): Flag indicating whether to extract table data. Default is True.

    Returns:
        tuple: A tuple containing:
            - text_pages (list): A list of strings, each containing the text of a page.
            - tables (list): A list of formatted table data as strings, one for each page.
            - message (str): Status message indicating the result of the operation.
    """
    # Open the PDF file
    doc = fitz.open(pdf_path)  # Open the PDF
    if doc.needs_pass:  # Check if the document is password-protected
        success = doc.authenticate(password)  # Try to authenticate with the password
        if not success:
            return None, None, "The password is incorrect. Please try again."
    
    text_pages = []
    tables = []
    pages = pages if pages else range(doc.page_count)
    
    # Iterate through each page
    for page_num in pages:
        data, text = retrieve_info(doc, page_num, tables_=tables_)
        
        if tables_:
            data = format_data(data)
            tables.append(data)

        text_pages.append(text)
    
    doc.close()  # Remember to close the document

    return text_pages, tables, "The PDF has been processed."
