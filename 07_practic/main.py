

from TodoManager import TodoManager
from Logger import TaskLogger
from TaskManager import AddTaskCommand, UpdateStatusCommand, DeleteTaskCommand
from Task import TaskStatus


class TodoApp:

    def __init__(self):
        """
        Инициализация первоначальных данных
        """
        self.manager = TodoManager()
        self.logger = TaskLogger()

        self.manager.add_observer(self.logger)
        self.manager.load_from_file()

    def display_menu(self) -> None:
        """
        Выводит меню в консоль
        """
        print("\n== TODO ==")
        print("1. Показать все задачи")
        print("2. Добавить задачу")
        print("3. Изменить статус задачи")
        print("4. Удалить задачу")
        print("5. Показать задачи по статусу")
        print("6. Сохранить в файл")
        print("7. Загрузить из файла")
        print("8. Выход")
        print("====================")

    def display_tasks(self, tasks) -> None:
        """
        Выводит в консоль существующие задачи

        Args:
            tasks: Список задач для отображения
        """
        if not tasks:
            print("Задачи не найдены.")
            return

        print("\n=== ЗАДАЧИ ===")
        for task in tasks:
            print(f"ID: {task.id}")
            print(f"Название: {task.title}")
            print(f"Описание: {task.description}")
            print(f"Статус: {task.status.value}")
            print(f"Создана: {task.created_at}")
            print(f"Обновлена: {task.updated_at}")
            print("-" * 30)

    def run(self) -> None:
        """
        Обрабатывает главный цикл приложения
        """
        print("Добро пожаловать в Todo приложение!")

        while True:
            self.display_menu()
            choice = input("Выберите пункт меню: ").strip()

            if choice == "1":
                tasks = self.manager.get_all_tasks()
                self.display_tasks(tasks)

            elif choice == "2":
                title = input("Введите название задачи: ").strip()

                # Проверка на пустое название
                if not title:
                    print("Ошибка: название задачи не может быть пустым.")
                    continue

                description = input("Введите описание задачи: ").strip()


                command = AddTaskCommand(self.manager, title, description)
                command.execute()
                print("Задача успешно добавлена!")


            elif choice == "3":
                try:
                    task_id = int(input("Введите ID задачи: ").strip())

                    # Проверка на
                    task = self.manager.get_task(task_id)
                    if not task:
                        print(f"Ошибка: задача с ID {task_id} не найдена.")
                    else:
                        print("Доступные статусы:")
                        print("1. pending")
                        print("2. in_progress")
                        print("3. completed")
                        status_choice = input("Выберите статус (1-3): ").strip()

                        status_map = {
                            "1": TaskStatus.PENDING,
                            "2": TaskStatus.IN_PROGRESS,
                            "3": TaskStatus.COMPLETED
                        }

                        if status_choice in status_map:
                            command = UpdateStatusCommand(self.manager, task_id, status_map[status_choice])
                            command.execute()
                            print("Статус задачи обновлен!")
                        else:
                            print("Ошибка: неверный выбор статуса.")

                except ValueError:
                    print("Ошибка: ID задачи должен быть числом.")

            elif choice == "4":
                try:
                    task_id = int(input("Введите ID задачи для удаления: ").strip())

                    # Проверка на существование задачи
                    task = self.manager.get_task(task_id)
                    if not task:
                        print(f"Ошибка: задача с ID {task_id} не найдена.")
                        continue

                    command = DeleteTaskCommand(self.manager, task_id)
                    command.execute()
                    print("Задача удалена!")
                except ValueError:
                    print("Ошибка: ID задачи должен быть числом.")

            elif choice == "5":
                print("Выберите статус для фильтрации:")
                print("1. pending")
                print("2. in_progress")
                print("3. completed")
                status_choice = input("Выберите статус (1-3): ").strip()

                status_map = {
                    "1": TaskStatus.PENDING,
                    "2": TaskStatus.IN_PROGRESS,
                    "3": TaskStatus.COMPLETED
                }

                if status_choice in status_map:
                    tasks = self.manager.get_tasks_by_status(status_map[status_choice])
                    self.display_tasks(tasks)
                else:
                    print("Ошибка: неверный выбор статуса.")

            elif choice == "6":
                if self.manager.save_to_file():
                    print("Задачи успешно сохранены в файл!")
                else:
                    print("Ошибка при сохранении задач.")

            elif choice == "7":
                if self.manager.load_from_file():
                    print("Задачи успешно загружены из файла!")
                else:
                    print("Ошибка при загрузке задач.")

            elif choice == "8":
                print("Спасибо за использование Todo приложения! До свидания!")
                break

            else:
                print("Ошибка: неверный пункт меню. Попробуйте снова.")


if __name__ == "__main__":
    app = TodoApp()
    app.run()
