from llama_index.core import VectorStoreIndex
from llama_index.readers.wikipedia import WikipediaReader
from wikipedia.exceptions import PageError, DisambiguationError
from llama_index.core.node_parser import SentenceSplitter
from utils import get_apikey
import openai

openai.api_key = get_apikey('openai').get('api_key')

def create_wikidocs(pages: list[str]):
    reader = WikipediaReader()
    documents = []
    for page_title in pages:
        try:
            page_documents = reader.load_data(pages=[page_title], auto_suggest=False)
            documents.extend(page_documents)
            print(f"Successfully loaded '{page_title}'")
        except PageError:
            print(f"Warning: Could not find Wikipedia page for '{page_title}'. Skipping.")
        except DisambiguationError as e:
            print(f"Warning: '{e.title}' is ambiguous. Skipping. Did you mean one of: {e.options[:5]}")
    return documents

def create_index_from_query(query: str):
    """Creates an index from a comma-separated query string of page titles."""
    pages = [page.strip() for page in query.split(',') if page.strip()]
    wikidocs = create_wikidocs(pages)
    if not wikidocs:
        print("No documents were loaded. Returning an empty index.")
        return VectorStoreIndex([])

    parser = SentenceSplitter(chunk_size=150, chunk_overlap=45)
    nodes = parser.get_nodes_from_documents(wikidocs)
    index = VectorStoreIndex(nodes)
    return index

def create_and_save_index_from_pages(pages: list[str], persist_dir: str):
    """Creates and saves an index from a list of pages."""
    wikidocs = create_wikidocs(pages)
    if not wikidocs:
        print("No documents were loaded. Aborting index creation.")
        return

    parser = SentenceSplitter(chunk_size=150, chunk_overlap=45)
    nodes = parser.get_nodes_from_documents(wikidocs)
    index = VectorStoreIndex(nodes)
    index.storage_context.persist(persist_dir=persist_dir)
    print(f"\nIndex for '{', '.join(pages)}' saved to '{persist_dir}'")

if __name__ == "__main__":
    wikipages = ["New York City", "London", "Tokyo", "2024 Summer Olympics"]
    PERSIST_DIR = "./storage"
    print(f"Creating and saving index for: {', '.join(wikipages)}")
    create_and_save_index_from_pages(wikipages, persist_dir=PERSIST_DIR)
    print("Done.")
