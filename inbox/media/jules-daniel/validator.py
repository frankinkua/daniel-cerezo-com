import json
import os
import sys
import datetime
from urllib.parse import urlparse
import argparse

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
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]) and result.scheme in ["http", "https"]:
            return True
        else:
            print(f"  - [ERROR] Invalid URL format: {url}")
            return False
    except ValueError:
        print(f"  - [ERROR] Malformed URL string: {url}")
        return False

def validate_date_not_future(date_str, as_of_date=None):
    try:
        if "T" in date_str:
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        elif len(date_str) == 7: # YYYY-MM
             dt = datetime.datetime.strptime(date_str, "%Y-%m")
        else:
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        current_date = as_of_date if as_of_date else datetime.datetime.utcnow()
        if dt > current_date:
            print(f"  - [ERROR] Date {date_str} is in the future relative to {current_date.strftime('%Y-%m-%d')}.")
            return False
        return True
    except Exception as e:
        print(f"  - [ERROR] Invalid date format for {date_str}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", type=str, help="Date to use as 'current' (YYYY-MM-DD)", default=None)
    args = parser.parse_args()

    as_of_dt = None
    if args.as_of:
        as_of_dt = datetime.datetime.strptime(args.as_of, "%Y-%m-%d")
        # Ensure it covers end of the given day if comparing
        as_of_dt = as_of_dt.replace(hour=23, minute=59, second=59)

    base_dir = os.path.dirname(os.path.abspath(__file__))
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

        if not validate_date_not_future(catalog.get("generated_at", "1970-01-01"), as_of_dt):
            errors += 1

        for item in catalog.get("items", []):
            item_id = item.get("id", "UNKNOWN")

            # Required fields for item
            required_item_fields = ["id", "type", "title", "source_url", "asset_url", "local_path",
                                    "person", "tags", "related_tags", "publisher", "date",
                                    "retrieved_at", "rights_status", "rights_evidence",
                                    "caption", "identity_evidence"]

            for f in required_item_fields:
                if f not in item:
                    print(f"  - [ERROR] Missing required field '{f}' in item {item_id}.")
                    errors += 1

            url = item.get("source_url")
            if url:
                if not validate_url(url):
                    errors += 1

            retrieved = item.get("retrieved_at")
            if retrieved:
                if not validate_date_not_future(retrieved, as_of_dt):
                    errors += 1

            local_path = item.get("local_path")
            rights_status = item.get("rights_status")

            if rights_status not in ["reference_only", "youtube_embed", "public_domain", "cc_by", "official_press_or_reference"]:
                print(f"  - [ERROR] Unsafe or unrecognized rights_status: {rights_status}")
                errors += 1

            if rights_status == "reference_only" and local_path != "":
                print(f"  - [ERROR] reference_only items must NOT have a local_path (found: {local_path} in {item_id}).")
                errors += 1

            if local_path != "":
                # Path traversal guard
                if ".." in local_path or local_path.startswith("/"):
                    print(f"  - [ERROR] Path traversal detected in local_path: {local_path}")
                    errors += 1
                else:
                    full_path = os.path.join(base_dir, "..", "..", "..", local_path)
                    if not os.path.exists(full_path):
                         # check if relative to script dir works
                         full_path_script = os.path.join(base_dir, local_path)
                         if not os.path.exists(full_path_script):
                             print(f"  - [ERROR] Missing local file: {local_path}")
                             errors += 1

                # Must have explicit evidence if a file is hosted locally
                rights_evidence = item.get("rights_evidence", "")
                if not rights_evidence or rights_status not in ["public_domain", "cc_by", "official_press_or_reference"]:
                     print(f"  - [ERROR] Local files must have explicit permissive rights_status and rights_evidence (item {item_id}).")
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
