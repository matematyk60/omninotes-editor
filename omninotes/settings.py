from typing import Optional
import os
import configparser

from datetime import datetime


class Settings:
    def __init__(self, trashed: bool, archived: bool, alarm: Optional[int]):
        self.trashed = trashed
        self.archived = archived
        self.alarm = alarm  # epoch millis

    @staticmethod
    def settings_section(): return "settings"

    @staticmethod
    def settings_file(base_dir): return os.path.join(base_dir, 'settings.ini')

    def write_to_file(self, base_dir):
        config = configparser.ConfigParser()

        config[Settings.settings_section()] = {
            "trashed": str(self.trashed).lower(),
            "archived": str(self.archived).lower(),
            "alarm": datetime.fromtimestamp(self.alarm / 1000).isoformat() if self.alarm else ""
        }

        with open(Settings.settings_file(base_dir), 'w') as f:
            config.write(f)

    def properties_map(self):
        alarm = {"alarm": self.alarm} if self.alarm else {}
        return {
            "trashed": self.trashed,
            "archived": self.archived,
            **alarm
        }

    @staticmethod
    def parse_from_json(json):
        Settings.validate_json(json)
        return Settings(
            json.get("trashed", False),
            json.get("archived", False),
            json.get("alarm")
        )

    @staticmethod
    def parse_from_file(base_dir):
        Settings.validate_file_structure(base_dir)
        config = configparser.ConfigParser()
        config.read(Settings.settings_file(base_dir))
        alarm = config.get(Settings.settings_section(), "alarm", fallback=None)
        parsed_alarm = int(datetime.fromisoformat(alarm).timestamp()) * 1000 if alarm else None
        return Settings(trashed=config.getboolean(Settings.settings_section(), "trashed"),
                        archived=config.getboolean(Settings.settings_section(), "archived"),
                        alarm=parsed_alarm)

    @staticmethod
    def validate_json(json):
        # TODO: validation
        pass

    @staticmethod
    def validate_file_structure(filePath):
        # TODO: validation
        pass
