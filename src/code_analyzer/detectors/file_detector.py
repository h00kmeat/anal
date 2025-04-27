import os
import glob
from typing import List, Dict, Any, Tuple
from .base import Detector

class FileDetector(Detector):
    """Детектор наличия файлов/директорий и поиска контента внутри файлов."""
    def __init__(self, directory: str, configs: List[Dict[str, Any]]):
        super().__init__(directory)
        self.configs = configs
        self._matches: List[Tuple[str, Any]] = []

    def detect(self) -> Tuple[bool, List[Tuple[str, Any]]]:
        """
        Ищет файлы и директории по списку конфигураций.
        Каждый cfg должен содержать:
          - 'type': 'file' или 'dir'
          - 'path': шаблон пути
          - опционально 'content' для файлов
        Возвращает (found, matches), где matches — список (путь, content_or_None).
        """
        self._matches.clear()
    
        for cfg in self.configs:
            pattern       = os.path.join(self.directory, cfg.get('path', ''))
            expected_type = cfg.get('type', 'file')
    
            for path in glob.glob(pattern, recursive=True):
                # Директория?
                if expected_type == 'dir':
                    if os.path.isdir(path):
                        self._matches.append((path, None))
                    continue
                
                # Файл?
                if not os.path.isfile(path):
                    continue
                
                # Поиск по содержимому (если нужно)
                if 'content' in cfg:
                    try:
                        text = open(path, 'r', encoding='utf-8', errors='ignore').read()
                    except Exception:
                        continue
                    if cfg['content'] in text:
                        self._matches.append((path, cfg['content']))
                else:
                    self._matches.append((path, None))
    
        return (bool(self._matches), self._matches)

    def confidence(self) -> float:
        """
        Оценка уверенности: отношение числа найденных совпадений к общему числу конфигураций.
        """
        total = len(self.configs)
        return (len(self._matches) / total) if total > 0 else 0.0