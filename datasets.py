import kaggle

# Set the API credentials
kaggle.api.authenticate()

# List all of your datasets and their IDs
datasets = kaggle.api.dataset_list()
for dataset in datasets:
    print(f"{dataset.ref} - {dataset.title} ({dataset.id})")