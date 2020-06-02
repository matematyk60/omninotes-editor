import re
import os
from os.path import join
from time import time
from typing import List
import magic


class Attachment:
    def __init__(self, id: int, mime: str, uri: str, attachments_path: str):
        self.id = id
        self.mime = mime
        self.uri = uri
        self.file_path = join(attachments_path, self.get_file_name())

    def get_file_name(self) -> str:
        regex = r".*/it.feio.android.omninotes/files/(.*)"
        match = re.match(regex, self.uri)
        return match.group(1)

    @staticmethod
    def parse(data, attachments_path) -> list:
        if not data:
            return []
        result = []
        for attachment in data:
            result.append(
                Attachment(
                    id=attachment["id"],
                    mime=attachment["mime_type"],
                    uri=attachment["uriPath"],
                    attachments_path=attachments_path)
            )
        return result

    @staticmethod
    def parse_from_file_structure(attachments_path) -> list:
        attachments = []
        with os.scandir(attachments_path) as entries:
            for entry in entries:
                if entry.is_file:
                    attachments.append(
                        Attachment(
                            id=int(time() * 1000),
                            mime=magic.Magic(mime=True).from_file(entry.path),
                            uri="content://it.feio.android.omninotes.authority/external_files/Android/data/it.feio.android.omninotes/files/" + entry.name,
                            attachments_path=attachments_path
                        )
                    )
                else:
                    pass
        return attachments

    def uri_with_prefix(self, prefix):
        splitted = self.uri.split("/")
        splitted_size = len(splitted)
        file_name = splitted[-1]

        prefixed = f"{prefix}_{file_name}"
        splitted.pop(splitted_size - 1)
        splitted.insert(splitted_size - 1, prefixed)

        return "/".join(splitted)

