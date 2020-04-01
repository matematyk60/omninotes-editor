import argparse
from omninotes.importer import Importer

class CLI:
    def __init__(self):

        self.parser = argparse.ArgumentParser(description="OmniNotes editor")
        self.parser.add_argument("-i", "--import", dest="import_", action='store_true')
        self.parser.add_argument("-e", "--export", dest="export", action='store_true')
        self.parser.add_argument("-p", "--path", dest="path")
        self.parser.add_argument("-d", "--destination", dest="dest")


    def run(self):
        options = self.parser.parse_args()
        if not options.path or (options.import_ and options.export):
            self.parser.print_usage()
        elif options.import_:
            dest = options.dest if options.dest else "./OmniNotesEditor/"
            Importer(options.path).importNotes(dest)
        elif options.export:
            raise NotImplementedError()
        else:
            self.parser.print_usage()


    