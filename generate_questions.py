import openai
import numpy as np
import pandas as pd

def generate_questions(context):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Write questions based on the text below\n\nText: {context}\n\nQuestions:\n1.",
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n\n"]
        )
        return response['choices'][0]['text']
    except:
        return ""