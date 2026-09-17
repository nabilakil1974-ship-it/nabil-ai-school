name: CRDP Master Curriculum Sync

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  sync:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests pymupdf

      - name: Run CRDP sync
        run: |
          python scripts/sync_crdp_master_curriculum.py /tmp/crdp_official app/static/crdp_master_curriculum_index.json

      - name: Validate curriculum
        run: |
          python scripts/validate_crdp_master_curriculum.py app/static/crdp_master_curriculum_index.json

      - name: Upload generated index
        uses: actions/upload-artifact@v4
        with:
          name: crdp-master-curriculum-index
          path: app/static/crdp_master_curriculum_index.json
          if-no-files-found: error
