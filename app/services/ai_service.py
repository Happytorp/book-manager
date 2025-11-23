import logging

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from app.config import settings
llm = ChatGroq(model="llama-3.1-8b-instant",
               api_key=settings.GROQ_API_KEY)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
async def generate_text(prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
    """Generate text using ChatGroq"""
    try:
        logger.info(f"Sending prompt to ChatGroq for text generation with content - {prompt}")
        response = await llm.ainvoke(
            [HumanMessage(content=prompt)],
            max_tokens=max_tokens,
            temperature=temperature
        )
        logger.info("Text generation successful")
        return response.content
    except Exception as e:
        return f"[CHATGROQ ERROR] {e}"


async def summarize_text(text: str, max_tokens: int = 200) -> str:
    """Summarize text using ChatGroq"""
    prompt = (
        "You are a helpful assistant. Summarize the following book content into a concise paragraph (3-5 "
        "sentences):\n\n"
        f"{text}\n\nSummary:"
    )
    try:
        response = await llm.ainvoke(
            [
                SystemMessage(content="You are a helpful assistant that provides concise summaries."),
                HumanMessage(content=prompt)
            ],
            max_tokens=max_tokens
        )
        return response.content
    except Exception as e:
        return f"[SUMMARIZATION ERROR] {e}"
