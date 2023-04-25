from datetime import datetime
import re

def get_weeks(comments, video_unix, div):
    weeks = {"0": (0, 0), "1": (0, 0), "2": (0, 0), "3": (0, 0)}
    max_date = 0
    # compare comment release date to video release date and sort into weeks one to four
    for comment in comments:
        max_date = max(max_date, convert_date_unix(
            comment["comment_published_at"]))
        cw = get_week(
            video_unix, comment["comment_published_at"], div)
        if cw >= 0 and cw < 4:
            if comment["comment_sentiment"] == 0:
                weeks[str(cw)] = (weeks[str(cw)][0] + 1, weeks[str(cw)][1])
            else:
                weeks[str(cw)] = (weeks[str(cw)][0], weeks[str(cw)][1] + 1)
        else:
            if comment["comment_sentiment"] == 0:
                weeks["3"] = (weeks["3"][0] + 1, weeks["3"][1])
            else:
                weeks["3"] = (weeks["3"][0], weeks["3"][1] + 1)
    print(weeks)
    return weeks, get_week(video_unix, max_date, div, maxi=True)


def get_week(video_release, comment_str, div, maxi=False):
    # convert unix to datetime
    comment_date = datetime.fromtimestamp(convert_date_unix(
        comment_str) if maxi == False else comment_str)
    # get difference in days
    diff = comment_date - datetime.fromtimestamp(video_release)
    # get difference in weeks
    weeks = diff.days // div
    return weeks


def convert_date_unix(string_date):
    date_obj = datetime.strptime(string_date, '%Y-%m-%dT%H:%M:%SZ')
    unix_timestamp = int(date_obj.timestamp())
    return unix_timestamp


def clean_text(text):
    pattern = re.compile(r'&#\d{1,2};|<.*?>|&quot;|&amp;|&gt;|&lt;')
    clean_string = pattern.sub('', text)
    return clean_string


def get_video_info(youtube, video_id):
    response = youtube.videos().list(part="snippet", id=video_id).execute()

    # extract video title and description
    video_title = response["items"][0]["snippet"]["title"]
    video_desc = response["items"][0]["snippet"]["channelTitle"]
    video_publish = convert_date_unix(
        response["items"][0]["snippet"]["publishedAt"])

    return (video_title, video_desc, video_publish)


