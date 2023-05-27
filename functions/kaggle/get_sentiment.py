import subprocess
import pandas as pd
import subprocess


def get_sentiment(comments, folder_name, first_time):
    # run the bash script
    subprocess.run(['bash', 'functions/kaggle/kaggle.sh', folder_name, first_time])
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
        item["comment_sentiment"] = sent[0] if sent.size > 0 else 0
        if sent.size > 0 and sent[0] == 1:
            negatives.append(item)
        if quest.size > 0 and quest[0] == 1:
            questions.append(item)
    return quest_counts, pred_counts, negatives, questions



