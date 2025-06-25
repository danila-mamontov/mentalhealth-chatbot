from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class VoiceAnswer:
    """Metadata for a single voice response."""

    user_id: int
    question_id: int
    file_unique_id: str
    file_id: str
    file_path: str
    duration: int
    timestamp: int
    file_size: int
    saved: bool = False


class SurveySession:
    """Track progress and answers for a survey run."""

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.current_index: int = 0
        # question index -> answer value
        self.answers: Dict[int, object] = {}
        # telegram message id -> VoiceAnswer
        self.voice_messages: Dict[int, VoiceAnswer] = {}
        # question index -> list of voice message ids in order
        self.question_voice_ids: Dict[int, List[int]] = {}

    # progress helpers
    def next_question(self) -> int:
        self.current_index += 1
        return self.current_index

    def prev_question(self) -> int:
        if self.current_index > 0:
            self.current_index -= 1
        return self.current_index

    def jump_to(self, index: int) -> int:
        if index < 0:
            index = 0
        self.current_index = index
        return self.current_index

    # voice handling
    def record_voice(self, message_id: int, meta: VoiceAnswer) -> None:
        """Store voice metadata for later persistence."""

        self.voice_messages[message_id] = meta
        self.question_voice_ids.setdefault(meta.question_id, []).append(message_id)


    def iter_voice_answers(self):
        """Yield stored voice answers."""
        for msg_id, meta in self.voice_messages.items():
            yield msg_id, meta

    def get_question_voice_answers(self, question_index: int) -> List[VoiceAnswer]:
        """Return voice answers stored for ``question_index`` in order."""

        ids = self.question_voice_ids.get(question_index, [])
        return [self.voice_messages[i] for i in ids if i in self.voice_messages]


class SurveyManager:
    """Simple singleton managing survey sessions."""

    _sessions: Dict[int, SurveySession] = {}

    @classmethod
    def get_session(cls, user_id: int) -> SurveySession:
        session = cls._sessions.get(user_id)
        if session is None:
            session = SurveySession(user_id)
            cls._sessions[user_id] = session
        return session

    @classmethod
    def remove_session(cls, user_id: int) -> None:
        cls._sessions.pop(user_id, None)
