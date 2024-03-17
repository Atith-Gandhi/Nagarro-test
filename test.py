from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import os

def text_to_dict(text):
    lines = text.strip().split('\n')
    result = {}
    for line in lines:
        if ': ' not in line:
            continue
        key, value = line.split(': ', 1)
        if value.lower() == 'null':
            value = None
        result[key] = value
    return result

anthropic_api_key = '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'

anthropic = Anthropic(
    api_key= anthropic_api_key,
)

completion = anthropic.completions.create(
    model="claude-2.1",
    max_tokens_to_sample=350,
    prompt=f"{HUMAN_PROMPT} Get four fields - task_type(Create, Edit, Delete, List), task_name, timestamp(proper timestamp format), and priority of the next sentence. \"Create a new task where I have to get the boxes by 7pm 16th March.\" {AI_PROMPT}",
)
print(completion.completion)
print(text_to_dict(completion.completion))