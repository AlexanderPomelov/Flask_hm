from abc import ABC
from typing import Optional

import pydantic

class AbstractAnnouncement(pydantic.BaseModel, ABC):
    title: str


class CreateAnnouncement(AbstractAnnouncement):
    title: str


class UpdateAnnouncement(AbstractAnnouncement):
    title: Optional[str] = None
