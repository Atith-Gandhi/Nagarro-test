from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import os
from utils import text_to_dict

def parse_prompt(user_prompt):
    anthropic_api_key = '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'

    anthropic = Anthropic(
        api_key= anthropic_api_key,
    )

    completion = anthropic.completions.create(
        model="claude-2.1",
        max_tokens_to_sample=350,
        prompt=f"{HUMAN_PROMPT} Get four fields - task_type(Create, Edit, Delete, List), task_name(3-4 words), timestamp(proper timestamp format), and priority of the next sentence. \"{user_prompt}\" {AI_PROMPT}",
    )
    print(completion.completion)
    try:
        dict_response = text_to_dict(completion.completion)
        return dict_response
    except:
        return {"task_name": None, "timestamp": None, "priority": None}