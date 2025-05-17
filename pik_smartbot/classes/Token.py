from datetime import datetime, timezone, timedelta
import uuid
from dataclasses import dataclass, field


@dataclass
class Token:
    _token: str = field(default_factory=lambda: str(uuid.uuid4()))
    _create_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def token(self) -> str:
        return self._token

    @property
    def create_at(self) -> datetime:
        return self._create_at

    #Проверяем действителен ли токен
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self._create_at + timedelta(hours=12)


    def update(self):
        self._token = str(uuid.uuid4())
        self._create_at = datetime.now(timezone.utc)

