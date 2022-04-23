set dotenv-load := true
poetry_run := if env_var_or_default("POETRY_ACTIVE", "0") == "1" {""} else {"poetry run "}
pytest := poetry_run + "pytest"
nox := poetry_run + "nox"
changelog_manager := poetry_run + "changelog-manager"

default: pytest

pytest *ARGS='-vv --log-level=INFO -m "not slow"':
    {{pytest}} {{ARGS}} tests

pytest-all *ARGS='-vv --log-level=INFO':
    {{pytest}} {{ARGS}} tests

nox *ARGS:
    {{nox}} {{ARGS}}

# Add a CHANGELOG.md entry, e.g. just changelog-add added "My entry"
changelog-add TYPE ENTRY:
    {{changelog_manager}} add {{TYPE}} {{ENTRY}}

# Install and bootstrap your dev env, usually a one off
bootstrap-dev-env:
    asdf install
    poetry install
    poetry run pre-commit install

# Find out what your next released version might be based on the changelog.
next-version:
    {{changelog_manager}} suggest

# Build and create files for a release
prepare-release:
    #!/bin/bash
    set -xeuo pipefail
    {{changelog_manager}} release
    poetry version $(changelog-manager current)
    rm -rvf dist
    poetry build

# Tag and release files, make sure you run 'just prepare-release' first.
do-release:
    #!/bin/bash
    set -xeuo pipefail
    VERSION=$({{changelog_manager}} current)
    POETRY_VERSION=$(poetry version -s)
    if [ "${VERSION}" != "${POETRY_VERSION}" ]; then
        echo "Mismatch between changelog version ${VERSION} and poetry version ${VERSION}"
        exit 1
    fi
    git add pyproject.toml CHANGELOG.md
    mkdir -p build
    {{changelog_manager}} display --version $VERSION > build/release-notes.md
    if [ ! -f dist/notions-${VERSION}.tar.gz ]; then
        echo "Missing expected file in dist, did you run 'just prepare-release'?"
        exit 1
    fi
    poetry publish --dry-run
    git commit -m"Release ${VERSION}"
    git tag $VERSION
    git push origin $VERSION
    git push origin main
    gh release create $VERSION --title $VERSION -F build/release-notes.md ./dist/*
    poetry publish
    rm -rvf ./dist
