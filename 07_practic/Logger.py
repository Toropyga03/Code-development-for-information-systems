from abc import ABC, abstractmethod
from datetime import datetime
from Task import Task
from typing import Optional


class Observer(ABC):
    """
    Абстрактный класс наблюдателя
    """

    @abstractmethod
    def update(self, event: str, task: Optional[Task] = None) -> None:
        """
        Абстрактный метод для обновления наблюдателя

        Args:
            event: Название события (строка)
            task: Задача (может быть None)
        """
        pass


class TaskLogger(Observer):
    """
    Класс для логирования событий задач
    """

    def update(self, event: str, task: Optional[Task] = None) -> None:
        """
        Выводит в консоль сообщение о событии

        Args:
            event: Название события
            task: Задача (опционально)
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if task:
            print(f"{current_time} {event}: {task}")
        else:
            print(f"{current_time} {event}")