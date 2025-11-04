from enum import Enum
from datetime import datetime
from typing import Dict, Any


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task:
    def __init__(self, title: str, description: str, status: TaskStatus = TaskStatus.PENDING):
        """
        Конструктор для инициализации первоначальных данных задачи

        Args:
            title: Название задачи
            description: Описание задачи
            status: Статус задачи (по умолчанию PENDING)
        """
        self.id = id(self)
        self.title = title
        self.description = description
        self.status = status
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """
        Форматирует и возвращает атрибуты класса в виде словаря

        Returns:
            Словарь с данными задачи
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Принимает параметр словаря и форматирует данные обратно в Task

        Args:
            data: Словарь с данными задачи

        Returns:
            Экземпляр класса Task
        """
        task = cls(
            title=data['title'],
            description=data['description'],
            status=TaskStatus(data['status'])
        )
        task.id = data['id']
        task.created_at = data['created_at']
        task.updated_at = data['updated_at']
        return task

    def update_status(self, status: TaskStatus) -> None:
        """
        Обновляет статус задачи

        Args:
            status: Новый статус задачи
        """
        self.status = status
        self.updated_at = datetime.now().isoformat()

    def __str__(self) -> str:
        """Строковое представление задачи для удобного вывода"""
        return f"Task(id={self.id}, title='{self.title}', status={self.status.value})"

    def __repr__(self) -> str:
        """Представление объекта для отладки"""
        return f"Task(id={self.id}, title='{self.title}', status={self.status.value}, created_at={self.created_at})"