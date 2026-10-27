import os


def _can_skip_ci_token_tests() -> bool:
    """Check when token based tests can run, for the CI."""
    if not os.getenv("CI") == "true":
        # Function relevant only for CI
        # It's running locally, we can expect users to have tokens with environment variables to try
        # Environment variables will be checked later
        return False

    if os.getenv("head_repository") != "qgis/qgis-plugin-ci":
        # It's not the main repository, secrets from qgis/qgis-plugin-ci are not shared to a fork
        # so tests can be skipped, a comment will be added to the PR
        return True

    if os.getenv("GITHUB_ACTOR") == "dependabot[bot]":
        # If PR author is dependabot, it can skip token based tests
        return True

    # From the CI, token based tests should be able to run, tokens will be checked
    return False


def can_skip_test_github() -> bool:
    """Check when the Transifex test can run."""
    if _can_skip_ci_token_tests():
        return True

    if not os.getenv("github_token"):
        return True

    return False


def can_skip_test_transifex() -> bool:
    """Check when the Transifex test can run."""
    if _can_skip_ci_token_tests():
        return True

    if not os.getenv("tx_api_token"):
        return True

    return False
