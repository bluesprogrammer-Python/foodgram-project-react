import csv
from os import listdir
from os.path import exists, isfile, join
from pathlib import Path
from typing import Any, Dict, Tuple, Type

from django.apps import apps
from django.conf import settings
from django.db.models import Model


def get_path(options: Dict[str, Any]) -> str:
    """Получение относительного пути к директории с файлами.
       Преобразование пути в полный.
       Проверка существования дректории.
    Args:
        options (Dict[str, Any]): Аргументы
    Returns:
        str: Полный путь к директории с файлами
    """
    input_path = Path(options['path'])
    path = join(settings.BASE_DIR, input_path)
    print(f'Введена директория: {path}')
    if exists(path):
        print('Директория найдена...')
        return path
    else:
        raise FileNotFoundError('Директория НЕ найдена!')


def check_files(path: str) -> Dict[str, str]:
    """Проверка наличия всех файлов.
       Проверка существования файлов.
    Args:
        path (str): Полный путь к директории
    Returns:
        Dict[str, str]: Словарь проверенных файлов
    """
    files_dict = {
        'ingredients': 'ingredients.csv',
    }
    access_files = {}
    files_list = [f for f in listdir(path) if isfile(join(path, f))]
    for model_name, files in files_dict.items():
        if files in files_list:
            print(f'Для модели {model_name} найден файл {files}')
            access_files[model_name] = files
        else:
            print(f'*Для модели {model_name} файл НЕ найден!')
    if len(files_dict) != len(access_files):
        print(len(access_files))
        raise FileNotFoundError('Найдены не все файлы!')
    return access_files


def get_models_and_files(
        path: str,
        files: Dict[str, str]) -> Dict[str, Tuple[Type[Model], str]]:
    """Создание словаря {Модель: Путь к файлу}.
    Args:
        path (str): Полный путь к директории
        files (Dict[str, str]): Словарь проверенных файлов
    Returns:
        Dict[str, Tuple[Type[Model], str]]: {Имя модели: (её экземпляр,
                                            путь к файлу)}
    """
    models = {**apps.all_models['cook']}
    models_files = {}
    print(models)
    print(files)
    for model_name, file_name in files.items():
        if model_name in models:
            model = models[model_name]
        else:
            raise TypeError('Такой модели не найдено')
        file_path = join(path, file_name)
        models_files[model_name] = model, file_path
    return models_files


def load_data(
        models_files: Dict[str, Tuple[Type[Model], str]]) -> None:
    """Загрузка данных в модели
    Args:
        models_files (Dict[str, Tuple[Type[Model], str]]): {Модель: путь
        к файлу для этой модели}
    """
    # Список для загрузки данных в определенном порядке
    models_names_list = [
        'ingredients',
    ]
    for model_name in models_names_list:
        model, file = models_files[model_name]
        count_obj_before = model.objects.all().count()
        with open(file, encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            print(f'Импорт данных в модель {model.__name__}')
            count_row = 0
            for count_row, row in enumerate(reader, start=2):
                object, created = model.objects.get_or_create(**row)
        count_obj_after = model.objects.all().count()
        print(f'Добавлено {count_obj_after - count_obj_before} из {count_row}')
