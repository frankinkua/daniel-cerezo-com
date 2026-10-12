import json
import sys
from datetime import datetime, timezone

def is_valid_access_time(time_str):
    if time_str is None:
        return True
    try:
        # Handle 'Z' suffix for UTC
        if time_str.endswith('Z'):
            time_str = time_str[:-1] + '+00:00'
        dt = datetime.fromisoformat(time_str)
        # If it's a naive datetime (date-only), assume UTC for comparison
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        if dt > now:
            return False # Future timestamp
        return True
    except ValueError:
        return False # Invalid format

def run_isolated_tests():
    # Test valid past noon timestamp
    assert is_valid_access_time('2026-10-11T12:00:00Z') == True

    # Test future non-noon timestamp
    assert is_valid_access_time('2027-10-12T13:00:00Z') == False

    # Test null
    assert is_valid_access_time(None) == True

    # Test date-only
    assert is_valid_access_time('2026-10-11') == True

    print("Isolated helper tests passed.")

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
        if not is_valid_access_time(log.get('access_time')):
            errors.append(f"Invalid or future timestamp found in search-log: {log.get('access_time')}")

    if errors:
        for err in errors:
            print("ERROR:", err)
        sys.exit(1)

    print("All validation passed successfully.")
    sys.exit(0)

if __name__ == '__main__':
    run_isolated_tests()
    run_tests()
