"Some simple utilities."
import importlib


def import_class(class_path):
    "Import a class using full path."
    parts = class_path.split('.')
    assert len(parts) > 1, "class path must include a module and a class, for example organize.csv.CSVParser"
    module_path = ".".join(parts[:-1])
    class_name = parts[-1]
    module_obj = importlib.import_module(module_path)
    return getattr(module_obj, class_name)
