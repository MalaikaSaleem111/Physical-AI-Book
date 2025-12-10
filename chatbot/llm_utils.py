import os
import logging
from typing import List, Dict
from dotenv import load_dotenv

# -------------------------------------------------
# LOAD ENV
# -------------------------------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

logger = logging.getLogger(__name__)

# -------------------------------------------------
# CLIENTS
# -------------------------------------------------
openai_client = None
if LLM_PROVIDER == "openai":
    if not OPENAI_API_KEY:
        raise RuntimeError("❌ OPENAI_API_KEY missing in .env")

    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
    except ImportError:
        raise ImportError("❌ Install OpenAI SDK: pip install openai")

cohere_client = None
if LLM_PROVIDER == "cohere":
    if not COHERE_API_KEY:
        raise RuntimeError("❌ COHERE_API_KEY missing in .env")

    import cohere
    cohere_client = cohere.Client(api_key=COHERE_API_KEY)


# -------------------------------------------------
# CORE CHAT FUNCTION (USED BY RAG)
# -------------------------------------------------
def generate_chat_response(
    messages: List[Dict],
    temperature: float = 0.2,
    max_tokens: int = 400
) -> str:
    """
    Generate a response using OpenAI or Cohere.
    Messages format:
    [
      {"role": "system", "content": "..."},
      {"role": "user", "content": "..."}
    ]
    """

    # ================= OPENAI =================
    if LLM_PROVIDER == "openai":
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"OpenAI LLM error: {e}")
            raise RuntimeError("OpenAI LLM generation failed")

    # ================= COHERE =================
    elif LLM_PROVIDER == "cohere":
        try:
            system_prompt = ""
            user_prompt = ""

            for msg in messages:
                if msg["role"] == "system":
                    system_prompt = msg["content"]
                elif msg["role"] == "user":
                    user_prompt = msg["content"]

            # Try multiple model names in order of preference
            model_names = [
                "command-r-plus-08-2024",
                "command-r-08-2024",
                "command-light",
                "command"
            ]

            response = None
            for model_name in model_names:
                try:
                    response = cohere_client.chat(
                        model=model_name,
                        message=user_prompt,
                        preamble=system_prompt,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    break  # If successful, break out of the loop
                except Exception as e:
                    # Log the error but try the next model
                    logger.warning(f"Cohere model {model_name} failed: {e}")
                    continue

            if response is None:
                raise Exception("All Cohere models failed")

            return response.text.strip()

        except Exception as e:
            logger.error(f"Cohere LLM error: {e}")
            raise RuntimeError("Cohere LLM generation failed")

    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")
