import os
import subprocess
import json

def test_negative_fixture():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    validator_path = os.path.join(base_dir, 'validator.py')

    # We will temporarily run the validator on the negative fixture
    # To do this cleanly, we temporarily copy negative_catalog to catalog
    # (assuming test environment is isolated or we can clean up)

    catalog_path = os.path.join(base_dir, 'catalog.json')
    negative_path = os.path.join(base_dir, 'negative_catalog.json')
    backup_path = os.path.join(base_dir, 'catalog.json.bak')

    # Backup real catalog
    os.rename(catalog_path, backup_path)
    # Put negative in place
    os.rename(negative_path, catalog_path)

    try:
        # Run validator, expect it to fail (return non-zero)
        result = subprocess.run(['python3', validator_path, '--as-of', '2026-10-11'], capture_output=True, text=True)
        assert result.returncode == 1, "Validator should have failed on negative fixture!"

        output = result.stdout
        # Check that specific errors were caught
        assert "is in the future" in output, "Failed to catch future generated_at date"
        assert "Invalid URL format" in output, "Failed to catch bad URL scheme"
        assert "Path traversal detected" in output, "Failed to catch path traversal in local_path"
        assert "reference_only items must NOT have a local_path" in output, "Failed to catch local_path used with reference_only"

        print("Negative fixture tests passed. Validator successfully caught the intentional errors.")
    finally:
        # Restore files
        os.rename(catalog_path, negative_path)
        os.rename(backup_path, catalog_path)

if __name__ == "__main__":
    test_negative_fixture()
