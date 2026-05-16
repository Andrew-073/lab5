import csv
from datetime import datetime

# ================= Константы новых файлов =================
INPUT_FILE = 'lab4_data.csv'          # исходный файл для ЛР4
OUTPUT_FILE = 'lab4_data_result.csv'  # результат работы ЛР4

# ================= Класс отдельной транзакции =================
class Transaction:
    def __init__(self, number, date_time, amount, description):
        self.__setattr__('number', number)
        self.__setattr__('date_time', date_time)
        self.__setattr__('amount', amount)
        self.__setattr__('description', description)

    def __repr__(self):
        return f"Transaction({self.number}, {self.date_time}, {self.amount}, '{self.description}')"

    # Запись значений только через __setattr__
    def __setattr__(self, name, value):
        if name == 'amount' and value < 0:
            raise ValueError("Сумма не может быть отрицательной")
        super().__setattr__(name, value)

# ================= Наследование =================
class SpecialTransaction(Transaction):
    """Особая транзакция с бонусом"""
    def __init__(self, number, date_time, amount, description, bonus=0):
        super().__init__(number, date_time, amount, description)
        self.__setattr__('bonus', bonus)

    def __repr__(self):
        return f"SpecialTransaction({self.number}, {self.date_time}, {self.amount}, '{self.description}', bonus={self.bonus})"

# ================= Коллекция транзакций =================
class TransactionList:
    def __init__(self):
        self.transactions = []

    def add(self, transaction):
        self.transactions.append(transaction)

    def __iter__(self):
        return iter(self.transactions)

    def __getitem__(self, index):
        return self.transactions[index]

    def __repr__(self):
        return f"TransactionList({self.transactions})"

    # Статический метод для чтения CSV
    @staticmethod
    def load_from_csv(file_path):
        t_list = TransactionList()
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    number = int(row['№'])
                    date_time = datetime.strptime(row['Дата и время'], "%Y-%m-%d %H:%M")
                    amount = float(row['Сумма'])
                    description = row['Описание транзакции']
                    t_list.add(Transaction(number, date_time, amount, description))
        except FileNotFoundError:
            print(f"Файл {file_path} не найден!")
        return t_list

    # Генератор для фильтрации по минимальной сумме
    def filter_by_amount(self, min_amount):
        for t in self.transactions:
            if t.amount >= min_amount:
                yield t

    # Сортировка по сумме
    def sort_by_amount(self):
        self.transactions.sort(key=lambda x: x.amount)

    # Сохранение в новый CSV
    def save_to_new_csv(self, new_file_path=OUTPUT_FILE):
        if not self.transactions:
            print("Нет данных для сохранения!")
            return
        fields = ['№', 'Дата и время', 'Сумма', 'Описание транзакции']
        with open(new_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for t in self.transactions:
                writer.writerow({
                    '№': t.number,
                    'Дата и время': t.date_time.strftime("%Y-%m-%d %H:%M"),
                    'Сумма': t.amount,
                    'Описание транзакции': t.description
                })
        print(f"Данные сохранены в новый файл '{new_file_path}'")

# ================= Главная программа =================
def main():
    # Загружаем транзакции из нового файла ЛР4
    t_list = TransactionList.load_from_csv(INPUT_FILE)
    if not t_list.transactions:
        return

    print("--- Все транзакции ---")
    for t in t_list:
        print(t)

    # Фильтрация с генератором по минимальной сумме
    try:
        min_amount = float(input("\nВведите минимальную сумму для фильтрации: "))
    except ValueError:
        print("Ошибка ввода!")
        return

    filtered = list(t_list.filter_by_amount(min_amount))
    print(f"\n--- Транзакции с суммой >= {min_amount} ---")
    for t in filtered:
        print(t)

    # Сортировка всех транзакций по сумме
    t_list.sort_by_amount()
    print("\n--- Транзакции отсортированные по сумме ---")
    for t in t_list:
        print(t)

    # Доступ по индексу
    print("\nПример доступа по индексу [0]:", t_list[0])

    # Добавляем специальную транзакцию
    special = SpecialTransaction(999, datetime.now(), 5000, "Бонусная транзакция", bonus=50)
    t_list.add(special)
    print("\nПосле добавления SpecialTransaction:")
    print(t_list)

    # Сохраняем результат в новый файл ЛР4
    t_list.save_to_new_csv()

if __name__ == "__main__":
    main()