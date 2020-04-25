from omninotes.category import Category
import os


class CategoryDump:
    def __init__(self):
        self.categories = []

    def add(self, category):
        self.categories.append(category)
    

    def write_category_file(self, base_dir: str):
        filename = os.path.join(base_dir, "categories.ini")
        categories = []
        for category in self.categories:
            dup_id_cat = list(filter(lambda c: c.id == category.id, categories)) 
            if dup_id_cat:
                if dup_id_cat[0].title != category.title or dup_id_cat[0].color != category.color:
                    print(f"Warning: categories {dup_id_cat[0].title}/{dup_id_cat[0].color} and {category.title}/{category.color}"
                            " have the same ID. Latter was not imported")
                continue
            categories.append(category)
                
        Category.dump_to_file(filename, categories)