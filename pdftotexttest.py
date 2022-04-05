import pdftotext

# Load your PDF
with open("0001545 - United States of America v. Califo.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)

for page in pdf:
    print(page)
