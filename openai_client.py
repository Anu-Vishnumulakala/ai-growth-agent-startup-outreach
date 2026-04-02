import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing in the .env file.")

    return OpenAI(api_key=api_key, timeout=60.0)
