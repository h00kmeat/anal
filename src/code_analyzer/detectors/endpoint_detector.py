import os
import fnmatch
from typing import Dict, Any, List
from .base import Detector
from ..patterns import ENDPOINT_PATTERNS, AJAX_PATTERN_EXT

class EndpointDetector(Detector):
    """
    Детектор API-эндпоинтов и AJAX-вызовов.
    Пропускает тестовые и mock-файлы и убирает дубли.
    """
    # файлы и папки, которые никогда не сканируем
    IGNORE_GLOBS = [
        '*.test.*', '*.spec.*', '*__tests__/*',
        '*mock*', '*.d.ts', '*.min.js'
    ]

    def detect(self) -> Dict[str, List[Dict[str, Any]]]:
        endpoints = set()
        ajax_calls = set()

        for root, _, files in os.walk(self.directory):
            for fname in files:
                fpath = os.path.join(root, fname)
                # 1) пропускаем игнор-глоблы
                if any(fnmatch.fnmatch(fpath, pat) for pat in self.IGNORE_GLOBS):
                    continue
                # 2) оставляем только нужные расширения
                if not any(fname.endswith(ext) for ext in (
                    '.js', '.ts', '.jsx', '.tsx',
                    '.py', '.rb', '.php', '.go'
                )):
                    continue

                try:
                    text = open(fpath, 'r', encoding='utf-8', errors='ignore').read()
                except Exception:
                    continue

                # 3) Ищем API-эндпоинты по паттернам для языка
                patterns = ENDPOINT_PATTERNS.get(self.main_lang, [])
                for regex, framework in patterns:
                    for match in regex.finditer(text):
                        # теперь захватываем первую группу
                        path = match.group(1)
                        line_no = text[:match.start()].count('\n') + 1
                        endpoints.add((
                            framework,
                            path,
                            os.path.relpath(fpath, start=self.directory),
                            line_no
                        ))

                # 4) Ищем AJAX-вызовы
                for match in AJAX_PATTERN_EXT.finditer(text):
                    url = next(g for g in match.groups() if g)
                    line_no = text[:match.start()].count('\n') + 1
                    ajax_calls.add((
                        os.path.relpath(fpath, start=self.directory),
                        line_no,
                        url
                    ))

        # Преобразуем в список словарей
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