import openai
import numpy as np
import pandas as pd

def get_answers(row):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Write questions based on the text below\n\nText: {row.Content}\n\nQuestions:\n{row.Questions}\n\nAnswers:\n1.",
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response['choices'][0]['text']
    except Exception as e:
        print (e)
        return ""