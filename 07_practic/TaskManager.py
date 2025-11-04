from abc import ABC, abstractmethod
from TodoManager import TodoManager
from Task import TaskStatus


class Command(ABC):
    """
    Абстрактный класс команды для реализации паттерна Command
    """

    @abstractmethod
    def execute(self) -> None:
        """
        Абстрактный метод для выполнения команды
        """
        pass


class AddTaskCommand(Command):
    """
    Команда для добавления новой задачи
    """

    def __init__(self, manager: TodoManager, title: str, description: str):
        """
        Конструктор команды добавления задачи

        Args:
            manager: Менеджер задач
            title: Название задачи
            description: Описание задачи
        """
        self.manager = manager
        self.title = title
        self.description = description

    def execute(self) -> None:
        """
        Выполняет команду добавления задачи
        """
        self.manager.add_task(self.title, self.description)


class UpdateStatusCommand(Command):
    """
    Команда для обновления статуса задачи
    """

    def __init__(self, manager: TodoManager, task_id: int, status: TaskStatus):
        """
        Конструктор команды обновления статуса

        Args:
            manager: Менеджер задач
            task_id: ID задачи
            status: Новый статус задачи
        """
        self.manager = manager
        self.task_id = task_id
        self.status = status

    def execute(self) -> None:
        """
        Выполняет команду обновления статуса задачи
        """
        self.manager.update_task_status(self.task_id, self.status)


class DeleteTaskCommand(Command):
    """
    Команда для удаления задачи
    """

    def __init__(self, manager: TodoManager, task_id: int):
        """
        Конструктор команды удаления задачи

        Args:
            manager: Менеджер задач
            task_id: ID задачи для удаления
        """
        self.manager = manager
        self.task_id = task_id

    def execute(self) -> None:
        """
        Выполняет команду удаления задачи
        """
        self.manager.delete_task(self.task_id)
