import sys
import types

sys.modules.setdefault("numpy", types.ModuleType("numpy"))
sys.modules.setdefault("pandas", types.ModuleType("pandas"))

from utils import storage
from localization import translations


def test_user_context_basic():
    uc = storage.UserContext()
    uc.add_new_user(1)
    uc.set_user_info_field(1, "language", "en")
    assert uc.get_user_info_field(1, "language") == "en"


def test_get_translation(monkeypatch):
    uc = storage.UserContext()
    uc.add_new_user(2)
    uc.set_user_info_field(2, "language", "de")
    monkeypatch.setattr(storage, "context", uc)
    result = storage.get_translation(2, "yes")
    assert result == translations["yes"]["de"]


def test_get_user_profile(monkeypatch):
    uc = storage.UserContext()
    uc.add_new_user(3)
    uc.set_user_info_field(3, "language", "en")
    uc.set_user_info_field(3, "gender", "male")
    uc.set_user_info_field(3, "age", 30)
    monkeypatch.setattr(storage, "context", uc)
    profile = storage.get_user_profile(3)
    assert "User ID: 3" in profile
    assert "Age: 30" in profile


