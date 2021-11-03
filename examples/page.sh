#!/usr/bin/env bash

# `notions page` examples

set -euo pipefail

notions --debug page get "${NOTIONS_PARENT_PAGE_UUID}"
