import glob
import os
import shutil
import pathlib
from os.path import join
from omninotes.notedata import NoteData


class Importer:
    def __init__(self, backup_path: str):
        self.backup_path = backup_path
        self.notes = []
        self.load_notes()

    def load_notes(self):
        backups = glob.glob(f"{self.backup_path}/*.json")
        for backup in backups:
            with open(backup) as f:
                self.notes.append(
                    NoteData.parse_from_backup(f.read(), f"{join(self.backup_path, 'files')}"))

    def importNotes(self, path: str):
        for note in self.notes:
            title = self.get_title(note)
            note_path = join(path, title)
            files_path = join(note_path, 'attachments')
            pathlib.Path(note_path).mkdir(parents=True, exist_ok=True)
            pathlib.Path(files_path).mkdir(parents=True, exist_ok=True)
            content_path = f"{join(note_path, note.title if note.title else 'content')}.txt"
            with open(content_path, 'w') as f:
                f.write(note.content)
            for attachment in note.attachments:
                shutil.copy2(attachment.file_path, files_path)

    def get_title(self, note: NoteData) -> str:
        if note.title:
            return f'{note.title}_{note.time_created}'
        return str(note.time_created)
