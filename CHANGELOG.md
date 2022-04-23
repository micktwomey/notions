# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Add database and page creation
- Switch to just from make for running development commands
- Added this changelog
- Add a NotionAPIResponse model which handles all Notion API responses.
- Add a NotionAPIResponseError exception to wrap all API errors.

### Fixed
- Fix list database call

### Changed
- Refactor properties. Now a single module holds the database and page properties, as well as the create versions.
- Changed QueryDatabaseSort direction to an enum

### Removed
- Remove request and update modules, moving related classes into the respective database and page modules.

## [0.3.0] - 20221-08-24
### Added
- Add CSV and TSV support

## [0.2.0] - 20221-08-03
### Added
- Add flatter representations

## [0.1.1] - 2021-08-02
### Added
- Initial release
- Creating library to talk to Notion API
