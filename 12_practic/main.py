import tkinter as tk
from tkinter import ttk
from db import init_db, save_rate, get_saved_rate
from api import fetch_rates


class CurrencyConverterApp(tk.Tk):
    """
    Главное приложение - калькулятор кредита с конвертацией валют.

    Предоставляет функционал для:
    - расчета кредитных платежей по аннуитетной формуле
    - конвертации результатов в различные валюты
    - кэширования курсов валют в локальной БД
    - логирования действий пользователя
    """

    def __init__(self):
        """
        Инициализация приложения.

        Создает главное окно, инициализирует переменные,
        создает виджеты и загружает начальные данные.
        """
        super().__init__()

        # Настройка главного окна
        self.title("Калькулятор кредита с конвертацией")
        self.geometry("500x600")

        # Инициализация переменных
        self.loan_var = tk.DoubleVar(value=0.0)
        self.loan_time_var = tk.IntVar(value=0)
        self.annual_interest_var = tk.DoubleVar(value=0.0)
        self.base_var = tk.StringVar(value="RUB")
        self.target_var = tk.StringVar(value="USD")

        # Создание виджетов
        self.create_widgets()

        # Инициализация БД
        self.init_db()

        # Загрузка валют
        self.load_currencies()

    def init_db(self):
        """Инициализирует базу данных при запуске приложения."""
        try:
            init_db()
            self.log("База данных инициализирована")
        except Exception as e:
            self.log(f"Ошибка инициализации БД: {e}")

    def create_widgets(self):
        """
        Создает и размещает все UI-компоненты приложения.

        Включает:
        - поля ввода параметров кредита
        - область отображения результатов
        - элементы для конвертации валют
        - панель логов действий
        """
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        ttk.Label(main_frame, text="Калькулятор кредита", font=("Arial", 14, "bold")).pack(pady=(0, 10))

        # Параметры кредита
        params_frame = ttk.LabelFrame(main_frame, text="Параметры кредита", padding="10")
        params_frame.pack(fill=tk.X, pady=5)

        ttk.Label(params_frame, text="Сумма кредита:").grid(row=0, column=0, sticky="w")
        ttk.Entry(params_frame, textvariable=self.loan_var, width=15).grid(row=0, column=1, padx=5)
        ttk.Label(params_frame, text="RUB").grid(row=0, column=2, sticky="w")

        ttk.Label(params_frame, text="Срок кредита:").grid(row=1, column=0, sticky="w")
        ttk.Entry(params_frame, textvariable=self.loan_time_var, width=15).grid(row=1, column=1, padx=5)
        ttk.Label(params_frame, text="мес.").grid(row=1, column=2, sticky="w")

        ttk.Label(params_frame, text="Процентная ставка:").grid(row=2, column=0, sticky="w")
        ttk.Entry(params_frame, textvariable=self.annual_interest_var, width=15).grid(row=2, column=1, padx=5)
        ttk.Label(params_frame, text="%").grid(row=2, column=2, sticky="w")

        ttk.Button(params_frame, text="Рассчитать", command=self.calculate_loan).grid(row=3, column=0, columnspan=3,
                                                                                      pady=10)

        # Результаты кредита
        results_frame = ttk.LabelFrame(main_frame, text="Результаты расчёта", padding="10")
        results_frame.pack(fill=tk.X, pady=5)

        self.monthly_label = ttk.Label(results_frame, text="Ежемесячный платеж: 0 RUB")
        self.monthly_label.pack(anchor="w")

        self.loan_sum_label = ttk.Label(results_frame, text="Сумма всех платежей: 0 RUB")
        self.loan_sum_label.pack(anchor="w")

        self.interest_label = ttk.Label(results_frame, text="Начисленные проценты: 0 RUB")
        self.interest_label.pack(anchor="w")

        # Конвертация валют
        convert_frame = ttk.LabelFrame(main_frame, text="Конвертация валют", padding="10")
        convert_frame.pack(fill=tk.X, pady=5)

        ttk.Label(convert_frame, text="Базовая валюта:").grid(row=0, column=0, sticky="w")
        ttk.Label(convert_frame, textvariable=self.base_var).grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(convert_frame, text="Целевая валюта:").grid(row=1, column=0, sticky="w")
        self.target_combobox = ttk.Combobox(convert_frame, textvariable=self.target_var, width=10)
        self.target_combobox.grid(row=1, column=1, padx=5)

        ttk.Button(convert_frame, text="Конвертировать", command=self.convert).grid(row=2, column=0, pady=5)
        ttk.Button(convert_frame, text="Обновить курсы", command=self.update_db).grid(row=2, column=1, pady=5)

        self.result_label = ttk.Label(convert_frame, text="", foreground="blue")
        self.result_label.grid(row=3, column=0, columnspan=2)

        # Лог
        log_frame = ttk.LabelFrame(main_frame, text="Лог действий", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill=tk.Y)

    def log(self, message: str):
        """
        Добавляет сообщение в лог приложения.

        Args:
            message: Текст сообщения для логирования
        """
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.update_idletasks()

    def is_loan_invalid(self, value: float, field_name: str) -> bool:
        """
        Проверяет корректность значения кредитного параметра.

        Args:
            value: Проверяемое значение
            field_name: Название поля для сообщения об ошибке

        Returns:
            bool: True если значение некорректно, False если корректно
        """
        if value < 0:
            self.log(f"Ошибка: Значение '{field_name}' не может быть отрицательным!")
            return True

        if value == 0:
            self.log(f"Ошибка: Значение '{field_name}' должно быть больше нуля!")
            return True

        return False

    def calculate_loan(self):
        """
        Рассчитывает параметры кредита по аннуитетной формуле.

        Вычисляет:
        - ежемесячный платеж
        - общую сумму выплат
        - сумму начисленных процентов

        Результаты отображаются в интерфейсе и логируются.
        """
        try:
            loan_amount = self.loan_var.get()
            loan_months = self.loan_time_var.get()
            annual_rate = self.annual_interest_var.get()

            if (self.is_loan_invalid(loan_amount, "Сумма кредита") or
                    self.is_loan_invalid(loan_months, "Срок кредита") or
                    self.is_loan_invalid(annual_rate, "Процентная ставка")):
                return

            monthly_rate = annual_rate / 100 / 12
            if monthly_rate == 0:
                monthly_payment = loan_amount / loan_months
            else:
                monthly_payment = (loan_amount * monthly_rate *
                                   (1 + monthly_rate) ** loan_months) / \
                                  ((1 + monthly_rate) ** loan_months - 1)

            total_payment = monthly_payment * loan_months
            total_interest = total_payment - loan_amount

            self.monthly_label.config(text=f"Ежемесячный платеж: {monthly_payment:,.2f} RUB")
            self.loan_sum_label.config(text=f"Сумма всех платежей: {total_payment:,.2f} RUB")
            self.interest_label.config(text=f"Начисленные проценты: {total_interest:,.2f} RUB")

            self.log("Расчёт кредита выполнен успешно")

        except Exception as e:
            self.log(f"Ошибка при расчёте кредита: {e}")

    def convert(self):
        """
        Конвертирует сумму ежемесячного платежа в выбранную валюту.

        Этапы конвертации:
        1. Проверка выполнения расчета кредита
        2. Получение актуального курса валюты из БД
        3. Выполнение конвертации RUB → целевая валюта
        4. Обновление интерфейса с результатом
        """
        target_currency = self.target_var.get().upper()  # Выносим для использования в except

        try:
            # Проверяем, выполнен ли расчёт кредита
            monthly_text = self.monthly_label.cget("text")
            try:
                monthly_value_str = monthly_text.split(": ")[1].replace(" RUB", "").replace(",", "")
                monthly_value = float(monthly_value_str)
            except (IndexError, ValueError):
                self.log("Ошибка: Сначала выполните расчёт кредита")
                return

            if monthly_value <= 0:
                self.log("Ошибка: Сначала выполните расчёт кредита")
                return

            # Получаем курс из базы данных
            rate = get_saved_rate(target_currency)

            # Конвертация RUB → выбранная валюта
            converted_amount = monthly_value / rate

            # Обновляем интерфейс
            self.result_label.config(
                text=f"Ежемесячный платеж: {converted_amount:,.2f} {target_currency}"
            )
            self.log(f"Конвертация: {monthly_value:,.2f} RUB → {converted_amount:,.2f} {target_currency}")

        except ValueError as e:
            # Обрабатываем только ошибку отсутствия курса из get_saved_rate()
            self.log(f"Ошибка: {e}")
        except Exception as e:
            # Остальные непредвиденные ошибки
            self.log(f"Ошибка при конвертации {target_currency}: {e}")

    def update_db(self):
        """
        Обновляет курсы валют в базе данных.

        Выполняет:
        - запрос актуальных курсов через API ЦБ РФ
        - сохранение курсов в локальную БД
        - обновление списка доступных валют в интерфейсе
        """
        try:
            self.log("Обновление курсов валют...")
            data = fetch_rates()
            valute = data.get('Valute', {})

            for code, info in valute.items():
                rate = info.get('Value')
                if rate:
                    save_rate(code, rate)

            self.load_currencies(data)
            self.log(f"Курсы валют успешно обновлены ({len(valute)} валют)")

        except Exception as e:
            self.log(f"Ошибка при обновлении курсов: {e}")

    def load_currencies(self, data=None):
        """
        Загружает список доступных валют в выпадающий список.

        Args:
            data: Готовые данные о валютах (опционально)
                  Если не переданы - выполняется API-запрос
        """
        try:
            if not data:
                data = fetch_rates()
            currencies = list(data.get('Valute', {}).keys())
            self.target_combobox['values'] = currencies
            self.log(f"Загружено {len(currencies)} валют")
        except Exception as e:
            default_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CNY']
            self.target_combobox['values'] = default_currencies
            self.log(f"Использован резервный список валют. Ошибка: {e}")


def main():
    """
    Точка входа в приложение.

    Создает и запускает главное окно приложения.
    """
    app = CurrencyConverterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
