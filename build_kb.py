import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

# ================================
# Load environment variables
# ================================
load_dotenv()  # loads .env file

groq_key = os.getenv("GROQ_API_KEY")

# STEP 1: Load Documents
def load_documents():
    file_path = "data/terms.txt"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found! Please add your terms.txt file.")
    
    loader = TextLoader(file_path)
    docs = loader.load()
    print(f"✅ Loaded {len(docs)} document(s)")
    return docs


# STEP 2: Split Documents
def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    print(f"✅ Split into {len(chunks)} chunks")
    return chunks


# STEP 3: Embed + Store in FAISS
def build_vector_store(chunks):
    # ✅ Use Hugging Face local embeddings — no quota or API key needed
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Build FAISS vectorstore from chunks
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Save locally
    os.makedirs("faiss_store", exist_ok=True)
    vectorstore.save_local("faiss_store")

    print("✅ FAISS vector store built and saved at 'faiss_store/'")


# MAIN
if __name__ == "__main__":
    docs = load_documents()
    chunks = split_documents(docs)
    build_vector_store(chunks)
