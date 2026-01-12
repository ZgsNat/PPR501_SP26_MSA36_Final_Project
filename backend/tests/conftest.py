import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.__enter__.return_value = uow
    uow.__exit__.return_value = None
    uow.students = MagicMock()
    return uow