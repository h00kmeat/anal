from abc import ABC, abstractmethod
from typing import Any, Tuple

class Detector(ABC):
    def __init__(self, directory: str):
        self.directory = directory

    @abstractmethod
    def detect(self) -> Tuple[bool, Any]:
        """
        Выполняет анализ и возвращает:
          - bool: факт обнаружения
          - Any: дополнительные данные (список совпадений или метаданные)
        """
        pass

    @abstractmethod
    def confidence(self) -> float:
        """
        Оценка уверенности в результатах анализа (0.0–1.0).
        """
        pass
