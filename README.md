# Notions - A Python Client Library and CLI for Notion

A command line client and API library for [Notion](https://notion.so).

Uses the [Notion API](https://developers.notion.com) to communicate with your Notion pages and databases.

* Homepage: https://github.com/micktwomey/notions
* Repo: https://github.com/micktwomey/notions
* PyPI project page: https://pypi.org/project/notions/

- [Notions - A Python Client Library and CLI for Notion](#notions---a-python-client-library-and-cli-for-notion)
- [Installation](#installation)
  - [pipx for CLI usage anywhere](#pipx-for-cli-usage-anywhere)
  - [pip](#pip)
  - [poetry](#poetry)
  - [pipenv](#pipenv)
- [Authentication](#authentication)
- [Command Line Usage](#command-line-usage)
  - [Output Formats](#output-formats)
  - [Commands](#commands)
    - [notions api](#notions-api)
    - [notions search](#notions-search)
    - [notions database list](#notions-database-list)
    - [notions database query](#notions-database-query)
    - [notions page get](#notions-page-get)
- [API](#api)
- [Developing Notions](#developing-notions)
- [What's the deal with the name?](#whats-the-deal-with-the-name)

# Installation

## pipx for CLI usage anywhere

To install as a CLI and make it available on your PATH you can use [pipx](https://pypa.github.io/pipx/) to install:

```sh
pipx install notions
```

## pip

To install using [pip](https://pip.pypa.io/en/stable/):

```sh
pip install notions
```

## poetry

To add as a depdency using [poetry](https://python-poetry.org):

```sh
poetry add notions
```

## pipenv

To add as a dependency using [pipenv](https://pipenv.pypa.io/en/latest/):

```sh
pipenv install notions
```

# Authentication

Currently only authentication using an Notion API token is supported (see [Notion's Getting Started Guide](https://developers.notion.com/docs#getting-started) for full details).

Rough steps to get a token you can use:
1. Go to https://www.notion.so/my-integrations
2. Create a new internal integration
3. Note down the API key, you'll need that later
4. Go to a Database or page in your notion (a top level item in your sidebar) and click on the sharing button
5. Add your integration to the shares. You need to do this for every database you want to share, Notion doesn't expose everything by default.

# Command Line Usage

1. Authenticate first, see [Authentication](#authentication), and get your API token (we'll refer to it as `YOUR_KEY_GOES_HERE` below)
2. You can either pass in the key each time you call the client using `notions --notion-api-key YOUR_KEY_GOES_HERE` or set the `NOTION_API_KEY` environment variable.
   1. To set in fish: `set -Ux NOTION_API_KEY YOUR_KEY_GOES_HERE`
   2. To set in bash/zsh: `export NOTION_API_KEY=YOUR_KEY_GOES_HERE`
3. Call `notions --help` to explore your options

Some options are global and go before the command, e.g. `notions --output-format notion_yaml database query --query foo`.

## Output Formats

Formats you can specify with `notions --output-format`
1. `notion_json` - Parses API output and dumps back as JSON, with multiple items contained in a list.
2. `notion_jsonl` - Parses API output and dumps back as JSON, one JSON object per line.
3. `notion_yaml` - Parses API output and dumps back as YAML, with multiple items in a list.
4. `text` (default) - Parse API output and return a simple text representation. Handy for looking up page and database ids.
5. `json` - Parses API output and dumps to a flatter JSON, more suitable for templating and processsing. Multiple items are placed in a list.
6. `jsonl` - Parses API output and dumps to a flatter JSON, one per line, more suitable for templating and processsing.
7. `yaml` - Parses API output and dumps to a flatter YAML, more suitable for templating and processsing. Multiple items are placed in a list.

## Commands

### notions api

`notions api` allows you to issue requests using the authentication features of the client.

1. To make a request and get back the response JSON: `notions api METHOD PATH`.
2. To make a request and leverage the pagination support (this will parse the response and give you the option to render as YAML or other formats): `notions api --paginate METHOD PATH`. Note that due to how the flags are handled you need the `--paginate` to trigger parsing and allow for different output formats.

```sh
# Get all databases, without pagination and return raw JSON from Notion's API
notions api GET /v1/databases/

# Get all databases with pagination and format output as YAML
# This is the same as `notions --output-format yaml database list`
notions --output-format yaml api GET /v1/databases/ --paginate
```

### notions search

`notions search` allows you to search across all databases and pages you have shared with the Notion integration you created. You can restrict the search with `--query SOME_QUERY_STRING` and items which have a matching title will be returned.

```sh
# show all pages and dbs with "example" in their title
notions search --query example
```

### notions database list

`notions database list` lists all the databases the integration has access to.

### notions database query

Run a query against all pages in a given database. You'll need the database UUID from something like `notions database list`.

```sh
# Show all pages in the given db and sort by the HP property in descending order
notions database query cc5ef123-05f5-409e-9b34-38043df965b0 --sort-property HP:descending
```

### notions page get

Get a single page.

```sh
# Get a page in YAML
notions --output-format yaml page get ccad10e7-c776-423e-9662-6ad5fb1256d6
```

# API

The main way to use the library is via the HTTP client (see [examples/basic.py](examples/basic.py) for same code):


```python
"""Example showing basic use of the client for API calls
"""

import asyncio
import os
import typing

import httpx

from notions.client import NotionAsyncClient
from notions.models.database import Database


async def http_list_databases(notion_client: NotionAsyncClient) -> httpx.Response:
    """Do a HTTP call with authentication to list databases

    This uses notions as a convenience for HTTP calls using httpx
    """
    async with notion_client.async_client() as client:
        url = notion_client.get_url_for_path("/v1/databases")
        return await client.request("GET", url.url)


async def list_databases(
    notion_client: NotionAsyncClient,
) -> typing.AsyncIterable[Database]:
    """Do a list db call (automatically reads all pages)

    This is the same underlying call as `http_list_databases` above
    but will also parse the response and handle pagination.

    Will yield notions.models.database.Database
    """
    async for db in notion_client.list_databases():
        yield db


async def main():
    api_token = os.environ.get("NOTION_API_KEY", "no-token-set")
    notion_client = NotionAsyncClient(api_token)

    response = await http_list_databases(notion_client)
    print(response)
    print(response.json())
    response.raise_for_status()

    async for db in list_databases(notion_client):
        print(db.id)
        print(db.title)
        print(db)


if __name__ == "__main__":
    asyncio.run(main())

```

# Developing Notions

To develop locally you'll need python 3.6+, [poetry](https://python-poetry.org) and make:

1. `make dep` to set up the development environment.
2. `make test` to test all supported pythons or `make pytest` to run tests more directly for your python.

You'll need a plan which allows for creating Notion integrations (API access) to develop against Notion, but I'm going to assume you have that if you're interested in this library :D

To release ensure you're happy with the current state of main and run `make release`.

# What's the deal with the name?

"Notions" is sometimes used in Ireland to refer to someone who has ideas abover their station ("so and so has notions"). It's typically Irish and a little bit mean, but often used in an ironic way. I picked it 'cos I thought it'd be funny (and maybe I have notions about writing a client library for a product produced by a company called Notion).
