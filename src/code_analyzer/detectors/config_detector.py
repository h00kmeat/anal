import os
from typing import Dict, List, Tuple
from .base import Detector
from ..patterns import CONFIG_PATTERNS, PASSWORD_PATTERN  

class ConfigDetector(Detector):
    """
    Детектор для анализа конфигурационных файлов и поиска шаблонов технологий и секретов.
    """
    def __init__(self, directory: str, config_patterns: Dict[str, Dict[str, str]] = None):
        super().__init__(directory)
        # если паттерны не передали — берём из patterns.py
        self.config_patterns = config_patterns or CONFIG_PATTERNS  
        self.detected: Dict[str, List[str]] = {}
        self.secrets: List[Tuple[str, List[str]]] = []

    def detect(self) -> Dict[str, List[str]]:
        """
        Ищет технологические шаблоны в конфигурационных файлах.
        Возвращает словарь {tech_name: [списки путей к файлам]}.
        """
        # теперь проходим только по файлам, которые есть в CONFIG_PATTERNS
        for root, _, files in os.walk(self.directory):
            for cfg_file, tech_map in self.config_patterns.items():
                if cfg_file not in files:
                    continue
                path = os.path.join(root, cfg_file)
                try:
                    content = open(path, 'r', encoding='utf-8', errors='ignore').read()
                except Exception:
                    continue

                # Поиск технологий по шаблонам
                for pattern, tech in tech_map.items():
                    if pattern in content:
                        self.detected.setdefault(tech, []).append(path)

                # Поиск секретов
                secrets = PASSWORD_PATTERN.findall(content)
                if secrets:
                    values = [match[1] for match in secrets]
                    self.secrets.append((path, values))
        return self.detected

    def confidence(self) -> float:
        """
        Доля найденных технологических совпадений от общего числа шаблонов.
        """
        total_patterns = sum(len(p) for p in self.config_patterns.values())
        found = sum(len(paths) for paths in self.detected.values())
        return (found / total_patterns) if total_patterns else 0.0