from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

from .engine import FlowEngine
from utils.storage import get_translation

# Lazy imports for menu callables to avoid circulars at import time
from utils import menu as menus

# Load engine once at import
_engine_path = Path(__file__).resolve().parents[1] / "message_flow.yaml"
engine = FlowEngine(_engine_path)

# Map node id -> menu builder callable(chat_id) -> InlineKeyboardMarkup
MENU_BY_NODE: dict[str, Callable[[int], object]] = {
    "language_confirm": menus.consent_menu,
    "language": lambda _t: menus.language_menu(),
    "consent": menus.consent_menu,
    "gender": menus.gender_menu,
    "age": menus.age_range_menu,
    "main_menu": menus.main_menu,
}


def render_node(
    bot,
    chat_id: int,
    node_id: str,
    *,
    fmt: Optional[dict] = None,
    menu: Optional[Callable[[int], object]] = None,
    message_id: Optional[int] = None,
) -> Optional[int]:
    """Render a node and return the affected message_id if available.

    - If message_id is provided, edits that message and returns the same id.
    - Otherwise sends a new message and returns its id (if available from bot API).
    """
    # set state if any
    state = engine.state(node_id)
    if state is not None:
        bot.set_state(chat_id, state, chat_id)

    key = engine.text_key(node_id)
    text = get_translation(chat_id, key)
    if fmt:
        try:
            text = text.format(**fmt)
        except Exception:
            pass

    menu_fn = menu if menu is not None else MENU_BY_NODE.get(node_id)
    markup = menu_fn(chat_id) if menu_fn else None

    if message_id is not None:
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                parse_mode="HTML",
                reply_markup=markup,
            )
        except Exception:
            try:
                msg = bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup)
                return getattr(msg, "message_id", None)
            except Exception:
                return None
        else:
            return message_id
    else:
        try:
            msg = bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup)
            return getattr(msg, "message_id", None)
        except Exception:
            return None
