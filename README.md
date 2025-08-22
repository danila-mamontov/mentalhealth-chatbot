Demo Presentation

[<img width="50%">](https://github.com/user-attachments/assets/db90864c-5ead-40aa-8f80-452e3a45cc5e "Demo Video")


Declarative message flow

- Flow config: message_flow.yaml (JSON-in-YAML) defines nodes with: id, text_key, optional state (e.g., "SurveyStates.age"), and next transitions (event->node, plus optional "default").
- Engine: flow/engine.py loads, validates, and exposes start, text_key(node), state(node), next(current,event).
- Renderer: flow/renderer.py provides a singleton engine and render_node(bot, chat_id, node_id, fmt=None, menu=None, message_id=None). It sets state, resolves text via utils.storage.get_translation, optionally attaches menus (mapped in MENU_BY_NODE), and sends or edits the message.
- Handlers: start, consent, language, gender use engine.next(...) and render_node(...) while keeping registrations.
- Tests: tests/test_flow_engine.py validates loading, state resolution, transitions, and error cases.

Modify the flow

1) Add or edit a node in message_flow.yaml:
   {
     "text_key": "my_text_key",
     "state": "SurveyStates.some_state" | null,
     "next": { "eventA": "target_node", "default": "fallback_node" }
   }
2) Ensure the target nodes exist and update transitions accordingly. The engine raises FlowConfigError on bad start or unknown targets.
3) If the node needs buttons, wire a menu builder in flow/renderer.py MENU_BY_NODE mapping.
4) Use engine.next(current, event) and render_node(bot, chat_id, node_id, ...) from handlers to navigate.

Notes

- i18n keys must exist in locales/*.yml; renderer calls utils.storage.get_translation.
- TeleBot states are resolved dynamically from states.py based on the dotted string in "state".
- To fail fast on misconfigurations, importing flow.renderer will validate the flow at startup.
