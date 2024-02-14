import pytest
import os
import chromadb
import shutil


def remove_persist_dir(persist_dir: str) -> None:
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir, ignore_errors=True)


def test_persist_reload_after_delete() -> None:
    persist_dir = './test_persist/db/chroma'
    remove_persist_dir(persist_dir)
    chroma_client = chromadb.PersistentClient(path=persist_dir)

    collection = chroma_client.create_collection(name="my_collection")

    collection.add(
        documents=["This is a document", "This is another document"],
        metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=["id1", "id2"]
    )

    assert os.path.exists(persist_dir), f"Persist directory {persist_dir} does not exist"
    remove_persist_dir(persist_dir)

    chroma_client = chromadb.PersistentClient(path=persist_dir)

    collection = chroma_client.get_collection(name="my_collection")

    collection.add(
        documents=["This is a document", "This is another document"],
        metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=["id1", "id2"]
    )
    assert os.path.exists(persist_dir), f"Persist directory {persist_dir} does not exist"
