from typing import List, Optional
from Task import Task, TaskStatus
from Storage import JSONStorage
from Logger import Observer


class TodoManager:
    """
    Класс для управления задачами

    """
    _instance = None
    _initialized = False

    def __new__(cls):
        """
        Создание Singleton-экземпляра
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Инициализация первоначальных данных
        """
        if not TodoManager._initialized:
            self.tasks: List[Task] = []
            self.storage = JSONStorage()
            self.observers: List[Observer] = []
            self.filename = "tasks.json"
            self.next_id = 1
            TodoManager._initialized = True

    def add_observer(self, observer: Observer) -> None:
        """
        Добавляет observer в список observers

        Args:
            observer: Наблюдатель для добавления
        """
        self.observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        """
        Удаляет выбранный observer

        Args:
            observer: Наблюдатель для удаления
        """
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, event: str, task: Optional[Task] = None) -> None:
        """
        Оповещает все обсерверы о событии

        Args:
            event: Событие для оповещения
            task: Задача (опционально)
        """
        for observer in self.observers:
            observer.update(event, task)

    def add_task(self, title: str, description: str) -> Task:
        """
        Создает новую задачу и добавляет её в список

        Args:
            title: Название задачи
            description: Описание задачи

        Returns:
            Task: Созданная задача
        """
        task = Task(title, description)
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        self.notify_observers("Task created", task)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Находит задачу по ID

        Args:
            task_id: ID задачи для поиска

        Returns:
            Optional[Task]: Найденная задача или None
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task_status(self, task_id: int, status: TaskStatus) -> bool:
        """
        Обновляет статус задачи

        Args:
            task_id: ID задачи
            status: Новый статус

        Returns:
            bool: True если успешно, False если задача не найдена
        """
        task = self.get_task(task_id)
        if task:
            old_status = task.status
            task.update_status(status)
            self.notify_observers(f"Task status updated from {old_status.value} to {status.value}", task)
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """
        Удаляет задачу по ID

        Args:
            task_id: ID задачи для удаления

        Returns:
            bool: True если успешно, False если задача не найдена
        """
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.notify_observers("Task deleted", task)
            return True
        return False

    def get_all_tasks(self) -> List[Task]:
        """
        Возвращает весь список задач

        Returns:
            List[Task]: Список всех задач
        """
        return self.tasks

    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """
        Возвращает задачи с определенным статусом

        Args:
            status: Статус для фильтрации

        Returns:
            List[Task]: Список задач с указанным статусом
        """
        return [task for task in self.tasks if task.status == status]

    def save_to_file(self) -> bool:
        """
        Сохраняет задачи в файл

        Returns:
            bool: True если успешно, False при ошибке
        """
        success = self.storage.save(self.tasks, self.filename)
        if success:
            self.notify_observers("Tasks saved to file")
        else:
            self.notify_observers("Error saving tasks to file")
        return success

    def load_from_file(self) -> bool:
        """
        Загружает задачи из файла

        Returns:
            bool: True если успешно, False при ошибке
        """
        loaded_tasks = self.storage.load(self.filename)
        if loaded_tasks:
            self.tasks = loaded_tasks
            if self.tasks:
                self.next_id = max(task.id for task in self.tasks) + 1
            self.notify_observers("Tasks loaded from file")
            return True
        return False
