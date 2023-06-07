from contextlib import contextmanager
from typing import List, Tuple, Any
from google.cloud.exceptions import GoogleCloudError
from google.cloud.firestore import Client


@contextmanager
def firebase_query(db: Client, collection: str, query: List[Tuple[str, str, Any]]):
    if isinstance(query, tuple):
        query = [query]
    try:
        docs = db.collection(collection)
        for q in query:
            docs = docs.where(*q)
        docs = docs.stream()
        yield [doc.to_dict() for doc in docs]
    except GoogleCloudError:
        yield None
