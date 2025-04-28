from typing import Dict, Set
import os
from ..patterns import TECHNOLOGY_DETECTORS, TECHNOLOGIES_BY_LANG, JS_TECH_DETECTION 
from ..detectors.base import Detector
from ..detectors import FileDetector, CodeDetector

class StackAnalyzer:
    def __init__(self, directory: str, main_lang: str):
        self.directory = directory
        self.main_lang = main_lang
        self.detectors = [] 

    def prepare_detectors(self):
        """
        Сначала добавляем детекторы из JS_TECH_DETECTION для JS/TS-проектов,
        затем — общие технологии из TECHNOLOGY_DETECTORS.
        """
        # ——— Новый блок для JS/TS ———
        pkg_json = os.path.join(self.directory, "package.json")
        if os.path.exists(pkg_json):
            for tech, info in JS_TECH_DETECTION.items():
                # категория: frontend / backend / database
                cat = 'frontend' if info['type']=='frontend' else 'backend' if info['type']=='backend' else 'database'
                # конфиг для FileDetector — паттерн найдёт package.json
                cfg = {
                    'type':   'file',
                    'pattern': r'"(?:' + '|'.join(info['packages']) + r')"'
                }
                self.detectors.append((cat, tech, [FileDetector(self.directory, [cfg])]))

        # ——— Существующий код для остальных технологий ———
        lang_techs = TECHNOLOGIES_BY_LANG.get(self.main_lang, {})
        for category_key, tech_list in lang_techs.items():
            for tech in tech_list:
                configs = TECHNOLOGY_DETECTORS.get(tech, [])
                if not configs:
                    continue
                instances = []
                for cfg in configs:
                    t = cfg.get('type')
                    if t in ('file', 'dir'):
                        instances.append(FileDetector(self.directory, [cfg]))
                    elif t == 'code':
                        instances.append(CodeDetector(self.directory, cfg['pattern']))
                if instances:
                    self.detectors.append((category_key, tech, instances))

    def analyze_stack(self) -> Dict[str, Set[str]]:
        """
        Запускает детекторы и возвращает найденные технологии по категориям.
        """
        result = {
            'backend': set(),
            'frontend': set(),
            'database': set(),
            'build_tools': set(),
            'testing': set(),
            'devops': set()
        }
        category_map = {
            'frameworks': 'backend',
            'frontend': 'frontend',
            'databases': 'database',
            'build_tools': 'build_tools',
            'test_frameworks': 'testing',
            'devops': 'devops'
        }
        for category_key, tech, instances in self.detectors:
            mapped = category_map.get(category_key, category_key)
            for det in instances:
                try:
                    detected = det.detect()
                except Exception:
                    continue
                found = bool(detected[0]) if isinstance(detected, tuple) else bool(detected)
                if found:
                    result[mapped].add(tech)
                    break
        return result
