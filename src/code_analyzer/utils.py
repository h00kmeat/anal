import os
from typing import Iterator, Tuple

# Вспомогательные функции для работы с файлами и путями

def format_path(path: str, base_dir: str = None) -> str:
    """
    Форматирует путь:
      - Если указан base_dir, возвращает относительный путь с ведущим '/',
      - Иначе — полный путь,
      Всегда нормализует слэши в Unix-стиль.
    """
    if base_dir:
        try:
            rel = os.path.relpath(path, start=base_dir)
            return "/" + rel.replace("\\\\", "/")
        except ValueError:
            return path.replace("\\\\", "/")
    return path.replace("\\\\", "/")


def read_files(directory: str) -> Iterator[Tuple[str, str]]:
    """Генератор обхода всех файлов: возвращает кортеж (путь, содержимое)"""
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                yield path, content
            except Exception:
                continue