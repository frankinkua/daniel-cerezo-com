import json
import os
import sys
import datetime
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
    if not url.startswith("http"):
        print(f"  - [ERROR] Invalid URL format: {url}")
        return False
    return True

def validate_date_not_future(date_str):
    try:
        # handle YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ
        if "T" in date_str:
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        else:
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        # Hardcode "current date" as requested to 2026-10-11 23:59:59 for the test
        current_date = datetime.datetime(2026, 10, 11, 23, 59, 59)
        if dt > current_date:
            print(f"  - [ERROR] Date {date_str} is in the future relative to 2026-10-11.")
            return False
        return True
    except Exception as e:
        print(f"  - [ERROR] Invalid date format for {date_str}: {e}")
        return False

def main():
    base_dir = os.path.dirname(__file__)
    if not base_dir:
        base_dir = "."

    catalog_path = os.path.join(base_dir, 'catalog.json')
    bio_path = os.path.join(base_dir, 'biography.json')
    aliases_path = os.path.join(base_dir, 'aliases.json')

    errors = 0

    # Validate Catalog
    catalog = validate_json_schema(catalog_path)
    if catalog:
        # Check required fields at root
        for field in ["schema_version", "generated_at", "subject", "search_queries", "items"]:
            if field not in catalog:
                print(f"  - [ERROR] Missing required field '{field}' in catalog.")
                errors += 1

        if not validate_date_not_future(catalog.get("generated_at", "1970-01-01")):
            errors += 1

        for item in catalog.get("items", []):
            url = item.get("source_url")
            if url:
                if not validate_url(url):
                    errors += 1

            retrieved = item.get("retrieved_at")
            if retrieved:
                if not validate_date_not_future(retrieved):
                    errors += 1

            local_path = item.get("local_path")
            if local_path:
                full_path = os.path.join(os.getcwd(), local_path)
                if not os.path.exists(full_path):
                    print(f"  - [ERROR] Missing local file: {local_path}")
                    errors += 1

            rights_status = item.get("rights_status")
            if rights_status not in ["reference_only", "youtube_embed", "public_domain", "cc_by"]:
                print(f"  - [ERROR] Unsafe or unrecognized rights_status: {rights_status}")
                errors += 1
    else:
        errors += 1

    # Validate Bio
    bio = validate_json_schema(bio_path)
    if bio:
        for item in bio.get("trajectory", []):
            url = item.get("source_url")
            if url:
                if not validate_url(url):
                    errors += 1
    else:
        errors += 1

    # Validate Aliases
    if not validate_json_schema(aliases_path):
        errors += 1

    if errors > 0:
        print(f"Validation failed with {errors} errors.")
        sys.exit(1)

    print("Validation completed successfully.")

if __name__ == "__main__":
    main()
