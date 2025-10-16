# conftest.py
# Este arquivo de configuração ensina ao Pytest como capturar
# o resultado de cada teste para que possamos tirar screenshots.

import pytest

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook do Pytest que é executado após cada fase do teste (setup, call, teardown).
    """
    outcome = yield
    rep = outcome.get_result()

    # Armazena o resultado de cada fase (rep.when) no objeto do item do teste.
    # Ex: item.rep_setup, item.rep_call, item.rep_teardown
    setattr(item, "rep_" + rep.when, rep)