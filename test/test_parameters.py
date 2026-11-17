#! /usr/bin/env python

# standard
import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

# Project
from qgispluginci.exceptions import ConfigurationNotFound
from qgispluginci.parameters import Parameters


class TestParameters(unittest.TestCase):
    def test_changelog_parameters(self):
        """Test parameters for changelog command."""
        # For the changelog command, the configuration file is optional.
        # It mustn't raise an exception
        parameters = Parameters.make_from(args={}, optional_configuration=True)
        self.assertIsNone(parameters.plugin_path)
        self.assertEqual("CHANGELOG.md", parameters.changelog_path)

    def test_global_parameters(self):
        """Test global parameters."""
        # A configuration file must exist.
        with self.assertRaises(ConfigurationNotFound):
            Parameters.make_from(
                args={}, path_to_config_file=Path("does-not-exist.yml")
            )

        # Existing configuration file
        parameters = Parameters.make_from(
            args={}, path_to_config_file=Path("test/fixtures/pyproject.toml")
        )
        self.assertIsInstance(parameters.create_datetime, datetime)
        self.assertIsNotNone(parameters.create_datetime.tzinfo)

        self.assertEqual("qgis_plugin_CI_testing", parameters.plugin_path)
        self.assertEqual("CHANGELOG.md", parameters.changelog_path)
        self.assertIsNone(parameters.plugin_repo_url)

    def test_plugin_repo_url_from_config(self):
        """--plugin-repo-url must be read from config file (repository_plugin_url)."""
        parameters = Parameters.make_from(
            path_to_config_file=Path("test/fixtures/.qgis-plugin-ci")
        )
        self.assertEqual(
            "https://qgis.github.io/qgis-plugin-ci/", parameters.plugin_repo_url
        )

    def test_metadata_multiline_values(self):
        """Values may span several lines, and '#' or ';' in them are kept."""
        metadata = """[general]
name=Multi-line Plugin
qgisMinimumVersion=3.40
description=Plugin with #hashtag in its description
version=dev

# Recommended items:

changelog=
    Fixed #123

    #456 is fixed too
    ; this is not a comment either
    see https://example.com/?key=value
# Tags are comma separated with spaces allowed
tags = one, two
about=
    First line of about.<br>
    Second line of about.
tracker=https://example.com/issues
repository=https://example.com/repository

[tool:qgis-plugin-ci]
commitNumber=
"""
        with TemporaryDirectory() as plugin_path:
            Path(plugin_path, "metadata.txt").write_text(metadata)
            parameters = Parameters({"plugin_path": plugin_path})
            get_metadata = parameters.collect_metadata()

        self.assertEqual(
            "First line of about.<br>\nSecond line of about.", parameters.about
        )
        self.assertEqual(
            "Plugin with #hashtag in its description", parameters.description
        )
        self.assertEqual(
            "Fixed #123\n\n#456 is fixed too\n"
            "; this is not a comment either\n"
            "see https://example.com/?key=value",
            get_metadata("changelog"),
        )
        self.assertEqual("one, two", parameters.tags)
        self.assertEqual("https://example.com/issues", parameters.issue_tracker)
        self.assertEqual("https://example.com/repository", parameters.repository_url)
        self.assertEqual("default", get_metadata("commitNumber", "default"))
