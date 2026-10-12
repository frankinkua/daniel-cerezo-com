import json
import sys
from datetime import datetime, timezone

def is_valid_access_time(time_str):
    if time_str is None:
        return True
    try:
        if time_str.endswith('Z'):
            time_str = time_str[:-1] + '+00:00'
        dt = datetime.fromisoformat(time_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        if dt > now:
            return False
        return True
    except ValueError:
        return False

def run_isolated_tests():
    assert is_valid_access_time('2026-10-11T12:00:00Z') == True
    assert is_valid_access_time('2027-10-12T13:00:00Z') == False
    assert is_valid_access_time(None) == True
    assert is_valid_access_time('2026-10-11') == True
    print("Isolated helper tests passed.")

def run_tests():
    with open('inbox/media/media-research-2026-10-12/r10/findings.json', 'r') as f:
        findings = json.load(f)

    with open('inbox/media/media-research-2026-10-12/r10/search-log.json', 'r') as f:
        search_log = json.load(f)

    with open('inbox/media/media-research-2026-10-12/r10/asset-delivery.json', 'r') as f:
        delivery_log = json.load(f)

    ids = set()
    errors = []

    # 1. Unique IDs
    for item in findings['items']:
        if item['id'] in ids:
            errors.append(f"Duplicate ID: {item['id']}")
        ids.add(item['id'])

        # 2. Schema check (basic)
        if item['type'] == 'image':
            if 'source_url' not in item or 'asset_url' not in item or 'canonical_url' not in item:
                errors.append(f"Missing source_url, asset_url or canonical_url in {item['id']}")
            if item['published_at'] is not None:
                errors.append(f"Image {item['id']} has published_at not set to None")

            if item.get('delivery_status') not in ['downloaded', 'permission_pending', 'access_failed', 'reference_only']:
                 errors.append(f"Invalid delivery_status in {item['id']}")

            if item.get('delivery_status') in ['permission_pending', 'access_failed', 'reference_only']:
                 if not item.get('next_action'):
                     errors.append(f"Missing next_action/blocker for undelivered image {item['id']}")

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

    # 4. Delivery Log counts
    image_items = [i for i in findings['items'] if i['type'] == 'image']
    if len(image_items) != delivery_log.get('discovered_image_count'):
        errors.append("Mismatch in discovered image count")
    pending = [i for i in image_items if i.get('delivery_status') == 'permission_pending']
    if len(pending) != delivery_log.get('permission_pending_count'):
        errors.append("Mismatch in pending permission image count")

    if errors:
        for err in errors:
            print("ERROR:", err)
        sys.exit(1)

    print("All validation passed successfully.")
    sys.exit(0)

if __name__ == '__main__':
    run_isolated_tests()
    run_tests()
