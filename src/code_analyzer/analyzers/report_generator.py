from typing import Any, Dict
import json

class ReportGenerator:
    def __init__(self, output_format: str = 'console'):
        self.output_format = output_format

    def generate(self, results: Dict[str, Any]) -> None:
        """
        Формирует отчёт по результатам анализа.
        Поддерживаемые форматы: 'console', 'json', 'html'.
        """
        if self.output_format == 'console':
            self._to_console(results)
        elif self.output_format == 'json':
            print(json.dumps(results, indent=2, ensure_ascii=False))
        elif self.output_format == 'html':
            self._to_html(results)

    def _to_console(self, results: Dict[str, Any]) -> None:
        """Красивый табличный вывод в консоль"""
        from collections import defaultdict
        from ..utils import format_path

        # Язык и распределение
        langs = results.get('languages', {})
        print("=== РАСПРЕДЕЛЕНИЕ ЯЗЫКОВ ===")
        for lang, perc in langs.items():
            print(f"- {lang}: {perc:.2f}%")

        # Строки кода
        sloc = results.get('sloc', {})
        by_lang = sloc.get('by_lang', {})
        total = sloc.get('total', 0)
        print(f"=== SLOC: всего {total} ===")
        for lang, count in by_lang.items():
            print(f"- {lang}: {count} строк")

        # Технологический стек
        stack = results.get('stack', {}) or {}
        print("=== ТЕХНОЛОГИЧЕСКИЙ СТЕК ===")
        for category, techs in stack.items():
            if techs:
                title = category.capitalize()
                print(f"{title}:")
                for tech in techs:
                    print(f"  - {tech}")

        # Зависимости
        deps = results.get('dependencies', {})
        if deps:
            print("=== ЗАВИСИМОСТИ ===")
            for cat, items in deps.items():
                print(f"{cat.capitalize()}: {', '.join(sorted(items))}")

        # Секреты
        secrets = results.get('secrets', [])
        if secrets:
            print("=== ПОТЕНЦИАЛЬНЫЕ СЕКРЕТЫ ===")
            for path, items in secrets:
                print(format_path(path))
                for item in items:
                    print(f"  - {item}")

         # === API ЭНДПОИНТЫ ===
        print("=== API ЭНДПОИНТЫ ===")
        endpoints = results.get('endpoints', [])
        if endpoints:
            for ep in endpoints:
                # Changed: вместо ep['pattern_type'] используем ep['framework']
                print(f"  [Line {ep['line']}] {ep['framework']} -> {ep['endpoint']}")
        else:
            print("Не найдено API эндпоинтов")

        # === AJAX-ЗАПРОСЫ ===
        print("\n=== AJAX-ЗАПРОСЫ ===")
        ajax = results.get('ajax', [])
        if ajax:
            for call in ajax:
                print(f"  {call['file']}:{call['line']} -> {call['call']}")
        else:
            print("Не найдено AJAX-вызовов")

    def _to_html(self, results: Dict[str, Any]) -> None:
        # Генерация HTML файла и сохранение на диск
        pass
