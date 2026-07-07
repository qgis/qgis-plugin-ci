from pytest import Config

from .utils import can_skip_test_github, can_skip_test_transifex


def pytest_report_header(config: Config):
    _ = config
    return (
        f"Running Transifex tests : {not can_skip_test_transifex()}\n"
        f"Running GitHub tests : {not can_skip_test_github()}\n"
    )
