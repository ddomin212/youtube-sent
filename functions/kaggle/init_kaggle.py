import json
import os
import subprocess


def init_kaggle(user_email: str):
    """
    Initializes a Kaggle notebook for the given user email.

    Args:
        user_email (str): The email of the user to initialize the notebook for.
    """
    if not os.path.isdir("static/generated"):
        os.mkdir("static/generated")
    os.mkdir(f"static/generated/{user_email}")
    init_dataset(user_email)
    init_kernel(user_email)
    os.mkdir(f"static/generated/{user_email}/output")


def init_dataset(user_email: str):
    """
    Initializes a Kaggle dataset for the given user email.

    Args:
        user_email (str): The email of the user to initialize the dataset for.
    """
    os.mkdir(f"static/generated/{user_email}/dataset")
    kaggle_metadata = {
        "title": f"youtube-sent-{user_email}",
        "id": f"dandominko/youtube-sent-{user_email}",
        "licenses": [{"name": "CC0-1.0"}],
    }
    json.dump(
        kaggle_metadata,
        open(
            f"static/generated/{user_email}/dataset/dataset-metadata.json",
            "w",
            encoding="utf-8",
        ),
    )


def init_kernel(user_email: str):
    """
    Initializes a Kaggle kernel for the given user email.

    Args:
        user_email (str): The email of the user to initialize the kernel for.
    """
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
        [
            "cp",
            "toxic.ipynb",
            f"static/generated/{user_email}/kernel/toxic.ipynb",
        ],
        check=True,
    )
    json.dump(
        kaggle_metadata,
        open(
            f"static/generated/{user_email}/kernel/kernel-metadata.json",
            "w",
            encoding="utf-8",
        ),
    )
