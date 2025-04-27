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

                # Пропускаем всё, что матчится под ignore-паттерны
                if any(pat.search(fpath) for pat in ENDPOINT_IGNORE_FILE_PATTERNS):
                    continue

                # Интересуют только кодовые файлы
                if not fname.endswith(('.js', '.ts', '.jsx', '.tsx', '.py', '.rb', '.php', '.go')):
                    continue

                try:
                    text = open(fpath, 'r', encoding='utf-8', errors='ignore').read()
                except Exception:
                    continue

                rel = os.path.relpath(fpath, start=self.directory)

                # 1) Ищем API-эндпоинты по паттернам для текущего языка
                for regex, framework in ENDPOINT_PATTERNS.get(self.main_lang, []):
                    for match in regex.finditer(text):
                        method = match.group(1)       # HTTP-метод (get, post...)
                        path   = match.group(2)       # путь из ковычек
                        line_no = text[:match.start()].count('\n') + 1
                        endpoints.add((
                            framework,
                            method,
                            path,
                            rel,
                            line_no
                        ))

                # 2) Ищем AJAX-запросы
                for match in AJAX_PATTERN_EXT.finditer(text):
                    url = next(g for g in match.groups() if g)
                    line_no = text[:match.start()].count('\n') + 1
                    ajax_calls.add((
                        rel,
                        line_no,
                        url
                    ))

        # Составляем списки словарей (без дублирования)
        endpoint_list = [
            {
                'framework': fw,
                'method':     meth,
                'endpoint':   ep,
                'file':       fp,
                'line':       ln
            }
            for fw, meth, ep, fp, ln in sorted(endpoints)
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