import logging
import os
from livekit.agents import JobContext, JobProcess, WorkerOptions, cli
from livekit.agents.job import AutoSubscribe
from livekit.agents.llm import ChatContext
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import cartesia, silero, llama_index, deepgram
from llama_index.core import StorageContext, load_index_from_storage, VectorStoreIndex
import shutil
from utils import get_apikey
from chat_agent import create_react_agent
import openai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-assistant")

# Get API keys from apikeys.yml
livekit_config = get_apikey('livekit')
DEEPGRAM_API_KEY = get_apikey('deepgram').get('api_key')
CARTESIA_API_KEY = get_apikey('cartesia').get('api_key')
openai.api_key = get_apikey('openai').get('api_key')

# Clear and recreate the storage directory for a fresh start
PERSIST_DIR = "./storage"
if os.path.exists(PERSIST_DIR):
    shutil.rmtree(PERSIST_DIR)
os.makedirs(PERSIST_DIR)

# Start with a fresh, empty index and persist it to create the file structure
index = VectorStoreIndex.from_documents([])
index.storage_context.persist(persist_dir=PERSIST_DIR)
react_agent = create_react_agent(MODEL="gpt-4o", index=index, persist_dir=PERSIST_DIR)


def prewarm(proc: JobProcess):
    logger.info("Prewarming VAD model")
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    chat_context = ChatContext().append(
        role="system",
        text=(
            "You are a helpful voice assistant that can answer questions about wikipedia pages. "
            "Be friendly and conversational."
        ),
    )

    logger.info(f"Connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logger.info(f"Connected to room {ctx.room.name}")

    participant = await ctx.wait_for_participant()
    logger.info(f"Starting voice assistant for participant {participant.identity}")

    stt = deepgram.STT(api_key=DEEPGRAM_API_KEY)
    tts = cartesia.TTS(api_key=CARTESIA_API_KEY)
    llm = llama_index.LLM(chat_engine=react_agent)

    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=stt,
        llm=llm,
        tts=tts,
        chat_ctx=chat_context,
    )

    agent.start(ctx.room, participant)

    await agent.say(
        "Hello! I am your friendly voice assistant. How can I help you today?",
        allow_interruptions=True,
    )


if __name__ == "__main__":
    os.environ["LIVEKIT_URL"] = livekit_config.get('url')
    os.environ["LIVEKIT_API_KEY"] = livekit_config.get('api_key')
    os.environ["LIVEKIT_API_SECRET"] = livekit_config.get('api_secret')

    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    )
