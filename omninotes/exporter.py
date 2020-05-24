import glob
import json
import os
import pathlib
import shutil
from omninotes.category import Category

from time import time, sleep

from omninotes.notedata import NoteData


class Exporter:
    def __init__(self, source_path: str):
        self.source_path = source_path
        self.notes = []
        self.categories = []
        self.load_categories()
        self.load_notes()

    def load_categories(self):
        self.categories = {category.title: category for category in
                           Category.parse_from_config_file(os.path.join(self.source_path, "categories.ini"))}

    def load_notes(self):
        with os.scandir(self.source_path) as entries:
            for entry in entries:
                if os.path.isdir(entry.path):
                    text_content_files = glob.glob(f"{entry.path}/*.txt")
                    checklist_content_files = glob.glob(f"{entry.path}/*.cl")
                    content_files = text_content_files + checklist_content_files
                    if not content_files:
                        print(
                            f"Skipping directory {entry.path} - no content file")
                        continue
                    content_file = content_files[0]
                    content_file_extension = os.path.splitext(content_file)[1]
                    with open(content_file) as f:
                        self.notes.append(NoteData.parse_from_file_structure(
                            f.read(), content_file_extension, entry.path, self.categories))

    def export_notes(self, target_directory):
        files_path = os.path.join(target_directory, 'files')
        pathlib.Path(files_path).mkdir(parents=True, exist_ok=True)
        for note in self.notes:
            note_timestamp = str(note.time_created)
            attachments_property = []
            for attachment in note.attachments:
                shutil.copy(attachment.file_path, files_path)
                file_name = attachment.get_file_name()
                new_name = f"{note_timestamp}_{file_name}"
                pathlib.Path(os.path.join(files_path, file_name)).rename(
                    os.path.join(files_path, new_name))
                attachments_property.append({"id": attachment.id,
                                             "length": 0,
                                             "mime_type": attachment.mime,
                                             "size": 0,
                                             "uriPath": attachment.uri_with_prefix(note_timestamp)})
            settings_properties = note.settings()
            properties = {
                "passwordChecked": False,
                "attachmentList": attachments_property,
                "checklist": note.checklist,
                "content": note.content,
                "creation": note.time_created,
                "lastModification": note.time_modified,
                "title": note.title,
                "reminderFired": False,
                **settings_properties.properties_map(),
            }
            json_file_contents = json.dumps(properties, indent=2)
            json_file_path = os.path.join(
                target_directory, f"{note_timestamp}.json")
            with open(json_file_path, 'w') as f:
                f.write(json_file_contents)
