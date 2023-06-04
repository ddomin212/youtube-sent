"""
This module contains support function for the searchController.py file.

Functions:
- check_first_time(user_email): Checks if a user has used the application before by 
                                checking if a directory exists with the user's email 
                                address. If the directory does not exist, it creates it 
                                and initializes a Kaggle API client for the user.
- save_comments_to_csv(comments, user_email): Saves a list of comments to a 
                                            CSV file in the user's directory.
"""

import os
import pandas as pd
from functions import init_kaggle

def check_first_time(user_email):
    """
    Checks if a user has used the application before by checking if a directory exists 
    with the user's email address. If the directory does not exist, it creates it and initializes
    a Kaggle API client for the user.

    Args:
        user_email (str): The email address of the user.

    Returns:
        tuple: "no" if the directory already exists, "yes" if it was just created.
    """
    if os.path.exists(f"static/generated/{user_email}"):
        return "no"
    else:
        init_kaggle(user_email)
        return "yes"

def save_comments_to_csv(comments, user_email):
    """
    Saves a list of comments to a CSV file in the user's directory.

    Args:
        comments (dict): A list of comments to save.
        user_email (str): The email address of the user.

    Returns:
        tuple: A tuple containing the user's video history document and the video type.
    """
    comments_df = pd.DataFrame.from_dict(comments)
    comments_df.to_csv(f"static/generated/{user_email}/dataset/data.csv", index=False)
    return
