from langchain_community.document_loaders import UnstructuredMarkdownLoader , PyPDFLoader
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunking_docs(folder_path:str|Path)->list[Document]:
    path=Path(folder_path)
    all_documents=[]
    for file in path.glob("*"):
        if not file.is_file():
            continue
        loader=None
        if file.suffix.lower()==".md":
            loader=UnstructuredMarkdownLoader(file_path=str(file))
        elif file.suffix.lower()==".pdf":
            loader=PyPDFLoader(file_path=str(file))
        if loader:
            all_documents.extend(loader.load())
    if not all_documents:
        return []

    text_splitter=RecursiveCharacterTextSplitter(separators=["\n\n","\n"," ",""],
                                                 chunk_size=700,
                                                 chunk_overlap=180
                                                 )
    chunks=text_splitter.split_documents(all_documents)

    return chunks    


if __name__=="__main__":
    test_folder=r"E:\AdvancedProjects\CodeSense\assets"
    chunking=chunking_docs(test_folder)
    for i , chunk in enumerate(chunking):
        print(f"Chunks : {i}")
        print(50*"#")
        print(chunk.page_content[:500])