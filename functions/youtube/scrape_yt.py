import os
from typing import Any, Dict, List
from googleapiclient.discovery import build, Resource
from functions.youtube.scrape_helpers import *


all_comments: List[Dict[str, Any]] = []


def get_comments(video_id: str):
    """
    Given a YouTube video ID, retrieves the top-level comments for the video and returns
    them along with the video's title, description, and publish date.

    Args:
        video_id (str): The ID of the YouTube video to scrape.

    Returns:
        Tuple[List[Dict[str, Any]], Tuple[str, str, str]]: A tuple containing a list of
        dictionaries representing the top-level comments for the video, and a tuple
        containing the video's title, description, and publish date.
    """

    gapi_key = os.getenv("GAPI_KEY")

    # Create a youtube resource object
    youtube = build("youtube", "v3", developerKey=gapi_key)

    get_comments_helper(youtube, video_id, "")
    video_info = get_video_info(youtube, video_id)
    return (all_comments, video_info)


def get_comments_helper(youtube: Resource, video_id: str, token: str = ""):
    """
    Recursive function that retrieves the top-level comments for a given YouTube video.

    Args:
        youtube (Any): The YouTube resource object.
        video_id (str): The ID of the YouTube video to scrape.
        token (str, optional): The token to use when retrieving comments. Defaults to "".
    """

    global all_comments
    total_reply_count = 0
    token_reply = None

    if len(token.strip()) == 0:
        all_comments = []

    if token == "":
        video_response = (
            youtube.commentThreads()
            .list(part="snippet", maxResults=100, videoId=video_id, order="relevance")
            .execute()
        )
    else:
        video_response = (
            youtube.commentThreads()
            .list(
                part="snippet",
                maxResults=100,
                videoId=video_id,
                order="relevance",
                pageToken=token,
            )
            .execute()
        )

    # Loop comments from the video:
    for item in enumerate(video_response["items"]):
        # Append coments:
        cleaned_text_thread = clean_text(
            item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        )
        if len(cleaned_text_thread.strip()) > 10:
            comment_thread = {
                "comment_text": cleaned_text_thread,
                "comment_author": item["snippet"]["topLevelComment"]["snippet"][
                    "authorDisplayName"
                ],
                "comment_author_url": item["snippet"]["topLevelComment"]["snippet"][
                    "authorChannelUrl"
                ],
                "comment_author_image": item["snippet"]["topLevelComment"]["snippet"][
                    "authorProfileImageUrl"
                ],
                "comment_published_at": item["snippet"]["topLevelComment"]["snippet"][
                    "updatedAt"
                ],
                "comment_published_at_unix": convert_date_unix(
                    item["snippet"]["topLevelComment"]["snippet"]["updatedAt"]
                ),
                "comment_like_count": item["snippet"]["topLevelComment"]["snippet"][
                    "likeCount"
                ],
                "comment_id": item["snippet"]["topLevelComment"]["id"],
                "comment_parent_id": item["snippet"]["topLevelComment"]["id"],
            }
            all_comments.append(comment_thread)

        # Get total reply count:
        total_reply_count = item["snippet"]["totalReplyCount"]

        # If the comment has replies, get them:
        if total_reply_count > 0:
            # Get replies - first batch:
            replies_response = (
                youtube.comments()
                .list(part="snippet", maxResults=100, parentId=item["id"])
                .execute()
            )
            for reply in replies_response["items"]:
                # Append the replies to the main array:
                cleaned_text = clean_text(reply["snippet"]["textDisplay"])
                if len(cleaned_text.strip()) > 10:
                    comment = {
                        "comment_text": cleaned_text,
                        "comment_author": reply["snippet"]["authorDisplayName"],
                        "comment_author_url": reply["snippet"]["authorChannelUrl"],
                        "comment_author_image": reply["snippet"][
                            "authorProfileImageUrl"
                        ],
                        "comment_published_at": reply["snippet"]["updatedAt"],
                        "comment_published_at_unix": convert_date_unix(
                            reply["snippet"]["updatedAt"]
                        ),
                        "comment_like_count": reply["snippet"]["likeCount"],
                        "comment_id": reply["id"],
                        "comment_parent_id": item["id"],
                    }
                    all_comments.append(comment)

            # If the reply has a token for get more replies, loop those replies
            # and add those replies to the main array:
            while "nextPageToken" in replies_response:
                token_reply = replies_response["nextPageToken"]
                replies_response = (
                    youtube.comments()
                    .list(
                        part="snippet",
                        maxResults=100,
                        parentId=item["id"],
                        pageToken=token_reply,
                    )
                    .execute()
                )
                for reply in replies_response["items"]:
                    cleaned_text = clean_text(reply["snippet"]["textDisplay"])
                    if len(cleaned_text.strip()) > 10:
                        comment_more = {
                            "comment_text": cleaned_text,
                            "comment_author": reply["snippet"]["authorDisplayName"],
                            "comment_author_url": reply["snippet"]["authorChannelUrl"],
                            "comment_author_image": reply["snippet"][
                                "authorProfileImageUrl"
                            ],
                            "comment_published_at": reply["snippet"]["updatedAt"],
                            "comment_published_at_unix": convert_date_unix(
                                reply["snippet"]["updatedAt"]
                            ),
                            "comment_like_count": reply["snippet"]["likeCount"],
                            "comment_id": reply["id"],
                            "comment_parent_id": item["id"],
                        }
                        all_comments.append(comment_more)

    if "nextPageToken" in video_response:
        return get_comments_helper(youtube, video_id, video_response["nextPageToken"])
    # Remove empty elements added to the list "due to the return in both functions":
    all_comments = [x for x in all_comments if len(x) > 0]
    print("Fin")
    return []
