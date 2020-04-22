# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.4] - 2020-04-21
### Added
- Add `gdbundle_list` command to LLDB
- Add Dockerfile, Tox, and Conda based testing on PR's and master branch

## [0.0.3] - 2020-04-16
### Added
- Get LLDB `gdbundle.init()` working again
- Add `url` and `homepage` to `pyproject.toml`

### Changed
- Rename `commands.py` to `commands_gdb.py` since it only contains GDB commands for now.

## [0.0.2] - 2020-04-14
### Added
- Prettier printing of `gdbundle list` command
- Added `load_module` to allow users to explicitly load a gdbundle plugin that
  doesn't being with `gdbundle_`

### Changed
- Updated README.md to match the announcement post

## [0.0.1] - 2020-04-14

- Initial Release to the world
