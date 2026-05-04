from _phase3.llm.client import call_llm

def handle_llm(query, prompt_template):
    prompt = prompt_template.format(query=query)
    return call_llm(prompt)