from PyPDF2 import PdfReader

# função para extrair o conteúdo de um arquivo .txt
def extract_txt(file):
    with open(file, "r") as f:
        return f.read()
    
def extract_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    print(text)
    return text

# teste
pdf_teste = "C:/Users/leona/brasas-movement-chat-ia/ms-embedding-documents/arquivos_teste/brasas_nossa_missao.pdf"
conteudo = extract_pdf(pdf_teste)
print(conteudo)