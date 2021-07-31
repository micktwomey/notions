# Notions - A Python Client Library and CLI for Notion

A command line client and API library for [Notion](https://notion.so).

Uses the [Notion API](https://developers.notion.com) to communicate with your Notion pages and databases.

# Installation

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

## pipx

To install as a CLI and make it available on your PATH you can use [pipx](https://pypa.github.io/pipx/) to install:

```sh
pipx install notions
```

# Authentication

Currently only authentication using an Notion API token is supported (see [Notion's Getting Started Guide](https://developers.notion.com/docs#getting-started) for full details):

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
