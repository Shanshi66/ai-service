from abc import ABC, abstractmethod
from enum import Enum
from typing import Any
from fastapi import Depends

from pydantic import HttpUrl
from models import Config


class AIService(ABC):
    @abstractmethod
    def summary(self, doc: str) -> str:
        pass
