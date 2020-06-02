import os
from time import time
from typing import Optional
from omninotes.category import Category
from omninotes.category_dump import CategoryDump
from omninotes.notedata import NoteData
from omninotes.importer import Importer
from omninotes.settings import Settings

class CliHelpers:
    @staticmethod
    def create_new_category(backups_path: str, title: str, color: str):
        id = int(time() * 1000)
        new_category = Category(id, title, color)
        dump = CategoryDump()
        for category in Category.parse_from_config_file(os.path.join(backups_path, "categories.ini")):
            if category.title == title:
                raise Exception(f"Category with title '{title}' already exists")
            dump.add(category)
        dump.add(new_category)
        dump.write_category_file(backups_path)

    @staticmethod
    def create_new_note(backups_path: str, title: Optional[str]):
        data = NoteData(
            content='',
            title=title,
            alarm=None,
            attachments=[],
            category=None,
            time_created=int(time() * 1000),
            time_modified=int(time() * 1000),
            trashed=False,
            archived=False,
            checklist=False,
            longitude=None,
            latitude=None
        )
        Importer.import_note(data, backups_path)

    @staticmethod
    def edit_settings(note_path: str, new_trashed: Optional[bool], new_archived: Optional[bool], new_category: Optional[str]):
        categories = Category.parse_from_config_file(os.path.join(note_path, "..", "categories.ini"))
        categories = { cat.title : cat for cat in categories}
        settings = Settings.parse_from_file(note_path, categories)
        settings.archived = new_archived if new_archived else settings.archived
        settings.trashed = new_trashed if new_trashed else settings.trashed
        if new_category:
            if new_category not in categories:
                raise Exception(f"Category with title [{new_category}] does not exist")
            else:
                settings.category = categories[new_category]
        settings.write_to_file(note_path)