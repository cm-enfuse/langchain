"""Loader that loads data from Dropbox."""
import os
import tempfile
from typing import List

from pydantic import BaseModel

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.document_loaders.unstructured import UnstructuredFileLoader


class DropboxFileLoader(BaseLoader):
    """Loader that loads data from Dropbox."""

    def __init__(self, dbx_file_path: str, auth_code: str):
        """Initialize with target directory path and auth_code."""
        self.dbx_file_path = dbx_file_path
        self.auth_code = auth_code  # Load from ENV?

    def load(self) -> List[Document]:
        """Load documents."""
        try:
            from dropbox import Dropbox
        except ImportError:
            raise ValueError(
                "Could not import dropbox python package. "
                "Please install it with `pip install dropbox`."
            )
        with Dropbox(self.auth_code) as dbx:
            with tempfile.TemporaryDirectory() as temp_dir:
                local_file_path = f'{temp_dir}/{self.dbx_file_path}'
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                dbx.files_download_to_file(local_file_path, self.dbx_file_path)
                loader = UnstructuredFileLoader(local_file_path)
                return loader.load()
