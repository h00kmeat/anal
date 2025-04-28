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
            expected_type = cfg.get('type', 'file')

            # 1) Если cfg содержит re.Pattern — фильтруем по нему
            if isinstance(cfg.get('pattern'), re.Pattern):
                pat: re.Pattern = cfg['pattern']
                for root, _, files in os.walk(self.directory):
                    for fname in files:
                        if pat.search(fname):
                            full = os.path.join(root, fname)
                            if expected_type == 'dir' and os.path.isdir(full):
                                self._matches.append((full, None))
                            elif expected_type == 'file' and os.path.isfile(full):
                                # при необходимости ищем по содержимому
                                if 'content' in cfg:
                                    text = open(full, 'r', encoding='utf-8', errors='ignore').read()
                                    if cfg['content'] in text:
                                        self._matches.append((full, cfg['content']))
                                else:
                                    self._matches.append((full, None))
                continue

            # 2) Иначе — классический glob по cfg['path']
            pattern_str = cfg.get('path', '')
            for full in glob.glob(os.path.join(self.directory, pattern_str), recursive=True):
                if expected_type == 'dir' and os.path.isdir(full):
                    self._matches.append((full, None))
                elif expected_type == 'file' and os.path.isfile(full):
                    if 'content' in cfg:
                        text = open(full, 'r', encoding='utf-8', errors='ignore').read()
                        if cfg['content'] in text:
                            self._matches.append((full, cfg['content']))
                    else:
                        self._matches.append((full, None))
    
        return (bool(self._matches), self._matches)

    def confidence(self) -> float:
        """
        Оценка уверенности: отношение числа найденных совпадений к общему числу конфигураций.
        """
        total = len(self.configs)
        return (len(self._matches) / total) if total > 0 else 0.0