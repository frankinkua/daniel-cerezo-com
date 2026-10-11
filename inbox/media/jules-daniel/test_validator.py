import os
import subprocess
import json
import tempfile

def run_validator(catalog_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    validator_path = os.path.join(base_dir, 'validator.py')
    result = subprocess.run(['python3', validator_path, '--as-of', '2026-10-11', '--catalog', catalog_path], capture_output=True, text=True)
    return result

def create_temp_json(temp_dir, filename, data):
    path = os.path.join(temp_dir, filename)
    with open(path, 'w') as f:
        json.dump(data, f)
    return path

def get_base_catalog():
    return {
      "schema_version": 1,
      "generated_at": "2026-10-11",
      "subject": "Daniel Cerezo",
      "search_queries": [],
      "items": []
    }

def get_base_item():
    return {
      "id": "test-id",
      "type": "image",
      "title": "Valid title",
      "source_url": "https://example.com/source",
      "asset_url": "https://example.com/asset.jpg",
      "local_path": "",
      "person": "Daniel",
      "tags": [],
      "related_tags": [],
      "publisher": "Pub",
      "date": "2020-01-01",
      "retrieved_at": "2020-01-01",
      "rights_status": "reference_only",
      "rights_evidence": "none",
      "caption": "test",
      "identity_evidence": "test"
    }

def test_duplicate_ids():
    with tempfile.TemporaryDirectory() as temp_dir:
        cat = get_base_catalog()
        item1 = get_base_item()
        item2 = get_base_item() # Same ID
        cat["items"] = [item1, item2]
        cat_path = create_temp_json(temp_dir, 'cat.json', cat)

        res = run_validator(cat_path)
        assert res.returncode == 1, "Failed to reject duplicate IDs"
        assert "Duplicate ID found" in res.stdout

def test_invalid_types():
    with tempfile.TemporaryDirectory() as temp_dir:
        cat = get_base_catalog()
        item = get_base_item()
        item["tags"] = "not-an-array" # Should be list
        item["title"] = 12 # Should be string
        cat["items"] = [item]
        cat_path = create_temp_json(temp_dir, 'cat.json', cat)

        res = run_validator(cat_path)
        assert res.returncode == 1, "Failed to reject invalid field types"
        assert "Missing or invalid type for field" in res.stdout

def test_bad_urls():
    with tempfile.TemporaryDirectory() as temp_dir:
        cat = get_base_catalog()
        item = get_base_item()
        item["source_url"] = None
        item["asset_url"] = "https://" # Missing hostname
        cat["items"] = [item]
        cat_path = create_temp_json(temp_dir, 'cat.json', cat)

        res = run_validator(cat_path)
        assert res.returncode == 1, "Failed to reject bad URLs"
        assert "URL must be a non-empty string" in res.stdout
        assert "Invalid URL format or missing hostname" in res.stdout

def test_ambiguous_local_rights():
    with tempfile.TemporaryDirectory() as temp_dir:
        cat = get_base_catalog()
        item = get_base_item()
        item["local_path"] = "some_file.jpg"
        # We need to create a dummy file to bypass the missing file check
        open(os.path.join(temp_dir, "some_file.jpg"), 'w').close()

        item["rights_status"] = "official_press_or_reference"
        item["rights_evidence"] = "Official hosting; no reuse permission found."
        cat["items"] = [item]
        cat_path = create_temp_json(temp_dir, 'cat.json', cat)

        res = run_validator(cat_path)
        assert res.returncode == 1, "Failed to reject ambiguous rights status for local file"
        assert "Unsafe or unrecognized rights_status" in res.stdout

def test_null_local_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        cat = get_base_catalog()
        item = get_base_item()
        item["local_path"] = None # Should not throw TypeError
        cat["items"] = [item]
        cat_path = create_temp_json(temp_dir, 'cat.json', cat)

        res = run_validator(cat_path)
        assert res.returncode == 0, f"Failed on null local_path, stdout: {res.stdout}, stderr: {res.stderr}"

if __name__ == "__main__":
    test_duplicate_ids()
    test_invalid_types()
    test_bad_urls()
    test_ambiguous_local_rights()
    test_null_local_path()
    print("All negative fixture tests passed.")
