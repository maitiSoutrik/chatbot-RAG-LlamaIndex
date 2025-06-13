# Chatbot with RAG using LlamaIndex and Chainlit

This project implements a chatbot that uses the Retrieval-Augmented Generation (RAG) pattern with LlamaIndex and Chainlit. The chatbot can answer questions based on a knowledge base created from Wikipedia articles.

## Features

- **Dynamic Knowledge Base:** Create a knowledge base from any set of Wikipedia articles on the fly.
- **Conversational AI:** Chat with an AI agent that can reason and answer questions based on the indexed documents.
- **Interactive UI:** A user-friendly chat interface built with Chainlit.
- **Customizable AI Model:** Choose between different OpenAI models (`gpt-3.5-turbo`, `gpt-4o-mini`).

## How it Works

1.  **Indexing:** When the application starts, you can specify a list of Wikipedia pages to be indexed. The application will fetch the content of these pages and create a vector index using LlamaIndex.
2.  **Chat:** Once the indexing is complete, you can ask the chatbot questions. The chatbot uses a ReAct agent to reason and retrieve relevant information from the indexed documents to generate an answer.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- An OpenAI API key

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API key:**

    Create a file named `apikeys.yml` in the root of the project and add your OpenAI API key:

    ```yaml
    openai:
      api_key: "YOUR_OPENAI_API_KEY"
    ```

### Running the Application

1.  **Run the Chainlit application:**

    ```bash
    chainlit run chat_agent.py -w
    ```

2.  **Open your browser:**

    Navigate to `http://localhost:8000` in your web browser.

3.  **Configure the chatbot:**

    -   In the settings panel, enter a query to specify the Wikipedia pages you want to index (e.g., "Cloud computing, Machine learning").
    -   Select the AI model you want to use.

4.  **Start chatting:**

    Once the indexing is complete, you can start asking the chatbot questions.

## Project Structure

```
.
├── .gitignore
├── apikeys.yml
├── chat_agent.py
├── index_wikipages.py
├── requirements.txt
└── utils.py
```

-   `chat_agent.py`: The main Chainlit application.
-   `index_wikipages.py`: Handles the creation of the Wikipedia knowledge base.
-   `utils.py`: Utility functions, such as retrieving the API key.
-   `requirements.txt`: The project dependencies.
-   `apikeys.yml`: Configuration file for API keys.

## Dependencies

-   `llama_index`
-   `openai`
-   `pydantic`
-   `PyYAML`
-   `llama-index-readers-wikipedia`
-   `wikipedia`
-   `chainlit`
