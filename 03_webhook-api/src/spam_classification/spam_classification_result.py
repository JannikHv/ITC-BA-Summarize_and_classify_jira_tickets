from dataclasses import dataclass
import json

@dataclass(frozen=True)
class SpamClassificationResult:
    spam: float

    @property
    def ham(self) -> float: return 1 - self.spam

    @property
    def json(self) -> dict: return { 'spam': self.spam, 'ham': self.ham }

    @property
    def json_string(self) -> str: return json.dumps(self.to_json())