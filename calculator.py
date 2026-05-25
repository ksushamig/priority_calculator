import re
import sys

# История вычислений
history_log = []


def tokenize_expression(expression: str) -> list:
    """Очищает строку и разбивает её на числа и операторы."""
    # Удаляем любые пробелы
    expression = expression.replace(" ", "")

    if not expression:
        raise ValueError("Выражение не может быть пустым.")

    # Проверка на запрещенные символы
    if re.search(r'[^0-9\+\-\*/\.]', expression):
        raise ValueError("Выражение содержит недопустимые символы. Используйте только цифры и + - * /")

    # Поиск чисел (включая отрицательные/дробные) и операторов
    tokens = re.findall(r'(-?\d+\.?\d*|[\+\-\*/])', expression)

    # Корректировка: разделяем бинарный минус от отрицательного числа
    valid_tokens = []
    for i, token in enumerate(tokens):
        if token.startswith('-') and len(token) > 1 and i > 0 and re.match(r'\d', tokens[i - 1][-1]):
            valid_tokens.append('-')
            valid_tokens.append(token[1:])
        else:
            valid_tokens.append(token)

    return valid_tokens


def calculate_priority_ops(tokens: list) -> list:
    """Выполняет операции высокого приоритета (* и /)."""
    i = 0
    while i < len(tokens):
        if tokens[i] in ('*', '/'):
            if i == 0 or i == len(tokens) - 1:
                raise ValueError("Некорректное расположение операторов умножения/деления.")

            left = float(tokens[i - 1])
            right = float(tokens[i + 1])
            op = tokens[i]

            if op == '*':
                res = left * right
            else:
                if right == 0:
                    raise ZeroDivisionError("Деление на ноль строго запрещено.")
                res = left / right

            # Схлопываем операцию в один результат
            tokens[i - 1: i + 2] = [str(res)]
            continue
        i += 1
    return tokens


def calculate_basic_ops(tokens: list) -> float:
    """Выполняет операции низкого приоритета (+ и -)."""
    if not tokens:
        raise ValueError("Ошибка разбора выражения.")

    # Первое число — стартовая точка
    try:
        result = float(tokens[0])
    except ValueError:
        raise ValueError("Выражение не может начинаться с этого оператора.")

    i = 1
    while i < len(tokens):
        op = tokens[i]

        # Проверка на два оператора подряд, оставшихся после разбора
        if op not in ('+', '-'):
            raise ValueError(f"Ожидался оператор сложения/вычитания, а получен: {op}")

        if i + 1 >= len(tokens):
            raise ValueError("Выражение обрывается на операторе.")

        right = float(tokens[i + 1])

        if op == '+':
            result += right
        elif op == '-':
            result -= right

        i += 2

    return result


def run_calculator(expression: str) -> float:
    """Основной конвейер обработки строки."""
    tokens = tokenize_expression(expression)
    tokens = calculate_priority_ops(tokens)
    result = calculate_basic_ops(tokens)
    return result


def main():
    """Интерактивный консольный интерфейс (Дополнительное решение)."""
    print("=== Умный Консольный Калькулятор ===")
    print("Поддерживает: приоритет строк, отрицательные числа, историю.")
    print("Команды: 'exit' - выход, 'history' - показать историю.")
    print("-" * 40)

    while True:
        try:
            user_input = input("\nВведите выражение > ").strip()

            if user_input.lower() == 'exit':
                print("Программа завершена. До свидания!")
                sys.exit(0)

            if user_input.lower() == 'history':
                print("--- История вычислений ---")
                if not history_log:
                    print("История пока пуста.")
                for record in history_log:
                    print(record)
                continue

            # Вычисление
            res = run_calculator(user_input)

            # Вывод форматированного результата (убираем .0 у целых чисел)
            formatted_res = int(res) if res.is_integer() else res
            output_line = f"{user_input} = {formatted_res}"

            print(f"Результат: {formatted_res}")
            history_log.append(output_line)

        except (ValueError, ZeroDivisionError) as e:
            print(f"⚠️  Ошибка валидации: {e}")
        except KeyboardInterrupt:
            print("\nПрограмма принудительно завершена.")
            sys.exit(0)
        except Exception as e:
            print(f" Непредвиденная ошибка системы: {e}")


if __name__ == "__main__":
    main()
