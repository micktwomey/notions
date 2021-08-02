# Expand current version early to ensure later version changes aren't picked up
CURRENT_VERSION:=$(shell poetry version -s)

.PHONY: all
all: test

.PHONY: dep
dep:
	poetry install
	poetry run pre-commit install

.PHONY: build
build: test

.PHONY: test
test:
	poetry run nox

.PHONY: pytest
pytest:
	poetry run pytest -vv --tb=short --log-level=DEBUG

.PHONY: check-repo-is-clean
check-repo-is-clean:
	# Quick and dirty check for pending commits
	git diff --exit-code
	git diff --cached --exit-code

.PHONY: release
release: check-repo-is-clean
	rm -rf $(CURDIR)/dist
	poetry build
	# Set poetry credentials to save typing them in all the time
	# See https://python-poetry.org/docs/repositories/#configuring-credentials
	poetry publish --dry-run
	gh release create --title $(CURRENT_VERSION) $(CURRENT_VERSION) dist/*
	poetry publish

.PHONY: bump-prerelease
bump-prerelease: check-repo-is-clean
	poetry version prerelease
	git add -p pyproject.toml
	git commit -m "Bump pre-release version to $(shell poetry version -s) from $(CURRENT_VERSION)"
	git push

.PHONY: bump-prepatch
bump-prepatch: check-repo-is-clean
	poetry version prepatch
	git add -p pyproject.toml
	git commit -m "Bump pre-patch version to $(shell poetry version -s) from $(CURRENT_VERSION)"
	git push

.PHONY: bump-patch
bump-patch: check-repo-is-clean
	poetry version patch
	git add -p pyproject.toml
	git commit -m "Bump patch version to $(shell poetry version -s) from $(CURRENT_VERSION)"
	git push

.PHONY: bump-preminor
bump-preminor: check-repo-is-clean
	poetry version preminor
	git add -p pyproject.toml
	git commit -m "Bump pre-minor version to $(shell poetry version -s) from $(CURRENT_VERSION)"
	git push

.PHONY: bump-minor
bump-minor: check-repo-is-clean
	poetry version minor
	git add -p pyproject.toml
	git commit -m "Bump minor version to $(shell poetry version -s) from $(CURRENT_VERSION)"
	git push

.PHONY: bump-premajor
bump-premajor: check-repo-is-clean
	poetry version premajor
	git add -p pyproject.toml
	git commit -m "Bump pre-major version to $(shell poetry version -s) from $(CURRENT_VERSION)"
	git push

.PHONY: bump-major
bump-major: check-repo-is-clean
	poetry version major
	git add -p pyproject.toml
	git commit -m "Bump major version to $(shell poetry version -s) from $(CURRENT_VERSION)"
	git push
