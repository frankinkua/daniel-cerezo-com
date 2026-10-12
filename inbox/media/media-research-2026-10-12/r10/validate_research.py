import json
import sys

def run_tests():
    with open('inbox/media/media-research-2026-10-12/r10/findings.json', 'r') as f:
        findings = json.load(f)

    with open('inbox/media/media-research-2026-10-12/r10/search-log.json', 'r') as f:
        search_log = json.load(f)

    ids = set()
    errors = []

    # 1. Unique IDs
    for item in findings['items']:
        if item['id'] in ids:
            errors.append(f"Duplicate ID: {item['id']}")
        ids.add(item['id'])

        # 2. Schema check (basic)
        if item['type'] == 'image':
            if 'source_url' not in item or 'asset_url' not in item:
                errors.append(f"Missing source_url or asset_url in {item['id']}")
            if item['published_at'] is not None:
                errors.append(f"Image {item['id']} has published_at not set to None (invented precision from URL path)")

        if item['rights_status'] == 'reference_only':
            if item.get('local_path') is not None:
                errors.append(f"Item {item['id']} is reference_only but has a local_path")

        # Confidence format
        if not item['confidence'] in ['high', 'medium', 'low']:
            errors.append(f"Item {item['id']} has invalid confidence enum: {item['confidence']}")
        if not item.get('confidence_reason'):
            errors.append(f"Item {item['id']} is missing confidence_reason")

    # 3. Search log precision
    for log in search_log['log']:
        if log['access_time'] is not None and "12:00:00" in log['access_time']:
            errors.append(f"Invented precision found in search-log: {log['access_time']}")

    if errors:
        for err in errors:
            print("ERROR:", err)
        sys.exit(1)

    print("All validation passed successfully.")
    sys.exit(0)

if __name__ == '__main__':
    run_tests()
