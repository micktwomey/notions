CURRENT_VERSION=$(shell poetry version -s)

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

.PHONY: release
release:
	# Quick and dirty check for pending commits
	git diff --exit-code
	git diff --cached --exit-code
	rm -rf $(CURDIR)/dist
	poetry build
	gh release create --title $(CURRENT_VERSION) $(CURRENT_VERSION) dist/*
	poetry publish
