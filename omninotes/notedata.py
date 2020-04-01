import json
from typing import List, Optional
from omninotes.category import Category
from omninotes.attachment import Attachment

class NoteData:
    def __init__(self, content: str, title: Optional[str], alarm: Optional[int],
                 attachments: List[Attachment], category: Optional[Category], time_created: int,
                 time_modified: int, trashed: bool, archived: bool):
        self.content = content
        self.title = title
        self.alarm = alarm
        self.attachments = attachments
        self.category = category
        self.time_created = time_created
        self.time_modified = time_modified
        self.trashed = trashed
        self.archived = archived

    @staticmethod
    def parse_from_backup(file_contents, attachments_path):
        data = json.loads(file_contents)
        NoteData.validate(data)
        return NoteData(
            content=data.get("content", ""),
            title=data.get("title"),
            alarm=data.get("alarm"),
            attachments=Attachment.parse(data.get("attachmentsList"), attachments_path),
            category=Category(data["baseCategory"]) if "baseCategory" in data else None,
            time_created=data.get("creation"),
            time_modified=data.get("lastModification"),
            trashed=data.get("trashed", False),
            archived=data.get("archived", False)
        )

    @staticmethod
    def validate(data):
        # TODO: validation
        pass
