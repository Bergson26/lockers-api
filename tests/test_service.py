import os
import tempfile

import pytest

from app import service, storage


@pytest.fixture(autouse=True)
def tmp_data(monkeypatch):
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    os.remove(path)
    monkeypatch.setattr(storage, "DATA_FILE", path)
    yield
    if os.path.exists(path):
        os.remove(path)


def test_set_status():
    service.set_status("A1", "occupied")


def test_unknown_status():
    with pytest.raises(service.UnknownStatus):
        service.set_status("A1", "broken")


def test_occupancy_rate():
    service.set_status("A1", "occupied")
    service.set_status("A2", "free")
    service.set_status("A3", "free")
    assert service.occupancy_rate() == 33.33
