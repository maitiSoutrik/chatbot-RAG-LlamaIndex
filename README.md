# Chatbot with RAG using LlamaIndex and Chainlit

This project implements a chatbot that uses the Retrieval-Augmented Generation (RAG) pattern with LlamaIndex and Chainlit. The chatbot can answer questions based on a knowledge base created from Wikipedia articles.

## Chatbot (Chainlit)

![Chat RAG Architecture](illustrations/Chat-RAG%20_%20Mermaid%20Chart-2025-07-03-225535.png)

### Key Features

- **Dynamic Knowledge Base:** Create a knowledge base from any set of Wikipedia articles on the fly.
- **Conversational AI:** Chat with an AI agent that can reason and answer questions based on the indexed documents.
- **Interactive UI:** A user-friendly chat interface built with Chainlit.
- **Customizable AI Model:** Choose between different OpenAI models (`gpt-3.5-turbo`, `gpt-4o-mini`).

### How it Works

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




## Voice Agent (LiveKit)

![Voice RAG Architecture](illustrations/Voice-RAG%20_%20Mermaid%20Chart-2025-07-03-225140.png)

The repository now includes a real-time voice-driven agent located in `livekit_voice_agent.py`.

### Running the voice agent

```bash
python livekit_voice_agent.py --room <ROOM_NAME> --token <ACCESS_TOKEN>
```

1. Start a LiveKit server (cloud or self-hosted).
2. Generate an access token for the target room.
3. Run the command above and join the same room from your browser or client. Speak naturally and the agent will respond in real-time.

### How it works

The voice agent continuously receives audio from the room, transcribes it with Deepgram, answers with the ReAct-powered RAG pipeline (same as the chat agent) and streams the response back using the Cartesia TTS service.

## Dynamic Knowledge Base

Each session starts with **no** pre-existing index. Whenever you ask about a concept that is not in the index, the agent will automatically fetch the relevant Wikipedia page, ingest it and update the vector store on the fly so that subsequent questions are answered with the new knowledge.

## Configuration

Create `apikeys.yml` in the project root with the following structure:

```yaml
openai:
  api_key: "YOUR_OPENAI_API_KEY"
livekit:
  url: "https://your-livekit-server"
  api_key: "YOUR_LIVEKIT_API_KEY"
  api_secret: "YOUR_LIVEKIT_API_SECRET"
deepgram:
  api_key: "YOUR_DEEPGRAM_API_KEY"
cartesia:
  api_key: "YOUR_CARTESIA_API_KEY"
```

Be sure to restart the application after editing the file.

## Dependencies

The following Python packages are required for both the Chainlit chatbot and the LiveKit voice agent:

- `llama_index`
- `openai`
- `pydantic`
- `PyYAML`
- `llama-index-readers-wikipedia`
- `wikipedia`
- `chainlit`
- `livekit`
- `deepgram-sdk`
- `cartesia`

