import json
from typing import List
from Task import Task


class JSONStorage:
    """
    Класс для работы с хранилищем задач в формате JSON
    """

    def save(self, tasks: List[Task], filename: str) -> bool:
        """
        Сохраняет список задач в JSON-файл

        Args:
            tasks: Список задач для сохранения
            filename: Имя файла для сохранения

        Returns:
            bool: True если сохранение успешно, False в случае ошибки
        """
        try:
            tasks_data = [task.to_dict() for task in tasks]

            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(tasks_data, file, ensure_ascii=False, indent=4)

            print(f"Задачи успешно сохранены в файл: {filename}")
            return True

        except Exception as e:
            print(f"Ошибка при сохранении задач в файл {filename}: {e}")
            return False

    def load(self, filename: str) -> List[Task]:
        """
        Загружает список задач из JSON-файла

        Args:
            filename: Имя файла для загрузки

        Returns:
            List[Task]: Список загруженных задач
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                tasks_data = json.load(file)

            tasks = [Task.from_dict(task_data) for task_data in tasks_data]

            print(f"Задачи успешно загружены из файла: {filename}")
            return tasks

        except FileNotFoundError:
            print(f"Файл {filename} не найден. Возвращен пустой список.")
            return []
        except json.JSONDecodeError:
            print(f"Ошибка чтения JSON из файла {filename}. Возвращен пустой список.")
            return []
        except Exception as e:
            print(f"Ошибка при загрузке задач из файла {filename}: {e}")
            return []
