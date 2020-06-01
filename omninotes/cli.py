import argparse
import sys
from omninotes.importer import Importer
import os
import pathlib
from omninotes.exporter import Exporter
from omninotes.category import Category
from omninotes.settings import Settings
from omninotes.category_dump import CategoryDump
from omninotes.cli_helpers import CliHelpers


class CLI:
    Instance = None

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="OmniNotes editor")
        self.parser.add_argument(
            "-i", "--import", dest="import_", action='store_true')
        self.parser.add_argument(
            "-e", "--export", dest="export", action='store_true')
        self.parser.add_argument(
            "-d", "--destination", dest="destination", action="store")
        self.parser.add_argument("backup_paths", nargs='*', action="store")
        self.parser.add_argument("-n", "--no-confirm",
                                 dest="no_confirm", action='store_true', help='No user input for incomplete data')
        self.parser.add_argument(
            "--add-category", action='store', dest="category_title")
        self.parser.add_argument(
            "--color", action='store', dest="color", help='color for new category')
        self.parser.add_argument(
            "-s", "--source", dest="source", action="store")
        self.parser.add_argument(
            "--add-note", dest="add_note", action='store_true')
        self.parser.add_argument("--title", dest="note_title", action='store')
        self.parser.add_argument("--settings", action='store', dest='settings')
        self.parser.add_argument("--trashed", dest='trashed', action='store')
        self.parser.add_argument("--archived", dest='archived', action='store')
        self.parser.add_argument("--category", dest='category', action='store')

    def run(self):
        CLI.Instance = self
        self.options = self.parser.parse_args()

        if self.options.category_title:
            try:
                self.add_category(self.options.category_title)
            except Exception as e:
                print(f"Error while creating category: {e}")
        elif self.options.add_note:
            try:
                self.add_note()
            except Exception as e:
                print(f"Error while creating note: {e}")
        elif bool(self.options.import_) == bool(self.options.export) and self.options.import_ and self.options.export:
            self.parser.print_usage()
        elif self.options.import_:
            dest = self.options.destination if self.options.destination else "./OmniNotesEditor/"
            category_dump = CategoryDump()
            pathlib.Path(dest).mkdir(parents=True, exist_ok=True)
            for backup_path in self.options.backup_paths:
                try:
                    Importer(backup_path, category_dump).import_notes(dest)
                except Exception as e:
                    print(f"Error while importing backup '{backup_path}': {e}")
            category_dump.write_category_file(dest)
        elif self.options.export:
            if self.options.backup_paths:
                source = self.options.backup_paths[0]
            else:
                self.parser.print_usage()
                return
            dest = self.options.destination if self.options.destination else "./OmniNotesEditor/backup/"
            try:
                exporter = Exporter(source)
                exporter.export_notes(dest)
            except Exception as e:
                print(
                    f"Error while exporting to backup from source '{source}': {e}")
        elif self.options.settings:
            note_directory = self.options.settings
            try:
                trashed = bool(self.options.trashed) if self.options.trashed else None
                archived = bool(self.options.archived) if self.options.archived else None
                category = self.options.category

                CliHelpers.edit_settings(note_directory, trashed, archived, category)
            except Exception as e:
                print(f"Error while changing settings in note '{note_directory}': {e}")

        else:
            raise NotImplementedError()

    def get_source_path(self) -> str:
        return self.options.source if self.options.source else "."

    def add_category(self, title):
        color = self.options.color
        if not color:
            if self.options.no_confirm:
                color = list(Category.color_names.keys())[0]
            else:
                color = input("Type color name or #AARRGGBB hex value: ")

        CliHelpers.create_new_category(self.get_source_path(), title, color)

    def add_note(self):
        title = self.options.note_title
        if not title:
            if not self.options.no_confirm:
                title = input("Type note title: ")
        CliHelpers.create_new_note(self.get_source_path(), title)


    def home_dir(self):
        os.path.expanduser("~")
