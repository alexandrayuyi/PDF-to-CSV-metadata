import os
import PyPDF2
import requests
import csv

# Define the headers
headersID = ['filename', 'source id']
headersInfo = ['filename', 'dc.title', 'dc.contributor.author', 'local.tgrado.tutor', 'dc.date.issued', 'dc.subject', 'dc.description.abstract', 'dspace.entity.type']
titles = []
authors = []
tutors = []
dates = []
subjects = []
summaries = []

# Open the CSV file in write mode



    # Write the data
    # Replace the following line with your actual data
    #data = ['filename1', 'source id1', 'autor1', 'tutor1', 'date1', 'subject1', 'summary1']
    #writer.writerow(data)

keywords = ['palabras claves', 'Palabras claves','Palabras Claves', 'descriptores', 'Descriptores', 'escuela', 'Escuela', 'ESCUELA', 'ACTA DE APROBACIÓN']
antikeywords = ['indice', 'Índice', 'INDICE', 'ÍNDICE']

def create_cropped_pdf(pdf_list, output_dir):
    
    new_dir = output_dir
    os.makedirs(new_dir, exist_ok=True)

    for pdf_file in pdf_list:
        # Open the original pdf file
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            # Create a PdfFileWriter object for the cropped pdf
            cropped_writer = PyPDF2.PdfWriter()

            #for i in range(min(20, len(reader.pages))):
                #cropped_writer.add_page(reader.pages[i])

            # Loop through all the pages in the original pdf
            for page_number in range(len(reader.pages)):
                page = reader.pages[page_number]

                # If the keyword is found in the page, add it to the cropped pdf
                
                text = page.extract_text()
                if (any(keyword in text for keyword in keywords) and (not any(antikeyword in text for antikeyword in antikeywords))):
                    cropped_writer.add_page(page)

            # Write the cropped pdf file
            with open(os.path.join(new_dir, pdf_file), 'wb') as output_pdf:
                cropped_writer.write(output_pdf)

def create_sources(croppedlist):

    source_ids = []
    for croppedpdf in croppedlist:
                
        files = [
                    ('file', ('file', open(croppedpdf, 'rb'), 'application/octet-stream'))
                ]
        headers = {
                'x-api-key': 'sec_kNQEr5wVKGqMTPJL0cOq672odYFcGPqR'
                }

        response = requests.post(
                    'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

        if response.status_code == 200:
            print('Source ID:', response.json()['sourceId'])
            try:
                source_ids.append(response.json()['sourceId'])
            except:
                source_ids.append(' ')
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)
    
    with open('source_IDs.csv', 'w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)

         # Write the headers
        writer.writerow(headersID)
    
        for i in range(len(source_ids)):
            data = [croppedlist[i], source_ids[i]]
            writer.writerow(data)



def create_chat(source, croppedlist):
    
    for source_id in source:
        headers = {
                            'x-api-key': 'sec_kNQEr5wVKGqMTPJL0cOq672odYFcGPqR',
                            "Content-Type": "application/json",
                        }

        data = {
                        'sourceId': source_id,
                        'messages': [
                                {
                                    'role': "user",
                                    'content': """Extract the title in title format, the author first name and surname, the tutor's title, first name and surname, the date issued and the subjects, in spanish. Do it so in spanish and do no redact anythind new yourself. Please deliver it as this example: 
                                    titulo: Desarrollo de un sistema para la Universidad de Carabobo
                                    autor: Maria Perez
                                    tutor: Dr. Juan Perez
                                    fecha: 2019-01-01
                                    categorías: Ingeniería de Sistemas
                                    """,
                                }
                            ]
                        }

        response2 = requests.post(
                            'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

        if response2.status_code == 200:
            print('Result:', response2.json()['content'])
            try:
                titles.append(response2.json()['content'].split('\n')[0])
            except:
                titles.append(' ')
            try:
                authors.append(response2.json()['content'].split('\n')[1])
            except:
                authors.append(' ')
            try:
                tutors.append(response2.json()['content'].split('\n')[2])
            except:
                tutors.append(' ')
            try:
                dates.append(response2.json()['content'].split('\n')[3])
            except:
                dates.append(' ')
            try:
                subjects.append(response2.json()['content'].split('\n')[4])
            except:
                subjects.append(' ')
        else:
            print('Status:', response2.status_code)
            print('Error:', response2.text)

        data = {
                            'sourceId': source_id,
                            'messages': [
                                {
                                    'role': "user",
                                    'content': "please extract the summary in spanish. Do not redact anything yourself",
                                }
                            ]
                        }

        response3 = requests.post(
                            'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

        if response3.status_code == 200:
            print('Result:', response3.json()['content'])
            try:
                summaries.append(response3.json()['content'].replace('\n', ''))
            except:
                summaries.append(' ')
                            
        else:
            print('Status:', response3.status_code)
            print('Error:', response3.text)
            
    with open('info.csv', 'w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the headers
        writer.writerow(headersInfo)
        for i in range(len(source)):
            try:
                filename = croppedlist[i]
            except:
                filename = ' '
            try:
                title = titles[i]
            except:
                title = ' '
            try:
                author = authors[i]
            except:
                author = ' '
            try:
                tutor = tutors[i]
            except:
                tutor = ' '
            try:
                date = dates[i]
            except:
                date = ' '
            try:
                subject = subjects[i]
            except:
                subject = ' '
            try:
                summary = summaries[i]
            except:
                summary = ' '
            try:
                data = [filename, title, author, tutor, date, subject, summary, 'Publication']
            except:
                continue


# Use the function to create a cropped pdf from an original pdf
#create_cropped_pdf(pdf_files)
                
def menu():
    while True:
        print("1. Create cropped PDF list")
        print("2. Create batch of sources")
        print("3. Create batch of chats")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            pdf_files = input("Enter the path of the directory containing the pdfs: ")
            pdf_files.replace('\\', '/')
            pdf_output_dir = input("Enter the path of the directory to write the pdfs: ")
            pdf_output_dir.replace('\\', '/')
            pdflist = [f for f in os.listdir(pdf_files) if os.path.isfile(f) and f.endswith('.pdf')]
            create_cropped_pdf(pdflist, pdf_output_dir)
            print("Cropped PDFs created successfully")
        elif choice == '2':
            pdf_files = input("Enter the path of the directory containing the pdfs: ")
            pdf_files.replace('\\', '/')
            pdflist = [f for f in os.listdir(pdf_files) if os.path.isfile(f) and f.endswith('.pdf')]
            create_sources(pdflist)
            print("Sources created successfully")
        elif choice == '3':
            pdf_files = input("Enter the path of the directory containing the pdfs: ")
            pdf_files.replace('\\', '/')
            pdflist = [f for f in os.listdir(pdf_files) if os.path.isfile(f) and f.endswith('.pdf')]
            sources = []
            with open('source_IDs.csv', 'r', newline='',encoding='utf-8') as file:
                reader = csv.reader(file)
                # Skip the header
                next(reader)

                for row in reader:
                    sources.append(row[1])
            create_chat(sources, pdflist)
            print("Chats created successfully")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

# Call the menu function
menu()
                
