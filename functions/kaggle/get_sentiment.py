"""
Handles sentiment analysis for YouTube video comments.

Functions:
    get_sentiment: Given a list of comments on a YouTube video, 
    returns the sentiment of each comment using the Kaggle API.
"""
import subprocess
from typing import Any, Dict, List
import pandas as pd


def get_counts(predictions: pd.DataFrame):
    """
    Get counts of questions and negatives from the predictions.

    @param predictions - Predictions in a pandas dataframe

    @return Tuple of integers : 1. Number of questions 2. Number of negatives
    """
    print(predictions.head(5))
    pred_counts = predictions.negative.value_counts().to_dict()
    quest_counts = predictions.questions.value_counts().to_dict()
    return quest_counts, pred_counts


def sort_comments(comments: List[Dict[str, Any]], predictions: pd.DataFrame):
    """
    Sort comments by sentiment and questions.

    @param comments - A list of comments to sort
    @param predictions - A pandas dataframe with the predictions for each comment

    @return A tuple of two lists : 1. A list of negatives 2. A list of questions
    """
    negatives, questions = [], []
    # Add comments to the list of comments.
    for item in comments:
        sent = predictions[
            predictions["comment_id"] == item["comment_id"]
        ].negative.values
        quest = predictions[
            predictions["comment_id"] == item["comment_id"]
        ].questions.values
        item["comment_sentiment"] = sent[0] if sent.size > 0 else 0
        # Add negatives to negatives list
        if sent.size > 0 and sent[0] == 1:
            negatives.append(item)
        # Add a question to the questions list
        if quest.size > 0 and quest[0] == 1:
            questions.append(item)
    return negatives, questions


def get_sentiment(comments: List[Dict[str, Any]], folder_name: str, first_time: str):
    """
    Given a the comments on a YouTube video,
    return comments tagged with sentiment and their respective counts.

    Args:
        text (str): The text to analyze.

    Returns:
        str: The sentiment of the text.
    """
    # run the bash script
    subprocess.run(
        ["bash", "functions/kaggle/kaggle.sh", folder_name, first_time], check=True
    )

    # We get the predicted values from a csv file. It is a bit hacky, but it's free and fast.
    predictions = pd.read_csv(
        f"static/generated/{folder_name}/output/preds.csv",
        usecols=["comment_id", "questions", "negative"],
        lineterminator="\n",
    )

    pred_counts, quest_counts = get_counts(predictions)
    negatives, questions = sort_comments(comments, predictions)

    return quest_counts, pred_counts, negatives, questions
