#%%
from pyaidocs.pyaidocs import retrieve_key_variables_text
from pyaidocs.options import Options

options = Options()
options.initialize()

pdf_path = r"C:\Users\jfimb\Dropbox\AlphaGenFiles\old\prototype_seine\NGEM\3Q23 NGEM Investment Report.pdf"

key_variables =  ["Fund Name", "CCY", "Vintage", "Ref. Date", "Seller's Fund Ownership", "Commitment", 
                  "Called", "Unfunded", "Distributed", "NAV", "FMV", "Other Assets", "Liabilities", 
                "% Called", "Final Closing", "Term", "Extensions", "Default Cash Exit Date", "Hurdle", "Carried", "Catch-Up" 
        ]
response = retrieve_key_variables_text(pdf_path, key_variables, options=options)
print(response)
# %%
