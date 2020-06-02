from typing import Optional
import os
import configparser
from omninotes.category import Category
from datetime import datetime
from time import time

class Settings:
    def __init__(self, trashed: bool, archived: bool, alarm: Optional[int], category: Optional[Category], time_created: int, longitude: float, latitude:float):
        self.trashed = trashed
        self.archived = archived
        self.alarm = alarm  # epoch millis
        self.category = category
        self.time_created = time_created
        self.longitude = longitude
        self.latitude = latitude

    @staticmethod
    def settings_section(): return "settings"

    @staticmethod
    def settings_file(base_dir): return os.path.join(base_dir, 'settings.ini')

    def write_to_file(self, base_dir):
        config = configparser.ConfigParser()
        config[Settings.settings_section()] = {
            "id": str(self.time_created),
            "trashed": str(self.trashed).lower(),
            "archived": str(self.archived).lower(),
            "alarm": datetime.fromtimestamp(self.alarm / 1000).isoformat() if self.alarm else "",
            "category": self.category.title if self.category else "",
            "longitude": self.longitude if self.longitude else "",
            "latitude": self.latitude if self.latitude else ""
        }

        with open(Settings.settings_file(base_dir), 'w') as f:
            config.write(f)

    def properties_map(self):
        alarm = {"alarm": int(self.alarm)} if self.alarm else {}
        category = {"baseCategory": self.category.to_json()} if self.category else {}
        location = {"latitude" : self.latitude, "longitude" : self.longitude} if self.longitude and self.latitude else {}
        return {
            "trashed": self.trashed,
            "archived": self.archived,
            **alarm,
            **category,
            **location
        }

    @staticmethod
    def parse_from_json(json):
        alarm = json.get("alarm")
        if alarm: alarm = int(alarm)
        creation = json.get("creation")
        if not creation: raise Exception("Note json does not contain 'creation'")
        return Settings(
            json.get("trashed", False),
            json.get("archived", False),
            alarm,
            Category.parse_from_backup(json["baseCategory"]) if "baseCategory" in json else None,
            creation,
            json.get("longitude"),
            json.get("latitude")
        )

    @staticmethod
    def parse_from_file(base_dir, categories):
        config = configparser.ConfigParser()
        config.read(Settings.settings_file(base_dir))

        category = config.get(Settings.settings_section(), "category", fallback=None)
        if category:
            cat_title = category
            category = categories.get(cat_title)
            if not category:
                categories[cat_title] = Settings.create_new_category(cat_title)
                category = categories[cat_title]
                Settings.write_new_category(category, os.path.join(base_dir, '..', 'categories.ini'))
        
        longitude = config.get(Settings.settings_section(), "longitude", fallback=None)
        if longitude:
            longitude = float(longitude)
        latitude=config.get(Settings.settings_section(), "latitude", fallback=None)
        if latitude:
            latitude = float(latitude)

        time_created = config.getint(Settings.settings_section(), "id", fallback=None)
        if time_created is None:
            raise Exception(f"Id is missing for note '{base_dir}'")
        alarm = config.get(Settings.settings_section(), "alarm", fallback=None)
        parsed_alarm = int(datetime.fromisoformat(alarm).timestamp()) * 1000 if alarm else None
        return Settings(trashed=config.getboolean(Settings.settings_section(), "trashed"),
                        archived=config.getboolean(Settings.settings_section(), "archived"),
                        alarm=parsed_alarm, category=category, time_created=time_created,
                        longitude=longitude,
                        latitude=latitude)


    @staticmethod
    def create_new_category(cat_title) -> Category:
        from omninotes.cli import CLI
        if not CLI.Instance.options.no_confirm:
            print(f"Category '{cat_title}' does not exists'")
            if input("Type 'y' to create, 'n' to abort exporting: ").strip().lower() != 'y':
                exit(0)
            color = input("Input color: ")
            if not Category.validate_color(color):
                raise Exception("Provider color is incorrect")
            return Category(int(time() * 1000), cat_title, color)
        return Category(int(time() * 1000), cat_title, "black")
        
    @staticmethod
    def write_new_category(category, path):
        if os.path.exists(path):
            Category.dump_to_file(path, [category], True)

