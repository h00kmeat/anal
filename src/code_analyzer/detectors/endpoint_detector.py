import os
from typing import List, Dict, Any
from .base import Detector
from ..patterns import ENDPOINT_PATTERNS, AJAX_PATTERN_EXT, ENDPOINT_IGNORE_FILE_PATTERNS

class EndpointDetector(Detector):
    """
    Детектор API-эндпоинтов и AJAX-вызовов.
    Пропускает тестовые и mock-файлы по ENDPOINT_IGNORE_FILE_PATTERNS
    и убирает дубли.
    """
    def __init__(self, directory: str, langs: List[str]):
        super().__init__(directory)
        self.langs = langs

    def detect(self) -> Dict[str, List[Dict[str, Any]]]:
        raw: List[tuple] = []     # [(file, line, framework, method, route), ...]
        ajax_calls = set()

        for root, _, files in os.walk(self.directory):
            for fname in files:
                fpath = os.path.join(root, fname)

                # 1) Пропускаем всё, что матчится под ignore-паттерны
                if any(pat.search(fpath) for pat in ENDPOINT_IGNORE_FILE_PATTERNS):
                    continue

                # 2) Интересуют только кодовые файлы
                if not fname.endswith(('.js', '.ts', '.jsx', '.tsx', '.py', '.rb', '.php', '.go')):
                    continue

                try:
                    text = open(fpath, 'r', encoding='utf-8', errors='ignore').read()
                except Exception:
                    continue

                rel = os.path.relpath(fpath, start=self.directory)

                # 3) Ищем API-эндпоинты по паттернам всех активных языков
                for lang in self.langs:
                    for regex, framework in ENDPOINT_PATTERNS.get(lang, []):
                        for m in regex.finditer(text):
                            line_no = text[:m.start()].count('\n') + 1
                            # если паттерн захватывает и метод и путь
                            if m.lastindex and m.lastindex >= 2:
                                method = m.group(1).upper()
                                route  = m.group(2)
                            else:
                                method = "ALL"
                                route  = m.group(1)
                            raw.append((rel, line_no, framework, method, route))

                # 4) Ищем AJAX-запросы (общие шаблоны)
                for match in AJAX_PATTERN_EXT.finditer(text):
                    url = next(g for g in match.groups() if g)
                    line_no = text[:match.start()].count('\n') + 1
                    ajax_calls.add((
                        rel,
                        line_no,
                        url
                    ))

        # 5) Сортируем raw по файлу, затем по номеру строки
        raw.sort(key=lambda x: (x[0], x[1]))

        # 6) Формируем список словарей для вывода
        endpoint_list: List[Dict[str, Any]] = []
        for f, ln, fw, meth, ep in raw:
            endpoint_list.append({
                'file':      f,
                'line':      ln,
                'framework': fw,
                'method':    meth,
                'endpoint':  ep
            })

        ajax_list = [
            {'file': fp, 'line': ln, 'call': url}
            for fp, ln, url in sorted(ajax_calls)
        ]

        return {'endpoints': endpoint_list, 'ajax': ajax_list}

    def confidence(self) -> float:
        """
        Оценка уверенности детектора.
        Если найдены хоть что-то — возвращаем максимальную уверенность 1.0.
        """
        results = self.detect()
        found_any = bool(results['endpoints'] or results['ajax'])
        return 1.0 if found_any else 0.0