import sys
import types
from pathlib import Path
import pytest

# Minimal telebot stubs so states.py can import
telebot_mod = types.ModuleType("telebot")
handler_backends = types.ModuleType("telebot.handler_backends")
handler_backends.StatesGroup = object
handler_backends.State = object
telebot_mod.handler_backends = handler_backends
sys.modules.setdefault("telebot", telebot_mod)
sys.modules.setdefault("telebot.handler_backends", handler_backends)

from flow.engine import FlowEngine, FlowConfigError


def test_engine_load_and_props():
    root = Path(__file__).resolve().parents[1]
    engine = FlowEngine(root / "message_flow.yaml")

    assert engine.start == "welcome"
    assert engine.text_key("welcome") == "welcome_message"

    import states
    assert engine.state("language") == getattr(states.SurveyStates, "language")
    assert engine.state("welcome") == getattr(states.SurveyStates, "welcome")
    assert engine.state("main_menu") == getattr(states.SurveyStates, "main_menu")

    # transitions
    assert engine.next("welcome") == "language_confirm"
    assert engine.next("language_confirm", event="yes") == "consent"
    assert engine.next("language_confirm", event="no") == "language"
    assert engine.next("gender") == "age"
    assert engine.next("age") == "main_menu"


def test_engine_validation_errors(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text('{"start": "nope", "nodes": {"a": {"text_key": "t", "next": {"default": "b"}}}}', encoding="utf-8")
    with pytest.raises(FlowConfigError):
        FlowEngine(bad)

    bad2 = tmp_path / "bad2.yaml"
    bad2.write_text('{"start": "a", "nodes": {"a": {"text_key": "t", "next": {"default": "b"}}}}', encoding="utf-8")
    with pytest.raises(FlowConfigError):
        FlowEngine(bad2)
