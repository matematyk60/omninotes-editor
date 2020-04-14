import re
from os.path import join
from typing import List

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
        Attachment.validate(data)
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
    def validate(data):
        #TODO: validation
        pass
