# import os
# from tqdm import tqdm
# from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_community.vectorstores import Chroma
# from langchain_groq import ChatGroq
# from langchain.chains import RetrievalQA
# from crewai_tools import tool
# from dotenv import load_dotenv

# load_dotenv()

# groq_api_key = os.getenv("GROQ_API_KEY")
# directory_path = r"C:\Users\HP\Desktop\crew ai\project2\knowledgebase"


# @tool
# def setup_rag_system(
#     directory_path=r"C:\Users\HP\Desktop\crew ai\project2\knowledgebase",
#     groq_api_key="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",
#     groq_model="llama3-8b-8192",
# ):
#     """
#     Set up the RAG (Retrieval-Augmented Generation) system by loading documents,
#     creating embeddings, and setting up the QA chain.

#     Parameters:
#     - directory_path: The path to the directory containing the documents.
#     - groq_api_key: The API key for Groq.
#     - groq_model: The Groq model to use (default is "llama3-8b-8192").

#     Returns:
#     - A string message indicating the setup completion.
#     """

#     # Ensure the API key is provided
#     if not groq_api_key:
#         return "Groq API key must be provided"

#     # Load and split documents
#     documents = load_documents(directory_path)
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000, chunk_overlap=200)
#     splits = text_splitter.split_documents(documents)

#     # Create embeddings and vector store
#     vectorstore = create_embeddings_and_vectorstore(splits)

#     # Set up the retriever and QA chain
#     retriever = vectorstore.as_retriever()
#     llm = ChatGroq(api_key=groq_api_key, model_name=groq_model)
#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm, chain_type="stuff", retriever=retriever
#     )

#     # Store the objects globally for reuse
#     global stored_vectorstore, stored_qa_chain
#     stored_vectorstore = vectorstore
#     stored_qa_chain = qa_chain

#     return "RAG system setup complete."


# def load_documents(directory_path):
#     """
#     Load and split documents from a specified directory.
#     """

#     documents = []
#     files = os.listdir(directory_path)

#     for filename in tqdm(files, desc="Loading documents"):
#         file_path = os.path.join(directory_path, filename)
#         if filename.endswith(".pdf"):
#             loader = PyPDFLoader(file_path)
#         elif filename.endswith(".txt"):
#             loader = TextLoader(file_path)
#         elif filename.endswith(".docx"):
#             loader = Docx2txtLoader(file_path)
#         else:
#             print(f"Skipping unsupported file type: {filename}")
#             continue
#         documents.extend(loader.load_and_split())
#     return documents


# def create_embeddings_and_vectorstore(splits):
#     """
#     Create embeddings and store them in a vector store.
#     """

#     embedding_function = OllamaEmbeddings(model="mxbai-embed-large:latest")
#     persist_directory = r"C:\Users\HP\Desktop\crew ai\project2\db"
#     os.makedirs(persist_directory, exist_ok=True)

#     vectorstore = Chroma(
#         persist_directory=persist_directory,
#         embedding_function=embedding_function,
#     )

#     for split in tqdm(splits, desc="Creating embeddings and vector store"):
#         vectorstore.add_texts(texts=[split.page_content])

#     return vectorstore


# @tool
# def query_rag_system(query_text: str):
#     """
#     Query the documents using the RAG system with Groq LLM.

#     Parameters:
#     - query_text: The question to ask about the content.

#     Returns:
#     - The answer to the query based on the content.
#     """

#     if "stored_qa_chain" not in globals() or "stored_vectorstore" not in globals():
#         return "RAG system not initialized. Please run setup_rag_system() first."

#     try:
#         result = stored_qa_chain.invoke({"query": query_text})
#         return (
#             result["result"]
#             if isinstance(result, dict) and "result" in result
#             else str(result)
#         )
#     except Exception as e:
#         return f"An error occurred while processing the query: {str(e)}"

import os
from tqdm import tqdm
import pickle
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from crewai_tools import tool

PERSIST_DIRECTORY = r"C:\Users\HP\Desktop\crew ai\project2\db"
PROCESSED_FILES_PATH = r"C:\Users\HP\Desktop\crew ai\project2\processed_files.pkl"


