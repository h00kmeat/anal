from typing import Any, Dict
import json

class ReportGenerator:
    def __init__(self, output_format: str = 'console'):
        self.output_format = output_format

    def generate(self, results: Dict[str, Any]) -> None:
        if self.output_format == 'console':
            self._to_console(results)
        elif self.output_format == 'json':
            print(json.dumps(results, indent=2, ensure_ascii=False))
        elif self.output_format == 'html':
            self._to_html(results)

    def _to_console(self, results: Dict[str, Any]) -> None:
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

        # --- API Эндпоинты ---
        print("=== API ЭНДПОИНТЫ ===")
        eps = results.get('endpoints', [])
        if not eps:
            print("Не найдено API эндпоинтов")
            return

        # Группируем по файлам
        by_file = defaultdict(list)
        for ep in eps:
            by_file[ep['file']].append(ep)

        # Выводим по файлам, предварительно сортируя по line
        for file_path, endpoints in sorted(by_file.items()):
            print(f"\n{file_path}:")
            # Сортируем список по номеру строки
            for ep in sorted(endpoints, key=lambda x: x.get('line', 0)):
                line      = ep.get('line', '?')
                method    = ep.get('method', '').upper()
                framework = ep.get('framework', '')
                endpoint  = ep.get('endpoint', '')
                print(f"  · {line:>4}  {method:<6} {framework:<10} {endpoint}")

        # --- AJAX ---
        print("=== AJAX-ЗАПРОСЫ ===")
        if not results['ajax']:
            print("Нет AJAX-запросов")
        else:
            for ajax in results['ajax']:
                print(f"  {ajax['file']}:{ajax['line']} -> {ajax['call']}")

        # 7) HTTP МЕТОДЫ
        http_methods = results.get('http_methods', [])
        print("\n=== HTTP МЕТОДЫ ===")
        if http_methods:
            # ожидаем список словарей вида {'file':..., 'line':..., 'method':..., 'context':...}
            for m in http_methods:
                print(f"{m['file']:40} · {m['line']:4}  {m['method']:7}  {m.get('context','')}")
        else:
            print("Не найдено HTTP методов")

        # 8) HTTP ЗАГОЛОВКИ
        headers = results.get('headers', [])
        print("\n=== HTTP ЗАГОЛОВКИ ===")
        if headers:
            # ожидаем список словарей вида {'file':..., 'line':..., 'header':..., 'value':...}
            for h in headers:
                hdr = h['headers']
                val = h.get('value')
                if val:
                    print(f"{h['file']:40} · {h['line']:4}  {hdr}: {val}")
                else:
                    print(f"{h['file']:40} · {h['line']:4}  {hdr}")
        else:
            print("Не найдено HTTP заголовков")

    def _to_html(self, results: Dict[str, Any]) -> None:
        # Генерация HTML файла и сохранение на диск
        pass
