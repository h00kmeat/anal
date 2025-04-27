import os
import fnmatch
from typing import List, Dict, Any
from .base import Detector
from ..patterns import ENDPOINT_PATTERNS, AJAX_PATTERN_EXT, ENDPOINT_IGNORE_FILE_PATTERNS

# Карта расширений файлов → язык
EXTENSION_LANG_MAP = {
    '.js':   'JavaScript',
    '.jsx':  'JavaScript',
    '.ts':   'TypeScript',
    '.tsx':  'TypeScript',
    '.py':   'Python',
    '.rb':   'Ruby',
    '.php':  'PHP',
    '.go':   'Go',
}

class EndpointDetector(Detector):
    """
    Детектор API-эндпоинтов и AJAX-вызовов.
    Пропускает тестовые и mock-файлы по ENDPOINT_IGNORE_FILE_PATTERNS,
    определяет язык по расширению, убирает дубли и сортирует по файлу и строке.
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
                rel = os.path.relpath(fpath, start=self.directory)

                # 1) Пропускаем всё, что матчится под ignore-паттерны
                if any(p.search(fpath) for p in ENDPOINT_IGNORE_FILE_PATTERNS):
                    continue

                # 2) Интересуют только кодовые файлы с известными расширениями
                ext = os.path.splitext(fname)[1].lower()
                if ext not in EXTENSION_LANG_MAP:
                    continue

                # 3) Читаем содержимое
                try:
                    text = open(fpath, 'r', encoding='utf-8', errors='ignore').read()
                except Exception:
                    continue

                # 4) Определяем язык по расширению и пропускаем, если он не в активных langs
                lang_for_file = EXTENSION_LANG_MAP[ext]
                if lang_for_file not in self.langs:
                    continue

                # 5) Ищем API-эндпоинты по паттернам этого языка
                for regex, framework in ENDPOINT_PATTERNS.get(lang_for_file, []):
                    for m in regex.finditer(text):
                        # если в паттерне есть группа 1 → HTTP-метод, иначе ALL
                        method = m.group(1).upper() if m.lastindex and m.lastindex >= 1 else 'ALL'
                        # группа 2 → путь
                        route = m.group(2)
                        line_no = text[:m.start()].count('\n') + 1
                        raw.append((rel, line_no, framework, method, route))

                # 6) Ищем AJAX-запросы
                for match in AJAX_PATTERN_EXT.finditer(text):
                    url = next(g for g in match.groups() if g)
                    line_no = text[:match.start()].count('\n') + 1
                    ajax_calls.add((rel, line_no, url))

        # 7) Сортируем raw по файлу, затем по номеру строки
        raw.sort(key=lambda x: (x[0], x[1]))

        # 8) Формируем список словарей для вывода
        endpoint_list: List[Dict[str, Any]] = []
        for f, ln, fw, meth, ep in raw:
            endpoint_list.append({
                'file':      f,
                'line':      ln,
                'framework': fw,
                'method':    meth,
                'endpoint':  ep
            })

        # 9) Формируем список AJAX-запросов
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
        return 1.0 if (results['endpoints'] or results['ajax']) else 0.0
