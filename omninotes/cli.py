import argparse
import sys
from omninotes.importer import Importer
import os
import pathlib
from omninotes.exporter import Exporter
from omninotes.category import Category
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
        self.parser.add_argument(
            "-s", "--source", dest="source", action="store")
        self.parser.add_argument("backup_paths", nargs='*', action="store")
        self.parser.add_argument("-n", "--no-confirm",
                                 dest="no_confirm", action='store_true', help='No user input for incomplete data')
        self.parser.add_argument(
            "--add-category", action='store', dest="category_title")
        self.parser.add_argument(
            "--color", action='store', dest="color", help='color for new category')

    def run(self):
        CLI.Instance = self
        self.options = self.parser.parse_args()

        if self.options.category_title:
            try:
                self.add_category(self.options.category_title)
            except Exception as e:
                print(f"Error while creating category: {e}")
        elif bool(self.options.import_) == bool(self.options.export):
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
            source = self.get_source_path()
            dest = self.options.destination if self.options.destination else "./OmniNotesEditor/backup/"
            try:
                exporter = Exporter(source)
                exporter.export_notes(dest)
            except Exception as e:
                print(
                    f"Error while exporting to backup from source '{source}': {e}")
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

    def home_dir(self):
        os.path.expanduser("~")
