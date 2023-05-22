import json
import os
import subprocess


def init_kaggle(user_email):
    if not os.path.isdir("static/generated"):
        os.mkdir("static/generated")
    os.mkdir(f"static/generated/{user_email}")
    init_dataset(user_email)
    init_kernel(user_email)
    os.mkdir(f"static/generated/{user_email}/output")


def init_dataset(user_email):
    os.mkdir(f"static/generated/{user_email}/dataset")
    kaggle_metadata = {
        "title": f"youtube-sent-{user_email}",
        "id": f"dandominko/youtube-sent-{user_email}",
        "licenses": [{"name": "CC0-1.0"}],
    }
    json.dump(
        kaggle_metadata,
        open(f"static/generated/{user_email}/dataset/dataset-metadata.json", "w"),
    )


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
        "competition_sources": [],
    }
    subprocess.run(
        ["cp", "toxic.ipynb", f"static/generated/{user_email}/kernel/toxic.ipynb"]
    )
    json.dump(
        kaggle_metadata,
        open(f"static/generated/{user_email}/kernel/kernel-metadata.json", "w"),
    )
