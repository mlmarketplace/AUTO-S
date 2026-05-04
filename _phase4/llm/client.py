# llm/client.py

import os
import json
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -----------------------------
# LLM CALL
# -----------------------------
def call_llm(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-5.3",
            messages=[
                {"role": "system", "content": "You are a precise Terraform support assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        })


# -----------------------------
# PROMPT LOADER
# -----------------------------
def load_prompt(version: str) -> str:
    base_path = os.path.join(os.path.dirname(__file__), "prompts")

    prompt_files = {
        "v1": "v1_basic.txt",
        "v2": "v2_structured.txt",
        "v3": "v3_safety.txt"
    }

    file_name = prompt_files.get(version, "v3_safety.txt")
    file_path = os.path.join(base_path, file_name)

    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "User query: {query}"


# -----------------------------
# SAFE JSON PARSER
# -----------------------------
def safe_parse(response: str) -> dict:
    try:
        return json.loads(response)
    except Exception:
        return {
            "status": "error",
            "message": "Invalid JSON response from LLM",
            "raw_output": response
        }