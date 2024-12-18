import json
import re

def handle_file_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            print(f"[ERROR] File not found: {e}")
        except IOError as e:
            print(f"[ERROR] I/O error: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
    return wrapper


class ConfigParser:
    def __init__(self):
        self.config = {}

    def parse(self, file_path):
        try:
            with open(file_path, 'r') as f:
                current_section = None
                for line in f:
                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue  
                    section_match = re.match(r'\[(.+)\]', line)
                    if section_match:
                        current_section = section_match.group(1)
                        if current_section in self.config:
                            raise ValueError(f"Duplicate section: {current_section}")
                        self.config[current_section] = {}
                    elif "=" in line:
                        if current_section is None:
                            raise ValueError("Key-value pair outside of section")
                        key, value = map(str.strip, line.split("=", 1))
                        if key in self.config[current_section]:
                            raise ValueError(f"Duplicate key: {key} in section [{current_section}]")
                        self.config[current_section][key] = value
                    else:
                        raise ValueError(f"Invalid line format: {line}")

        except Exception as e:
            print(f"[ERROR] Failed to parse file: {e}")

    def validate(self):
        for section, params in self.config.items():
            if section == "Database":
                if "port" in params:
                    if not params["port"].isdigit():
                        raise ValueError(f"Invalid port in section [{section}]")
            if section == "API":
                if "timeout" in params:
                    if not params["timeout"].isdigit():
                        raise ValueError(f"Invalid timeout in section [{section}]")

    def save_to_json(self, file_path):
        try:
            with open(file_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            print(f"Configuration saved to {file_path}")
        except FileNotFoundError as e:
            print(f"[ERROR] File not found: {e}")
        except IOError as e:
            print(f"[ERROR] I/O error: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")

    def load_from_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                self.config = json.load(f)
            print(f"Configuration loaded from {file_path}")
        except FileNotFoundError as e:
            print(f"[ERROR] File not found: {e}")
        except IOError as e:
            print(f"[ERROR] I/O error: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")



if __name__ == "__main__":
    parser = ConfigParser()
    parser.parse("config.cfg")
    try:
        parser.validate()
    except ValueError as e:
        print(f"[ERROR] Validation failed: {e}")
    parser.save_to_json("config.json")
    parser.load_from_json("config.json")

    print("Parsed configuration:")
    print(parser.config)