@tool
def setup(directory_path, groq_api_key=None, groq_model="llama3-8b-8192"):
    """
    Set up the vector store and RetrievalQA chain for document processing.

    This function initializes the vector store, processes any new documents in the
    specified directory, and sets up a question-answering chain using the Groq API.

    Args:
        directory_path (str): The path to the directory containing documents.
        groq_api_key (str): The API key for accessing Groq services.
        groq_model (str, optional): The Groq model to use. Defaults to "llama3-8b-8192".

    Returns:
        tuple: A tuple containing the initialized vector store and QA chain.
    """
    if not groq_api_key:
        raise ValueError("Groq API key must be provided")

    if not os.path.exists(PERSIST_DIRECTORY):
        print("Creating vector store and processing all files...")
        vectorstore = create_new_vectorstore(directory_path)
    else:
        print("Loading existing vector store...")
        vectorstore = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=OllamaEmbeddings(
                model="mxbai-embed-large:latest"),
        )
        print("Updating vector store with new files...")
        update_vectorstore(vectorstore, directory_path)

    print("Creating retriever and QA chain...")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    llm = ChatGroq(api_key=groq_api_key, model_name=groq_model)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="map_reduce", retriever=retriever
    )

    print("Setup complete.")
    return vectorstore, qa_chain


def load_documents(directory_path, processed_files):
    """
    Load and split documents from the specified directory.

    Args:
        directory_path (str): The path to the directory containing documents.
        processed_files (set): A set of already processed file names.

    Returns:
        list: A list of documents ready to be split into chunks.
    """
    documents = []
    files = os.listdir(directory_path)

    for filename in tqdm(files, desc="Loading documents"):
        file_path = os.path.join(directory_path, filename)
        if filename in processed_files:
            continue
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif filename.endswith(".txt"):
            loader = TextLoader(file_path)
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        else:
            print(f"Skipping unsupported file type: {filename}")
            continue
        documents.extend(loader.load_and_split())
    return documents


def create_new_vectorstore(directory_path):
    """
    Create a new vector store by processing and embedding documents.

    Args:
        directory_path (str): The path to the directory containing documents.

    Returns:
        Chroma: The initialized vector store with embedded document chunks.
    """
    processed_files = set()
    documents = load_documents(directory_path, processed_files)

    print("Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)

    print("Creating embeddings and vector store...")
    vectorstore = create_embeddings_and_vectorstore(splits)

    with open(PROCESSED_FILES_PATH, 'wb') as f:
        pickle.dump(set(os.listdir(directory_path)), f)

    return vectorstore


def update_vectorstore(vectorstore, directory_path):
    """
    Update the existing vector store with new documents.

    Args:
        vectorstore (Chroma): The existing vector store.
        directory_path (str): The path to the directory containing documents.
    """
    processed_files = set()
    if os.path.exists(PROCESSED_FILES_PATH):
        with open(PROCESSED_FILES_PATH, 'rb') as f:
            processed_files = pickle.load(f)

    new_documents = load_documents(directory_path, processed_files)

    if new_documents:
        print("Splitting text for new documents...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(new_documents)

        print("Creating embeddings for new documents...")
        embedding_function = OllamaEmbeddings(model="mxbai-embed-large:latest")
        for split in tqdm(splits, desc="Adding new embeddings"):
            vectorstore.add_texts(texts=[split.page_content])

        new_processed_files = set(os.listdir(directory_path))
        processed_files.update(new_processed_files)
        with open(PROCESSED_FILES_PATH, 'wb') as f:
            pickle.dump(processed_files, f)
    else:
        print("No new documents found.")


def create_embeddings_and_vectorstore(splits):
    """
    Create embeddings for document chunks and initialize the vector store.

    Args:
        splits (list): A list of document chunks.

    Returns:
        Chroma: The initialized vector store with embedded document chunks.
    """
    embedding_function = OllamaEmbeddings(model="mxbai-embed-large:latest")
    os.makedirs(PERSIST_DIRECTORY, exist_ok=True)

    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_function,
    )

    for split in tqdm(splits, desc="Creating embeddings and vector store"):
        vectorstore.add_texts(texts=[split.page_content])

    return vectorstore


@tool
def query(vectorstore, qa_chain, query_text):
    """
    Query the initialized RetrievalQA system with a user-provided query.

    Args:
        vectorstore (Chroma): The vector store containing document embeddings.
        qa_chain (RetrievalQA): The question-answering chain initialized during setup.
        query_text (str): The user's query to be processed.

    Returns:
        str: The result of the query, or an error message if processing fails.
    """
    if not qa_chain:
        raise ValueError("RAG system not initialized. Call setup() first.")

    try:
        result = qa_chain.invoke({"query": query_text})
        return (
            result["result"]
            if isinstance(result, dict) and "result" in result
            else str(result)
        )
    except Exception as e:
        return f"An error occurred while processing the query: {str(e)}"


# Example usage
if __name__ == "__main__":
    vectorstore, qa_chain = setup(
        r"C:\Users\HP\Desktop\crew ai\project2\knowledgebase",
        groq_api_key="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",
    )
    result = query(
        vectorstore,
        qa_chain,
        """who is greatest chola and what is a Napoleon's personal life and give a contact management system Functional Requirements."""
    )
    print(result)
