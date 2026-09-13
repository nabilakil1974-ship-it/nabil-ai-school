# NABIL AI — automatic CRDP curriculum sync

The platform checks the official CRDP sources once per day and updates the
static curriculum catalogue consumed by the lesson page.

Official monitored sources:

- `https://www.crdp.org/`
- `https://www.crdp.org/curriculum`
- `https://www.crdp.org/curriculum1/173`
- `https://www.crdp.org/books-pdf`

## Safety policy

- Only `crdp.org` and `www.crdp.org` links are accepted.
- New resources and confidently identified grade/subject pairs are added.
- Existing lessons, books, and subjects are never deleted automatically.
- If CRDP is unavailable or redirects outside its official domain, the current
  working index remains untouched and the workflow fails visibly.
- A heading is not converted into an invented lesson. Detailed lesson titles
  remain subject to the platform's existing verified-content boundary.

## Manual test

```bash
python -m unittest discover -s tests -p 'test_sync_crdp_curriculum.py'
python scripts/sync_crdp_curriculum.py
```

The second command is a dry run. To write the changes locally:

```bash
python scripts/sync_crdp_curriculum.py --apply
```

GitHub Actions also provides a **Run workflow** button for an immediate check.
