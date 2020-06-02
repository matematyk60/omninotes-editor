import json
import os
from os.path import join
from typing import List, Optional
from omninotes.category import Category
from omninotes.attachment import Attachment
import time

from omninotes.settings import Settings


class NoteData:
    def __init__(self, content: str, title: Optional[str], alarm: Optional[int],
                 attachments: List[Attachment], category: Optional[Category], time_created: int,
                 time_modified: int, trashed: bool, archived: bool, checklist: bool, longitude: float, latitude:float):
        self.content = content
        self.title = title
        self.alarm = alarm
        self.attachments = attachments
        self.category = category
        self.time_created = time_created
        self.time_modified = time_modified
        self.trashed = trashed
        self.archived = archived
        self.checklist = checklist
        self.longitude = longitude 
        self.latitude = latitude

    def settings(self):
        return Settings(
            self.trashed,
            self.archived,
            self.alarm,
            self.category,
            self.time_created,
            self.longitude,
            self.latitude
        )

    def category_map(self) -> dict:
        if not self.category:
            return {}
        return self.category.to_json()

    @staticmethod
    def parse_from_backup(file_contents, attachments_path):
        data = json.loads(file_contents)
        settings = Settings.parse_from_json(data)
        return NoteData(
            content=data.get("content", ""),
            title=data.get("title"),
            alarm=settings.alarm,
            attachments=Attachment.parse(data.get("attachmentsList"), attachments_path),
            category=settings.category,
            time_created=data.get("creation"),
            time_modified=data.get("lastModification"),
            trashed=settings.trashed,
            archived=settings.archived,
            checklist=data.get("checklist"),
            longitude=data.get("longitude"),
            latitude=data.get("latitude")
        )

    @staticmethod
    def parse_from_file_structure(content_file_contents, content_file_extension, note_path, categories):
        settings = Settings.parse_from_file(note_path, categories)
        return NoteData(
            content=content_file_contents,
            title=os.path.basename(note_path).split("_")[0],
            alarm=settings.alarm,
            attachments=Attachment.parse_from_file_structure(str(join(note_path, "attachments"))),
            category=settings.category,
            time_created=settings.time_created,
            time_modified=int(round(time.time() * 1000)),
            trashed=settings.trashed,
            archived=settings.archived,
            checklist=content_file_extension == ".cl",
            longitude=settings.longitude,
            latitude=settings.latitude
        )