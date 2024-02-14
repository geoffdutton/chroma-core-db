import pytest
import os
import chromadb
import shutil


def remove_persist_dir(persist_dir: str) -> None:
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir, ignore_errors=True)


def test_persist_reload_after_delete() -> None:
    persist_dir = './fixture_for_test_persist_reload_after_deleted/chroma'
    remove_persist_dir(persist_dir)

    chroma_client = chromadb.PersistentClient(path=persist_dir)

    collection = chroma_client.create_collection(name="my_collection")

    collection.add(
        embeddings=[[1, 2, 3], [4, 5, 6]],
        documents=["This is a document", "This is another document"],
        metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=["id1", "id2"]
    )

    assert os.path.exists(persist_dir), f"Persist directory {persist_dir} does not exist"

    # Remove in the same process
    remove_persist_dir(persist_dir)

    # Reload the client
    # Roughly trying to follow the langchain Chroma.from_tests(..)
    ## https://github.com/langchain-ai/langchain/blob/master/libs/community/langchain_community/vectorstores/chroma.py#L682
    chroma_client = chromadb.PersistentClient(path=persist_dir)

    try:
        chroma_client.get_collection(name="my_collection")
        assert False, "Collection should not exist"
    except ValueError:
        pass

    collection = chroma_client.create_collection(name="my_collection")

    collection.add(
        documents=["This is a document", "This is another document"],
        metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=["id1", "id2"]
    )
    assert os.path.exists(persist_dir), f"Persist directory {persist_dir} does not exist"
