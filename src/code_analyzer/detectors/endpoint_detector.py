# src/code_analyzer/detectors/endpoint_detector.py
import os
import re
from typing import List, Dict, Any
from .base import Detector
from ..patterns import (
    ENDPOINT_PATTERNS,
    AJAX_PATTERN_EXT,
    ENDPOINT_IGNORE_FILE_PATTERNS
)

# Привязка расширений к языкам
EXTENSION_LANG_MAP = {
    '.js':   'JavaScript',
    '.jsx':  'JavaScript',
    '.ts':   'TypeScript',
    '.tsx':  'TypeScript',
    '.py':   'Python',
    '.rb':   'Ruby',
    '.php':  'PHP',
    '.go':   'Go',
    '.java': 'Java',
    '.kt':   'Kotlin',
}

class EndpointDetector(Detector):
    def __init__(self, directory: str, langs: List[str]):
        super().__init__(directory)
        self.langs = langs

    def detect(self) -> Dict[str, List[Dict[str, Any]]]:
        raw: List[tuple] = []     # [(file, line, framework, method, route), ...]
        ajax_calls = set()

        for root, _, files in os.walk(self.directory):
            for fname in files:
                fpath = os.path.join(root, fname)

                # 1) Пропускаем игнор-файлы
                if any(pat.search(fpath) for pat in ENDPOINT_IGNORE_FILE_PATTERNS):
                    continue

                # 2) Только кодовые расширения
                ext = os.path.splitext(fname)[1].lower()
                if ext not in EXTENSION_LANG_MAP:
                    continue

                # 3) чтение
                try:
                    text = open(fpath, 'r', encoding='utf-8', errors='ignore').read()
                except Exception:
                    continue

                rel = os.path.relpath(fpath, start=self.directory)

                # 4) Определяем язык файла и сразу берём только его паттерны
                lang_for_file = EXTENSION_LANG_MAP[ext]
                if lang_for_file not in self.langs:
                    continue

                for regex, framework in ENDPOINT_PATTERNS.get(lang_for_file, []):
                    for m in regex.finditer(text):
                        # если паттерн захватывает метод (например Express), берём его, иначе "ALL"
                        method = m.group(1).upper() if regex.groups >= 2 else 'ALL'
                        # путь всегда последняя группа
                        route = m.group(regex.groups)
                        line_no = text[:m.start()].count('\n') + 1
                        raw.append((
                            rel,
                            line_no,
                            framework,
                            method,
                            route
                        ))

                # 4) Ищем AJAX-запросы (общие шаблоны)
                for match in AJAX_PATTERN_EXT.finditer(text):
                    # безопасный next — если нет ни одной непустой группы, пропускаем
                    url = next((g for g in match.groups() if g), None)
                    if not url:
                        continue
                    line_no = text[:match.start()].count('\n') + 1
                    ajax_calls.add((
                        rel,
                        line_no,
                        url
                    ))

        # 6) Сортировка и форматирование
        raw.sort(key=lambda x: (x[0], x[1]))
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
        res = self.detect()
        return 1.0 if (res['endpoints'] or res['ajax']) else 0.0
