# Changelog (CLI)

Manipulate `CHANGELOG.md` file, extracting relevant information.  
Used within the [package](cli_package) and [release](cli_release) commands to populate the `metadata.txt` and the GitHub Release description.

By default, the script will look for a file `CHANGELOG.md` in the root folder.
But you can specify a specific file path with `changelog_path` in the configuration file.
For instance:

```ini
changelog_path=CHANGELOG-3.4.md
```

or

```ini
changelog_path=subfolder/CHANGELOG.md
```

## Command help

```{argparse}
:func: make_parser
:module: qgispluginci.cli
:path: changelog
:prog: qgis-plugin-ci
```

## Requirements

The `CHANGELOG.md` file must follow the convention [Keep A Changelog](https://keepachangelog.com/). For example, see this [repository changelog](https://github.com/opengisch/qgis-plugin-ci/blob/master/CHANGELOG.md).

:::{warning}
Currently the "Unreleased" section and subsections (e.g. "Fixed" etc) are not supported, see [#56](https://github.com/opengisch/qgis-plugin-ci/issues/56).
:::

## Use cases

- Extract the `CHANGELOG.md` content and copy it into the `changelog` section within plugin `metadata.txt`
- Extract the `n` latest versions from `CHANGELOG.md` into `metadata.txt`
- Get the latest version release note

## Examples

### Extract changelog for latest version

```bash
$ qgis-plugin-ci changelog latest
- Separate python files and UI files in the temporary PRO file (#29)
```
