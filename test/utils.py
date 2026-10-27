import os


def can_skip_test_github():
    """Check when the GitHub test can run."""
    if os.getenv("CI") == "true":
        # On CI, always run the test when secrets are available (see test workflow)
        return os.getenv("HAS_SECRETS") != "true"

    return not os.getenv("github_token")


def can_skip_test_transifex():
    """Check when the Transifex test can run."""
    if os.getenv("CI") == "true":
        # On CI, always run the test when secrets are available (see test workflow)
        return os.getenv("HAS_SECRETS") != "true"

    return not os.getenv("tx_api_token")
