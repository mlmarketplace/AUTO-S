import os
from openai import OpenAI

client = OpenAI()

def diagnose_issue(user_query: str, error: str) -> str:
    """
    Uses LLM to diagnose Terraform issue
    """

    prompt = f"""
You are a DevOps expert.

User Query:
{user_query}

Terraform Error:
{error}

Tasks:
1. Explain the issue clearly
2. Identify root cause
3. Suggest a fix
4. Provide example Terraform correction

Keep it concise and actionable.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert in Terraform and cloud debugging."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content