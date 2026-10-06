"""
Script to execute the notebook in place and embed all output cells and graphs.
"""

import nbformat
from nbclient import NotebookClient

with open("Python/Loan_Credit_Risk_Analysis.ipynb", "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

client = NotebookClient(nb, timeout=600, kernel_name="python3")
client.execute()

with open("Python/Loan_Credit_Risk_Analysis.ipynb", "w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print("Notebook successfully executed and outputs saved in-place.")
