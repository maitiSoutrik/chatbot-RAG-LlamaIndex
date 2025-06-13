from llama_index.core import VectorStoreIndex, download_loader
from llama_index.readers.wikipedia import WikipediaReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.program.openai import OpenAIPydanticProgram
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel
from utils import get_apikey
import openai

openai.api_key = get_apikey()

# define the data model in pydantic
class WikiPageList(BaseModel):
    "Data model for WikiPageList"
    pages: list[str]

def wikipage_list(query: str) -> WikiPageList:
    prompt_template_str = """
    Please extract the list of Wikipedia pages from the following query.
    Return the list of pages as a JSON object with a single key 'pages'.
    Query: {query}
    """

    program = OpenAIPydanticProgram.from_defaults(
        output_cls=WikiPageList,
        prompt_template_str=prompt_template_str,
        verbose=True,
    )

    wikipage_requests = program(query=query)
    return wikipage_requests

def create_wikidocs(wikipage_requests):
    reader = WikipediaReader()
    documents = reader.load_data(pages=wikipage_requests)
    return documents

def create_index(query: str):
    wikipages = wikipage_list(query)
    wikidocs = create_wikidocs(wikipages)
    parser = SentenceSplitter(chunk_size=150, chunk_overlap=45)
    nodes = parser.get_nodes_from_documents(wikidocs)
    index = VectorStoreIndex(nodes)
    return index

if __name__ == "__main__":
    query = "/get wikipages: london, birmingham, new york"
    index = create_index(query)
    print("INDEX CREATED", index)
