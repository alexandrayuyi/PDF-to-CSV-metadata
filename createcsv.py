import os
import pandas as pd
import shutil
from PyPDF4 import PdfFileReader, PdfFileWriter

def copy_first_20_pages(pdf_files):
    # Create a new directory for the copied pdf files
    new_dir = 'Copied_PDFs'
    os.makedirs(new_dir, exist_ok=True)

    for pdf_file in pdf_files:
        # Open the pdf file
        with open(pdf_file, 'rb') as file:
            reader = PdfFileReader(file)

            # Create a PdfFileWriter object
            writer = PdfFileWriter()

            # Add the first 20 pages (or less if the pdf has less than 20 pages)
            for i in range(min(20, reader.getNumPages())):
                writer.addPage(reader.getPage(i))

            # Write the pages to a new pdf file
            with open(os.path.join(new_dir, pdf_file), 'wb') as output_pdf:
                writer.write(output_pdf)

# Get a list of all pdf files in the current directory
pdf_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.pdf')]

# Create a DataFrame with the pdf file names
df = pd.DataFrame(pdf_files, columns=['bundle:ORIGINAL'])

# Add new columns with None as their values
df['dc.title'] = None
df['dc.contributor.author'] = None
df['dc.date.issued'] = "2018-08-15"
df['local.tgrado.tutor'] = None
df['dc.description.abstract'] = None
df['dc.subject'] = None
df['dspace.entity.type'] = None

# Assign the type to all items in the 'dc.entity.type' column
df['dspace.entity.type'] = "Publication"

# Write the DataFrame to a csv file
df.to_csv('pdf_files.csv',encoding='utf-8', index=False)

copy_first_20_pages(pdf_files)