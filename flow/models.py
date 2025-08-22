from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class FlowNode:
    """A single dialogue node.

    Fields
    - id: unique node identifier
    - text_key: i18n key to render
    - state: fully-qualified TeleBot state attribute (e.g., "SurveyStates.age"), or None
    - next: mapping of event -> next node id; may include "default"
    """

    id: str
    text_key: str
    state: Optional[str]
    next: Dict[str, str]

