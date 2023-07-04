DEFAULT_MAP_PROMPT_TEMPLATE_STRING = """I will give you text content, you will rewrite it and output that in a short summarized version of my text.
Keep the meaning the same. Ensure that the revised content has significantly fewer characters than the original text, and no more than 200 words, the fewer the better.
Only give me the output and nothing else.
Now, using the concepts above, summarize the following text. Respond in the Chinese::
{text}
"""


DEFAULT_REDUCE_PROMPT_TEMPLATE_STRING = """I will give you text content, you will rewrite it and output that in a short summarized version of my text.
Keep the meaning the same. Ensure that the revised content has significantly fewer characters than the original text, and no more than 200 words, the fewer the better.
Only give me the output and nothing else.
Now, using the concepts above, summarize the following text. Respond in the Chinese::
{text}
"""
