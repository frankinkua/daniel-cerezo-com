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
    if not isinstance(url, str) or not url:
        print(f"  - [ERROR] URL must be a non-empty string, got: {url}")
        return False
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]) and result.scheme in ["http", "https"]:
            return True
        else:
            print(f"  - [ERROR] Invalid URL format or missing hostname: {url}")
            return False
    except ValueError:
        print(f"  - [ERROR] Malformed URL string: {url}")
        return False

def validate_date_not_future(date_str, as_of_date=None):
    if date_str == "unknown":
        return True
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
    parser.add_argument("--catalog", type=str, help="Specific catalog file to test", default=None)
    args = parser.parse_args()

    as_of_dt = None
    if args.as_of:
        as_of_dt = datetime.datetime.strptime(args.as_of, "%Y-%m-%d")
        as_of_dt = as_of_dt.replace(hour=23, minute=59, second=59)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    catalog_path = args.catalog if args.catalog else os.path.join(base_dir, 'catalog.json')
    bio_path = os.path.join(base_dir, 'biography.json')
    aliases_path = os.path.join(base_dir, 'aliases.json')

    errors = 0

    # Validate Catalog
    catalog = validate_json_schema(catalog_path)
    if catalog:
        for field in ["schema_version", "generated_at", "subject", "search_queries", "items"]:
            if field not in catalog:
                print(f"  - [ERROR] Missing required field '{field}' in catalog.")
                errors += 1

        if not validate_date_not_future(catalog.get("generated_at", "1970-01-01"), as_of_dt):
            errors += 1

        seen_ids = set()
        for item in catalog.get("items", []):
            item_id = item.get("id", "UNKNOWN")

            if item_id in seen_ids:
                print(f"  - [ERROR] Duplicate ID found: {item_id}")
                errors += 1
            seen_ids.add(item_id)

            # Type and existence checking
            required_string_fields = ["id", "type", "title", "person", "publisher", "date", "retrieved_at", "rights_status", "caption", "identity_evidence"]
            for f in required_string_fields:
                val = item.get(f)
                if not isinstance(val, str):
                    print(f"  - [ERROR] Missing or invalid type for field '{f}' in item {item_id}. Expected string.")
                    errors += 1

            required_array_fields = ["tags", "related_tags"]
            for f in required_array_fields:
                val = item.get(f)
                if not isinstance(val, list):
                    print(f"  - [ERROR] Missing or invalid type for field '{f}' in item {item_id}. Expected list.")
                    errors += 1

            source_url = item.get("source_url")
            if not validate_url(source_url):
                errors += 1

            asset_url = item.get("asset_url")
            if asset_url is not None and not validate_url(asset_url):
                errors += 1

            retrieved = item.get("retrieved_at")
            if isinstance(retrieved, str):
                if not validate_date_not_future(retrieved, as_of_dt):
                    errors += 1

            local_path = item.get("local_path")
            rights_status = item.get("rights_status")

            if not isinstance(local_path, str):
                local_path = ""

            if rights_status not in ["reference_only", "youtube_embed", "public_domain", "cc_by"]:
                print(f"  - [ERROR] Unsafe or unrecognized rights_status: {rights_status}")
                errors += 1

            if rights_status == "reference_only" and local_path != "":
                print(f"  - [ERROR] reference_only items must NOT have a local_path (found: {local_path} in {item_id}).")
                errors += 1

            if local_path != "":
                if ".." in local_path or local_path.startswith("/"):
                    print(f"  - [ERROR] Path traversal detected in local_path: {local_path}")
                    errors += 1
                else:
                    # Resolve relative to the catalog file being tested
                    catalog_dir = os.path.dirname(os.path.abspath(catalog_path))
                    # Fallback check assuming the path might be relative to the script's root in real environment
                    full_path = os.path.join(catalog_dir, "..", "..", "..", local_path)
                    if not os.path.exists(full_path):
                         full_path_script = os.path.join(catalog_dir, local_path)
                         if not os.path.exists(full_path_script):
                             print(f"  - [ERROR] Missing local file: {local_path}")
                             errors += 1

                rights_evidence = item.get("rights_evidence", "")
                if not rights_evidence or rights_status not in ["public_domain", "cc_by"]:
                     print(f"  - [ERROR] Local files must have explicit permissive rights_status and rights_evidence (item {item_id}).")
                     errors += 1

    else:
        errors += 1

    # Validate Bio (only if we didn't specify a custom catalog test)
    if not args.catalog:
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
