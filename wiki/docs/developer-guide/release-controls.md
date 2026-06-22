# Release controls

Release control is enforced by `wiki/scripts/validate_wiki.py` and `tests/test_wiki.py`.

Before tagging a release, confirm:

- `pyproject.toml` project version matches `caereflex/version.py`.
- The package version has a matching `wiki/docs/releases/<version>.md` page.
- The release page declares the current ReflexCase schema version.
- `CHANGELOG.md` contains the package version.
- `wiki/mkdocs.yml` includes the release page in navigation.
- The wiki documents all current CLI commands.
- The wiki documents all current REST routes.
- The wiki names the implemented adapters.
- The wiki contains the safe-use/do-not-claim limitations.
- `mkdocs build --strict` succeeds.

The current documentation policy is current-version wiki pages plus frozen release summary pages. Full historical documentation trees should only be added if multiple supported release lines exist.
