from __future__ import annotations

import importlib
import json
from dataclasses import asdict
from typing import Dict, Optional
from pathlib import Path

from .models import FlowNode


class FlowConfigError(Exception):
    pass


class FlowEngine:
    """Loads and validates the dialogue flow and exposes navigation helpers.

    Contract
    - start: start node id
    - text_key(node_id) -> i18n key (str)
    - state(node_id) -> TeleBot State object or None
    - next(current, event=None) -> next node id or None
    """

    def __init__(self, path: str | Path) -> None:
        self._path = str(path)
        self._start: str = ""
        self._nodes: Dict[str, FlowNode] = {}
        self._raw_nodes: Dict[str, dict] = {}
        self._load()
        self._validate()

    @property
    def start(self) -> str:
        return self._start

    def text_key(self, node_id: str) -> str:
        return self._nodes[node_id].text_key

    def state(self, node_id: str):
        node = self._nodes[node_id]
        if not node.state:
            return None
        # resolve dotted notation like "SurveyStates.age"
        dotted = node.state
        if "." not in dotted:
            raise FlowConfigError(f"Invalid state reference '{dotted}' in node '{node_id}'")
        group_name, state_name = dotted.split(".", 1)
        try:
            states_mod = importlib.import_module("states")
        except Exception as e:
            raise FlowConfigError(f"Cannot import states module: {e}")
        try:
            group = getattr(states_mod, group_name)
        except AttributeError as e:
            raise FlowConfigError(f"Unknown state group '{group_name}' for node '{node_id}'")
        try:
            return getattr(group, state_name)
        except AttributeError:
            raise FlowConfigError(
                f"Unknown state '{state_name}' in group '{group_name}' for node '{node_id}'"
            )

    def next(self, current: str, event: Optional[str] = None) -> Optional[str]:
        node = self._nodes.get(current)
        if not node:
            return None
        nxt = None
        if event is not None:
            nxt = node.next.get(str(event))
        if not nxt:
            nxt = node.next.get("default")
        return nxt

    def _load(self) -> None:
        p = Path(self._path)
        if not p.exists():
            raise FlowConfigError(f"Flow config not found: {self._path}")
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            raise FlowConfigError(f"Failed to parse flow config as JSON: {e}")

        start = data.get("start")
        nodes = data.get("nodes")
        if not isinstance(start, str) or not isinstance(nodes, dict):
            raise FlowConfigError("Invalid flow file: must contain 'start' and 'nodes' map")

        self._start = start
        self._raw_nodes = nodes
        self._nodes = {}
        for node_id, raw in nodes.items():
            if not isinstance(raw, dict):
                raise FlowConfigError(f"Node '{node_id}' must be a mapping")
            text_key = raw.get("text_key")
            state = raw.get("state")
            next_map = raw.get("next", {})
            if not isinstance(text_key, str) or not isinstance(next_map, dict):
                raise FlowConfigError(f"Node '{node_id}' missing 'text_key' or has invalid 'next'")
            if state is not None and not isinstance(state, str):
                if state is not None:
                    raise FlowConfigError(f"Node '{node_id}' has invalid 'state' type")
            self._nodes[node_id] = FlowNode(id=node_id, text_key=text_key, state=state, next=next_map)

    def _validate(self) -> None:
        if self._start not in self._nodes:
            raise FlowConfigError(f"Start node '{self._start}' not found in nodes")
        for node in self._nodes.values():
            for _, target in node.next.items():
                if target not in self._nodes:
                    raise FlowConfigError(
                        f"Node '{node.id}' has transition to unknown node '{target}'"
                    )

    def as_dict(self) -> dict:
        return {
            "start": self._start,
            "nodes": {nid: asdict(n) for nid, n in self._nodes.items()},
        }

