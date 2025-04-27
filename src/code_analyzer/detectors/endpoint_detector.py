import os
from typing import List, Dict, Any
from .base import Detector
from ..patterns import ENDPOINT_PATTERNS, AJAX_PATTERN_EXT, ENDPOINT_IGNORE_FILE_PATTERNS

class EndpointDetector(Detector):
    """
    Детектор API-эндпоинтов и AJAX-вызовов.
    Пропускает тестовые и mock-файлы и убирает дубли.
    """
    # — Убрали IGNORE_GLOBS, теперь используем ENDPOINT_IGNORE_FILE_PATTERNS
    
    def __init__(self, directory: str, main_lang: str):
        super().__init__(directory)
        self.main_lang = main_lang

    def detect(self) -> Dict[str, List[Dict[str, Any]]]:
        endpoints = set()
        ajax_calls = set()

        for root, _, files in os.walk(self.directory):
            for fname in files:
                fpath = os.path.join(root, fname)
                
                # — Используем ENDPOINT_IGNORE_FILE_PATTERNS (regex) вместо старых glob-паттернов
                if any(regex.search(fpath) for regex in ENDPOINT_IGNORE_FILE_PATTERNS):
                    continue

                # только поддерживаемые расширения
                if not fname.lower().endswith((
                    '.js', '.ts', '.jsx', '.tsx',
                    '.py', '.rb', '.php', '.go'
                )):
                    continue

                try:
                    text = open(fpath, 'r', encoding='utf-8', errors='ignore').read()
                except Exception:
                    continue

                # 1) Ищем API-эндпоинты по языковым паттернам
                patterns = ENDPOINT_PATTERNS.get(self.main_lang, [])
                for regex, framework in patterns:
                    for match in regex.finditer(text):
                        endpoint = match.group(1)  # <-- group(1) holds the path
                        line_no = text[:match.start()].count('\n') + 1
                        endpoints.add((
                            framework,
                            endpoint,
                            os.path.relpath(fpath, start=self.directory),
                            line_no
                        ))

                # 2) Ищем AJAX-запросы
                for match in AJAX_PATTERN_EXT.finditer(text):
                    url = next(g for g in match.groups() if g)
                    line_no = text[:match.start()].count('\n') + 1
                    ajax_calls.add((
                        os.path.relpath(fpath, start=self.directory),
                        line_no,
                        url
                    ))

        endpoint_list = [
            {'framework': fw, 'endpoint': ep, 'file': fp, 'line': ln}
            for fw, ep, fp, ln in sorted(endpoints)
        ]
        ajax_list = [
            {'file': fp, 'line': ln, 'call': url}
            for fp, ln, url in sorted(ajax_calls)
        ]

        return {'endpoints': endpoint_list, 'ajax': ajax_list}

    def confidence(self) -> float:
        """
        Оценка уверенности детектора. 
        Если найдены хоть что-то (эндпоинты или AJAX) — максимально уверены.
        """
        results = self.detect()
        found_any = bool(results['endpoints'] or results['ajax'])
        return 1.0 if found_any else 0.0