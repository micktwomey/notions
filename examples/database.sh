#!/usr/bin/env bash

# `notions database` examples

set -euo pipefail

# List all databases
notions --debug database list

# Get ID of first DB
DATABASE_ID=$(notions  --output-format json database list | jq -r '.[0].id')

# Query it for pages
notions --debug database query "${DATABASE_ID}"
