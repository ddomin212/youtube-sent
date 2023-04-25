def add_to_firebase(data, video_id, user_uid, db):
    # Get a reference to the document collection
    users_ref = db.collection('history')
    # Create a document
    doc_ref = users_ref.document(str(video_id) + "|" + str(user_uid))
    print(data)
    doc_ref.set(data)