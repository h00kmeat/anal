import os
import re
from typing import List, Tuple
from .base import Detector

class CodeDetector(Detector):
    """
    Детектор, ищущий совпадения по регулярному выражению в исходном коде.
    """

    def __init__(self, directory: str, pattern: str):
        super().__init__(directory)
        # Компилируем паттерн один раз
        self.pattern = re.compile(pattern, re.IGNORECASE)
        # Список найденных совпадений: (путь, номер_строки, текст_совпадения)
        self._matches: List[Tuple[str, int, str]] = []

    def detect(self) -> List[Tuple[str, int, str]]:
        """
        Сканирует все файлы проекта с исходным кодом и ищет совпадения по regex.
        Возвращает список кортежей (путь_к_файлу, номер_строки, совпавший_текст).
        """
        self._matches.clear()
        for root, _, files in os.walk(self.directory):
            for fname in files:
                if not fname.endswith(('.py', '.js', '.ts', '.java', '.php', '.cs')):
                    continue
                path = os.path.join(root, fname)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        for lineno, line in enumerate(f, start=1):
                            m = self.pattern.search(line)
                            if m:
                                self._matches.append((path, lineno, m.group(0)))
                except Exception:
                    # Пропускаем файлы, которые не удалось прочитать
                    continue
        return self._matches

    def confidence(self) -> float:
        """
        Оценка уверенности: доля файлов, в которых найдены совпадения,
        от общего числа проверенных файлов с исходным кодом.
        """
        total = 0
        seen_files = set(path for path, _, _ in self._matches)
        for root, _, files in os.walk(self.directory):
            for fname in files:
                if fname.endswith(('.py', '.js', '.ts', '.java', '.php', '.cs')):
                    total += 1
        return (len(seen_files) / total) if total > 0 else 0.0