"""Loader that loads data from Dropbox."""
from typing import List

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.document_loaders.dropbox_file import DropboxFileLoader


class DropboxDirectoryLoader(BaseLoader):
    """Loader that loads data from Dropbox."""

    def __init__(self, dbx_directory_path: str, auth_code: str):
        """Initialize with target directory path and auth_code."""
        self.dbx_directory_path = dbx_directory_path
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

        docs = []
        with Dropbox(self.auth_code) as dbx:
            entries = list()
            hasmore = True
            while hasmore is True:
                res = dbx.files_list_folder(self.dbx_directory_path)
                entries.extend(res.entries)
                hasmore = res.has_more

            for entry in entries:
                if hasattr(entry, 'is_downloadable') and entry.is_downloadable is True:
                    loader = DropboxFileLoader(entry.path_display, self.auth_code)
                    docs.extend(loader.load())

        return docs
