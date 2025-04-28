import argparse
from .analyzers.language_analyzer    import LanguageAnalyzer
from .analyzers.stack_analyzer       import StackAnalyzer
from .analyzers.dependency_analyzer  import DependencyAnalyzer
from .analyzers.secret_analyzer       import SecretAnalyzer
from .analyzers.report_generator      import ReportGenerator
from .detectors.endpoint_detector     import EndpointDetector
from .detectors.config_detector       import ConfigDetector
from .patterns                        import CONFIG_PATTERNS, ENDPOINT_PATTERNS

def main():
    parser = argparse.ArgumentParser(description="Анализатор безопасности исходного кода")
    parser.add_argument('path', help='Путь к корню проекта')
    parser.add_argument(
        '--format',
        choices=['console', 'json', 'html'],
        default='console',
        help='Формат вывода отчёта'
    )
    args = parser.parse_args()

    # 1) Языки и SLOC
    lang_analyzer = LanguageAnalyzer(args.path)
    distro, = lang_analyzer.detect_languages(),  # распределение языков
    sloc_by_lang, total_sloc = lang_analyzer.count_sloc()
    main_lang = max(distro, key=distro.get) if distro else None

    # 2) Первичный стек по структурам и коду
    stack_analyzer = StackAnalyzer(args.path, main_lang or "")
    stack_analyzer.prepare_detectors()
    tech_stack = stack_analyzer.analyze_stack()

    # 3) Зависимости (из package.json, pom.xml и т.д.)
    dep_analyzer = DependencyAnalyzer(args.path, main_lang)
    deps = dep_analyzer.analyze()

    # 4) Общие секреты
    secret_analyzer = SecretAnalyzer(args.path)
    secrets = secret_analyzer.find_secrets()

    # 5) Эндпоинты и AJAX
    active_langs = [lang for lang in distro.keys() if lang in ENDPOINT_PATTERNS]
    ep_detector = EndpointDetector(args.path, active_langs)
    ep_res      = ep_detector.detect()
    endpoints   = ep_res.get('endpoints', [])
    ajax_calls  = ep_res.get('ajax', [])

    # 6) Конфиги и секреты в них
    config_detector = ConfigDetector(args.path, CONFIG_PATTERNS)
    configs         = config_detector.detect()
    config_secrets  = config_detector.secrets

    # 7) Сливаем зависимостями и конфига в единый tech_stack
    for cat, items in deps.items():
        if items:
            tech_stack.setdefault(cat, set()).update(items)

    # сопоставление технологий из config_patterns к категориям
    for tech in configs:
        if tech in {"MySQL", "PostgreSQL", "Redis"}:
            tech_stack.setdefault("database", set()).add(tech)
        else:
            tech_stack.setdefault("backend", set()).add(tech)

    # 8) Собираем окончательные результаты
    results = {
        "languages":      distro,
        "sloc":           {"by_lang": sloc_by_lang, "total": total_sloc},
        "stack":          tech_stack,
        "dependencies":   deps,
        "secrets":        secrets,
        "endpoints":      endpoints,
        "ajax":           ajax_calls,
        "configs":        configs,
        "config_secrets": config_secrets,
    }

    # 9) Генерация отчёта
    report = ReportGenerator(args.format)
    report.generate(results)


if __name__ == "__main__":
    main()