import glob
import os
import shutil
import pathlib
from os.path import join
from omninotes.notedata import NoteData
from omninotes.category import Category
from omninotes.category_dump import CategoryDump


class Importer:
    def __init__(self, backup_path: str, category_dump: CategoryDump):
        self.backup_path = backup_path
        self.notes = []
        self.category_dump = category_dump
        self.load_notes()

    def load_notes(self):
        backups = glob.glob(f"{self.backup_path}/*.json")
        for backup in backups:
            with open(backup) as f:
                self.notes.append(
                    NoteData.parse_from_backup(f.read(), f"{join(self.backup_path, 'files')}"))

    def import_notes(self, path: str):
        for note in self.notes:
            title = self.get_title(note)
            note_path = join(path, title)
            files_path = join(note_path, 'attachments')
            pathlib.Path(note_path).mkdir(parents=True, exist_ok=True)
            pathlib.Path(files_path).mkdir(parents=True, exist_ok=True)
            extension = ".cl" if note.checklist else ".txt"
            content_path = f"{join(note_path, note.title if note.title else 'content')}{extension}"
            with open(content_path, 'w') as f:
                f.write(note.content)
            for attachment in note.attachments:
                shutil.copy2(attachment.file_path, files_path)
            note.settings().write_to_file(note_path)
        self.add_categories()

    def get_title(self, note: NoteData) -> str:
        if note.title:
            return f'{note.title}_{note.time_created}'
        return str(note.time_created)

    def add_categories(self):
        for note in self.notes:
            if note.category:
                self.category_dump.add(note.category)
