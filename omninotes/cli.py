import argparse
import sys
from omninotes.importer import Importer


class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="OmniNotes editor")
        self.parser.add_argument(
            "-i", "--import", dest="import_", action='store_true')
        self.parser.add_argument(
            "-e", "--export", dest="export", action='store_true')
        self.parser.add_argument(
            "-d", "--destination", dest="destination", action="store")
        self.parser.add_argument("backup_paths", nargs='+', action="store")

    def run(self):
        options = self.parser.parse_args()
        if bool(options.import_) == bool(options.export):
            self.parser.print_usage()
        elif options.import_:
            dest = options.destination if options.destination else "./OmniNotesEditor/"
            for backup_path in options.backup_paths:
                try:
                    Importer(backup_path).importNotes(dest)
                except Exception as e:
                    print(f"Error while importing backup '{backup_path}': {e}")
        else:
            raise NotImplementedError()
