from googleapiclient.discovery import build
from functions.youtube.scrape_helpers import *
all_comments = []
API_URL = "https://api-inference.huggingface.co/models/s-nlp/roberta_toxicity_classifier"
headers = {"Authorization": "Bearer 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"}


def get_comments(video_id):
    # Replace YOUR_API_KEY with your actual API key
    gapi_key = 'AIzaSyA9YS74xcdXRqQvjcN8wV4rFbfUSm5Z66o'

    # Create a youtube resource object
    youtube = build('youtube', 'v3', developerKey=gapi_key)

    get_comments_helper(youtube, video_id, '')
    video_info = get_video_info(youtube, video_id)
    return (all_comments, video_info)


def get_comments_helper(youtube, video_id, token=''):
    """
    Recursive function that retrieves the comments (top-level ones) a given video has.
    """

    global all_comments
    totalReplyCount = 0
    token_reply = None

    if (len(token.strip()) == 0):
        all_comments = []

    if (token == ''):
        video_response = youtube.commentThreads().list(part='snippet', maxResults=100,
                                                       videoId=video_id, order='relevance').execute()
    else:
        video_response = youtube.commentThreads().list(part='snippet', maxResults=100,
                                                       videoId=video_id, order='relevance', pageToken=token).execute()

    # Loop comments from the video:
    for indx, item in enumerate(video_response['items']):
        # Append coments:
        cleaned_text_thread = clean_text(
            item['snippet']['topLevelComment']['snippet']['textDisplay'])
        if (len(cleaned_text_thread.strip()) > 10):
            comment_thread = {"comment_text": cleaned_text_thread,
                              "comment_author": item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                              "comment_author_url": item['snippet']['topLevelComment']['snippet']['authorChannelUrl'],
                              "comment_author_image": item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'],
                              "comment_published_at": item['snippet']['topLevelComment']['snippet']['updatedAt'],
                              "comment_published_at_unix": convert_date_unix(item['snippet']['topLevelComment']['snippet']['updatedAt']),
                              "comment_like_count": item['snippet']['topLevelComment']['snippet']['likeCount'],
                              "comment_id": item['snippet']['topLevelComment']['id'],
                              "comment_parent_id": item['snippet']['topLevelComment']['id']}
            all_comments.append(comment_thread)

        # Get total reply count:
        totalReplyCount = item['snippet']['totalReplyCount']

        # If the comment has replies, get them:
        if (totalReplyCount > 0):
            # Get replies - first batch:
            replies_response = youtube.comments().list(
                part='snippet', maxResults=100, parentId=item['id']).execute()
            for indx, reply in enumerate(replies_response['items']):
                # Append the replies to the main array:
                cleaned_text = clean_text(reply['snippet']['textDisplay'])
                if (len(cleaned_text.strip()) > 10):
                    comment = {"comment_text": cleaned_text,
                               "comment_author": reply['snippet']['authorDisplayName'],
                               "comment_author_url": reply['snippet']['authorChannelUrl'],
                               "comment_author_image": reply['snippet']['authorProfileImageUrl'],
                               "comment_published_at": reply['snippet']['updatedAt'],
                               "comment_published_at_unix": convert_date_unix(reply['snippet']['updatedAt']),
                               "comment_like_count": reply['snippet']['likeCount'],
                               "comment_id": reply['id'],
                               "comment_parent_id": item['id']}
                    all_comments.append(
                        comment)

            # If the reply has a token for get more replies, loop those replies
            # and add those replies to the main array:
            while "nextPageToken" in replies_response:
                token_reply = replies_response['nextPageToken']
                replies_response = youtube.comments().list(part='snippet', maxResults=100,
                                                           parentId=item['id'], pageToken=token_reply).execute()
                for indx, reply in enumerate(replies_response['items']):
                    cleaned_text = clean_text(reply['snippet']['textDisplay'])
                    if (len(cleaned_text.strip()) > 10):
                        comment_more = {"comment_text": cleaned_text,
                                        "comment_author": reply['snippet']['authorDisplayName'],
                                        "comment_author_url": reply['snippet']['authorChannelUrl'],
                                        "comment_author_image": reply['snippet']['authorProfileImageUrl'],
                                        "comment_published_at": reply['snippet']['updatedAt'],
                                        "comment_published_at_unix": convert_date_unix(reply['snippet']['updatedAt']),
                                        "comment_like_count": reply['snippet']['likeCount'],
                                        "comment_id": reply['id'],
                                        "comment_parent_id": item['id']}
                        all_comments.append(
                            comment_more)

    # Check if the video_response has more comments:
    if "nextPageToken" in video_response:
        return get_comments_helper(youtube, video_id, video_response['nextPageToken'])
    else:
        # Remove empty elements added to the list "due to the return in both functions":
        all_comments = [x for x in all_comments if len(x) > 0]
        print("Fin")
        return []