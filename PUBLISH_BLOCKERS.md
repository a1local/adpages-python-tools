# Publish Blockers

Before publishing to PyPI:

- Confirm ownership or availability of the `adpages-tools` package name.
- Finalize the license and add the license file.
- Add production repository, changelog, documentation, and support URLs to `pyproject.toml`.
- Build wheel and source distribution artifacts in a clean environment.
- Run `twine check` against the built artifacts.
- Install from the built wheel in a clean virtual environment and test the `adpages-tools` CLI.
- Recheck Google Ads responsive search ad copy limits against official Google Ads documentation.
- Add a few real tutorial examples that point back to the broader AdPages toolset.

Do not publish until these items are complete.

