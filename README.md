# omninotes readme

# usage

## import your notes

To import your notes from OmniNotes app you have to do backup in app. Go to Settins → Data → Sync and Backups → Backup and type name for the backup. Then you can import backup folder to your computer. Your backup directory structure should have following structure:

```bash
.
├── 1591002625529.json
├── 1591002640043.json
└── files
    └── 20200601_111656_466.jpg
```

To import your backup run.

```bash
./omninoteseditor --import /home/user/my-backup --destination /home/user/my-notes
```

Created note structure should has following structure:

```bash
.
├── My checklist_1591002625529 # checklist note with title 'My checklist'
│   ├── My checklist.cl # checklist note file
│   ├── attachments # directory with note attachments
│   └── settings.ini # settings file
├── My note_1591002640043 # text note with title 'My note'
│   ├── My note.txt # note file with note contents
│   ├── attachments #directory with note attachments
│   │   └── 20200601_111656_466.jpg # image attachment to note 'My note'
│   └── settings.ini # settings file
└── categories.ini # category database file
```

## edit your notes

To edit text note, simply edit contents of note's `.txt` file. Same instructions apply to editing a checklist note (`.cl`), but you have to remember that is must have checklist structure, e.g.:

```
[ ] Cut tree
[ ] Smell fresh grass
[x] do the laundry
```

## add an attachment

To add new attachment simply add file to `attachments` directory.

## export your notes

## dependencies

# development documentation