import re
from typing import Any, Dict, List
from datetime import datetime
from googleapiclient.discovery import Resource


def get_weeks(comments: List[Dict[str, Any]], video_unix: str, div: int):
    """
    Given a list of comments (in dictionary format), a video release date (in Unix timestamp format),
    and a divisor, returns a tuple containing a dictionary of sentiment counts for each week after
    the video release date, and the maximum number of comments in a single week.

    Args:
        comments (List[Dict[str, Any]]): The list of comments to analyze.
        video_unix (str): The Unix timestamp of the video release date.
        div (int): The divisor to use when calculating the number of weeks.

    Returns:
        Tuple[Dict[str, Tuple[int, int]], int]: A tuple containing a dictionary of sentiment counts
        for each week after the video release date, and the maximum number of comments in a single week.
    """
    weeks = {"0": (0, 0), "1": (0, 0), "2": (0, 0), "3": (0, 0)}
    max_date = 0
    # compare comment release date to video release date and sort into weeks one to four
    for comment in comments:
        publish_unix = convert_date_unix(comment["comment_published_at"])
        max_date = max(max_date, publish_unix)
        cw = get_week(video_unix, publish_unix, div)
        if cw >= 0 and cw < 4:
            weeks[str(cw)] = (
                (weeks[str(cw)][0] + 1, weeks[str(cw)][1])
                if comment["comment_sentiment"] == 0
                else (weeks[str(cw)][0], weeks[str(cw)][1] + 1)
            )
        elif comment["comment_sentiment"] == 0:
            weeks["3"] = (weeks["3"][0] + 1, weeks["3"][1])
        else:
            weeks["3"] = (weeks["3"][0], weeks["3"][1] + 1)
    return weeks, get_week(video_unix, max_date, div)


def get_week(video_release: str, comment_str_date: int, div: int):
    """
    Given a video release date (in Unix timestamp format), a comment date (in string format),
    and a divisor, returns the number of weeks between the two dates.

    Args:
        video_release (str): The Unix timestamp of the video release date.
        comment_str_date (int): The Unix timestamp of the comment.
        div (int): The divisor to use when calculating the number of weeks.
        maxi (bool, optional): Whether or not the comment date is already in Unix timestamp format.
            Defaults to False.

    Returns:
        int: The number of weeks between the two dates.
    """
    # convert unix to datetime
    comment_date = datetime.fromtimestamp(comment_str_date)
    # get difference in days
    diff = comment_date - datetime.fromtimestamp(int(video_release))
    return diff.days // div


def convert_date_unix(string_date: str):
    """
    Converts a string date in the format "%Y-%m-%dT%H:%M:%SZ" to a Unix timestamp.

    Args:
        string_date (str): The string date to convert.

    Returns:
        int: The Unix timestamp.
    """
    date_obj = datetime.strptime(string_date, "%Y-%m-%dT%H:%M:%SZ")
    return int(date_obj.timestamp())


def clean_text(text: str):
    """
    Cleans a block of text by removing newlines, extra whitespace, and HTML tags.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text.
    """
    pattern = re.compile(r"&#\d{1,2};|<.*?>|&quot;|&amp;|&gt;|&lt;")
    return pattern.sub("", text)


def get_video_info(youtube: Resource, video_id: str):
    """
    Given a YouTube video URL, returns a tuple containing the video's title,
    description, and publish date.

    Args:
        video_url (str): The URL of the YouTube video to scrape.

    Returns:
        Tuple[str, str, str]: A tuple containing the video's title, description,
        and publish date.
    """
    response = youtube.videos().list(part="snippet", id=video_id).execute()

    # extract video title and description
    video_title = response["items"][0]["snippet"]["title"]
    video_desc = response["items"][0]["snippet"]["channelTitle"]
    video_publish = convert_date_unix(response["items"][0]["snippet"]["publishedAt"])

    return (video_title, video_desc, video_publish)
