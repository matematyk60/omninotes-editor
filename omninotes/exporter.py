import glob
import json
import os
import pathlib
import shutil
from time import time, sleep


from omninotes.notedata import NoteData


class Exporter:
    def __init__(self, source_path: str):
        self.source_path = source_path
        self.notes = []
        self.load_notes()

    def load_notes(self):
        with os.scandir(self.source_path) as entries:
            for entry in entries:
                if entry.is_dir:
                    content_file = glob.glob(f"{entry.path}/*.txt")[0]
                    with open(content_file) as f:
                        self.notes.append(NoteData.parse_from_file_structure(f.read(), entry.path))
                else:
                    pass

    def export_notes(self, target_directory):
        files_path = os.path.join(target_directory, 'files')
        pathlib.Path(files_path).mkdir(parents=True, exist_ok=True)
        for note in self.notes:
            sleep(0.01)
            note_timestamp = str(int(time() * 1000))
            attachments_property = []
            for attachment in note.attachments:
                shutil.copy(attachment.file_path, files_path)
                file_name = attachment.get_file_name()
                new_name = f"{note_timestamp}_{file_name}"
                pathlib.Path(os.path.join(files_path, file_name)).rename(os.path.join(files_path, new_name))
                attachments_property.append({"id": attachment.id,
                                             "length": 0,
                                             "mime_type": attachment.mime,
                                             "size": 0,
                                             "uriPath": attachment.uriWithPrefix(note_timestamp)})
            properties = {
                "passwordChecked": False,
                "archived": note.archived,
                "attachmentList": attachments_property,
                "checkList": False,
                "content": note.content,
                "creation": note.time_created,
                "lastModification": note.time_modified,
                "trashed": note.trashed,
                "title": note.title,
                "reminderFired": False
            }
            json_file_contents = json.dumps(properties)
            json_file_path = os.path.join(target_directory, f"{note_timestamp}.json")
            with open(json_file_path, 'w') as f:
                f.write(json_file_contents)
