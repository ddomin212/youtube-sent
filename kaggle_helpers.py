import subprocess
import pandas as pd
import json
import os
import subprocess
import shutil


def get_sentiment(comments, folder_name, first_time):
    # run the bash script
    subprocess.run(['bash', 'kaggle.sh', folder_name, first_time])
    # continue with Python code
    print("The script has finished executing.")
    predictions = pd.read_csv(
        f"static/generated/{folder_name}/output/preds.csv", usecols=["comment_id", "questions", "negative"], lineterminator='\n')
    print(predictions.head(5))
    pred_counts = predictions.negative.value_counts().to_dict()
    quest_counts = predictions.questions.value_counts().to_dict()
    negatives, questions = [], []
    for item in comments:
        sent = predictions[predictions["comment_id"]
                           == item["comment_id"]].negative.values
        quest = predictions[predictions["comment_id"]
                            == item["comment_id"]].questions.values
        item["comment_sentiment"] = sent[0] if sent else 0
        if sent and sent[0] == 1:
            negatives.append(item)
        if quest and quest[0] == 1:
            questions.append(item)
    return quest_counts, pred_counts, negatives, questions


def init_kaggle(user_email):
    if not os.path.isdir(
            f"static/generated"):
        os.mkdir(f"static/generated")
    os.mkdir(f"static/generated/{user_email}")
    init_dataset(user_email)
    init_kernel(user_email)
    os.mkdir(f"static/generated/{user_email}/output")


def init_dataset(user_email):
    os.mkdir(f"static/generated/{user_email}/dataset")
    kaggle_metadata = {
        "title": f"youtube-sent-{user_email}",
        "id": f"dandominko/youtube-sent-{user_email}",
        "licenses": [
            {
                "name": "CC0-1.0"
            }
        ]
    }
    json.dump(kaggle_metadata, open(
        f"static/generated/{user_email}/dataset/dataset-metadata.json", "w"))


def init_kernel(user_email):
    os.mkdir(f"static/generated/{user_email}/kernel")
    kaggle_metadata = {
        "id": f"dandominko/youtube-{user_email}",
        "title": f"youtube-{user_email}",
        "code_file": "toxic.ipynb",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": True,
        "enable_internet": True,
        "keywords": ["gpu"],
        "dataset_sources": [f"dandominko/youtube-sent-{user_email}"],
        "kernel_sources": [],
        "competition_sources": []
    }
    subprocess.run(
        ['cp', 'toxic.ipynb', f'static/generated/{user_email}/kernel/toxic.ipynb'])
    json.dump(kaggle_metadata, open(
        f"static/generated/{user_email}/kernel/kernel-metadata.json", "w"))
