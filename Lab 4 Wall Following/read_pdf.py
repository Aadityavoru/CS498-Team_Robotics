import sys
import PyPDF2

def read_pdf(file_path):
    with open('pdf_content.txt', 'w', encoding='utf-8') as out_file:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for i, page in enumerate(reader.pages):
                out_file.write(f"--- PAGE {i+1} ---\n")
                out_file.write(page.extract_text() + "\n")

if __name__ == '__main__':
    read_pdf(sys.argv[1])
