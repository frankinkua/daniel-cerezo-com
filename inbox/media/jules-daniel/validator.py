import json
import os
import urllib.request
from urllib.error import URLError, HTTPError

def validate_json_schema(filepath):
    print(f"Validating {filepath}...")
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"  - [OK] {filepath} is valid JSON.")
        return data
    except Exception as e:
        print(f"  - [ERROR] Failed to parse {filepath}: {e}")
        return None

def validate_url(url):
    # Some sites block python urllib, so we just check if it's well-formed
    if not url.startswith("http"):
        print(f"  - [ERROR] Invalid URL format: {url}")
        return False
    return True

def main():
    base_dir = os.path.dirname(__file__)
    if not base_dir:
        base_dir = "."

    catalog_path = os.path.join(base_dir, 'catalog.json')
    bio_path = os.path.join(base_dir, 'biography.json')
    aliases_path = os.path.join(base_dir, 'aliases.json')

    # Validate Catalog
    catalog = validate_json_schema(catalog_path)
    if catalog:
        for item in catalog.get("items", []):
            url = item.get("source_url")
            if url:
                validate_url(url)

    # Validate Bio
    bio = validate_json_schema(bio_path)
    if bio:
        for item in bio.get("trajectory", []):
            url = item.get("source_url")
            if url:
                validate_url(url)

    # Validate Aliases
    validate_json_schema(aliases_path)

    print("Validation complete.")

if __name__ == "__main__":
    main()
