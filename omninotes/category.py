
import os
import configparser


class Category:
    # ARGB
    color_names = {
        "black": 0xFF000000,
        "white": 0xFFFFFFFF,
        "red": 0xFFFF0000,
        "green": 0xFF00FF00,
        "blue": 0xFF0000FF
    }

    def __init__(self, id: int, title: str, color: str):
        self.id = id
        self.title = title
        self.color = color

    def get_color_json_value(self):
        name = self.color.lower()
        if name in Category.color_names.keys():
            value = Category.color_names[name]
        else:
            value = int(name[1:], 16)
        return value - 2**32

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.title,
            "color": self.get_color_json_value(),
            "description" : "",
            "count": 0
        }

    @staticmethod
    def json_value_to_hex_string_or_name(value: int):
        hex_val = 0xFFFFFFFF & value
        if hex_val in Category.color_names.values():
            return [name for name in Category.color_names.keys()
                    if Category.color_names[name] == hex_val][0]
        return "#%08X" % (hex_val)

    @staticmethod
    def parse_from_config_file(filename) -> list:
        if not os.path.exists(filename):
            print(
                f"Warning: category definition file {filename} does not exist")
            return []
        config = configparser.ConfigParser()
        config.read(filename)
        categories = []
        for section in config.sections():
            color = config.get(section, "color", fallback=None)
            id = config.get(section, "id", fallback=None)
            if not id:
                print(f"Warning: ID not specified for category: {section}")
                continue
            if not color:
                print(f"Warning: color not specified for category: {section}")
                continue
            if not Category.validate_color(color):
                print(
                    f"Warning: color for category {section} is in incorrect format")
                continue
            categories.append(Category(id, section, color))
        return categories

    @staticmethod
    def parse_from_backup(json_dict):
        Category.validate_backup_json(json_dict)
        return Category(
            json_dict["id"],
            json_dict["name"],
            Category.json_value_to_hex_string_or_name(int(json_dict["color"])))

    @staticmethod
    def validate_backup_json(json_dict):
        if "id" not in json_dict or "name" not in json_dict or "color" not in json_dict:
            raise Exception("Backup has invalid category data")

    @staticmethod
    def validate_color(color):
        if color.lower() in Category.color_names.keys():
            return True
        if not color.startswith("#"):
            return False
        try:
            hex_val = int(color[1:], 16)
            return hex_val >= 0 and hex_val <= 0xFFFFFFFF
        except:
            return False

    @staticmethod
    def dump_to_file(filename, categories: list, append=False):
        config = configparser.ConfigParser()
        for category in categories:
            config[category.title] = {
                "id": category.id,
                "color": category.color
            }
        if not append:
            with open(filename, "w") as f:
                f.write(Category.get_categories_header())
                config.write(f)
        else:
            with open(filename, "a") as f:
                f.write('\n')
                config.write(f)

    @staticmethod
    def get_categories_header() -> str:
        return f"; Available colors: {', '.join(Category.color_names.keys())}\n; or hex values: #AARRGGBB\n"