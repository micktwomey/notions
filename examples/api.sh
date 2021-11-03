#!/usr/bin/env bash

# Examples of using the `notions api` command to perform GET requests

set -xeuo pipefail

# `notions api` examples

#
# Listing databases
#
# This will return the raw (json) response from the Notion API
notions --debug api GET /v1/databases
# This will return a YAML formatted version, you need to use --paginate to trigger parsing
notions --debug --output-format yaml api --paginate GET /v1/databases/
# This will return a CSV formatted output
notions --debug --output-format csv api --paginate GET /v1/databases/

#
# Getting pages
#
notions --debug api GET "/v1/pages/${NOTIONS_PARENT_PAGE_UUID}"

#
# Searching
#
notions --debug api POST "/v1/search"
