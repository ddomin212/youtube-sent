import requests
import json
import asyncio
import pickle

comments = pickle.load(
    (open("static/generated/comments_ucet.pc2122@gmail.com.pkl", "rb")))


print(comments)


API_URL = "https://api-inference.huggingface.co/models/s-nlp/roberta_toxicity_classifier"
headers = {"Authorization": "Bearer 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"}


async def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    print(response.status_code)
    return response.json()

for comment in comments[:50]:
    output = asyncio.run(query({
        "inputs": comment['comment_text'], "wait_for_model": True}))
    print(output)
