"""Expose all handler modules for convenient importing.

Importing handlers as a package is used by ``bot.py`` which expects each
handler module to be available as an attribute of the package:

``from handlers import start_handler, treatment_handler``

To support that style the initializer eagerly imports the modules listed in
``__all__`` so they become attributes on the package object.
"""

from importlib import import_module

__all__ = [
    "profile_handler",
    "age_handler",
    "goto_handler",
    "start_handler",
    "help_handler",
    "delete_me_handler",
    "gender_handler",
    "consent_handler",
    "language_handler",
    "treatment_handler",
    "depression_handler",
    "depressive_handler",
    "main_menu_handler",
    "phq9_survey_handler",
    "wbmms_survey_handler",
    "voice_handler",
]

for name in __all__:
    globals()[name] = import_module(f".{name}", __name__)

