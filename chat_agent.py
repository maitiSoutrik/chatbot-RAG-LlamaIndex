from llama_index.core.tools.query_engine import QueryEngineTool
from llama_index.core.tools.types import ToolMetadata
from llama_index.core.tools import FunctionTool
from llama_index.readers.wikipedia import WikipediaReader
from llama_index.core.agent.react.base import ReActAgent
from llama_index.core.chat_engine.types import AgentChatResponse
from llama_index.llms.openai.base import OpenAI
import chainlit as cl
from chainlit.input_widget import Select, TextInput
import openai
from index_wikipages import create_index_from_query as create_index
from utils import get_apikey



index = None
agent = None

@cl.on_chat_start
async def on_chat_start():
    global index
    global agent
    # Settings
    settings = await cl.ChatSettings(
        [
            Select(
                id= "MODEL",
                label= "OpenAI - Model",
                values=["gpt-3.5-turbo", "gpt-4o-mini"],
                initial_index=0,
            ),
            TextInput(id="WikiPageRequest", label="Request Wikipage"),
        ]
    ).send()


def wikisearch_engine(index):
    query_engine = index.as_query_engine(
        response_mode="compact", verbose= True, similarity_top_k= 10
    )
    return query_engine


def create_react_agent(MODEL, index, persist_dir: str = None):
    query_engine_tools = [
        QueryEngineTool(
            query_engine=wikisearch_engine(index),
            metadata=ToolMetadata(
                name="Wikipedia",
                description="Useful for performing searches on the wikipedia knowledgebase",
            ),
        )
    ]

    openai.api_key = get_apikey('openai').get('api_key')
    llm = OpenAI(model=MODEL)
    def add_page(page_title: str) -> str:
        """
        Adds a new Wikipedia page to the knowledge base.
        Use this tool when the user asks to add, learn about, or index a new topic.
        The index will be updated and saved for future sessions.
        """
        try:
            page_documents = WikipediaReader().load_data(pages=[page_title], auto_suggest=False)
            for doc in page_documents:
                index.insert(doc)
            
            if persist_dir:
                index.storage_context.persist(persist_dir=persist_dir)
                return f"Successfully added and saved the page '{page_title}' to the knowledge base."
            else:
                return f"Successfully added page '{page_title}' to the current session. It will not be saved."

        except Exception as e:
            return f"Failed to add page '{page_title}': {e}"

    add_page_tool = FunctionTool.from_defaults(
        fn=add_page,
        name="add_wikipedia_page",
        description="Adds a new Wikipedia page to the knowledge base. Use this when the user asks to add, learn about, or index a new topic."
    )

    all_tools = query_engine_tools + [add_page_tool]

    agent = ReActAgent.from_tools(
        tools=all_tools,
        llm=llm,
        verbose=True,
    )

    return agent


@cl.on_settings_update
async def setup_agent(settings):
    global agent
    global index
    query = settings["WikiPageRequest"]
    if not isinstance(query, str):
        query = str(query)
    index = create_index(query)
    print("Index created for query:", query)

    print("on_settings_update", settings)
    MODEL = settings["MODEL"]
    if not isinstance(MODEL, str):
        MODEL = str(MODEL)
    agent = create_react_agent(MODEL, index)
    await cl.Message(
        author="Agent", content=f"""Wikipage(s) "{query}" successfully indexed"""
    ).send()


@cl.on_message
async def main(message: cl.Message):
    global agent
    if agent:
        print("Agent is available, processing message.")

    print("Received message:", message.content)

    if agent:
        print("Agent is available, processing message")
        response = await cl.make_async(agent.chat)(message.content)
        await cl.Message(author="Agent", content=response.response if isinstance(response, AgentChatResponse) else str(response)).send()
    else:
        print("Agent is not available!")