
import kaggle
import os

kaggle.api.authenticate()


data_file = "data.csv"

kaggle.api.dataset_upload_file(
    "/d/projects/data science/youtube_sent", data_file)
