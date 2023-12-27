import telebot

bot = telebot.TeleBot("6304128627:AAGMwnjsGSmeJUneaaTOOs3b8Uy6AALKbrk")

test_questions = [
    {
        "question": "Какой оператор используется для выполнения целочисленного деления в Python?",
        "options": [
            "/",
            "%",
            "//",
            "*"
        ],
        "correct_option": 2
    },
    {
        "question": "Как объявить переменную в Python?",
        "options": [
            "var x = 5",
            "x = 5",
            "int x = 5",
            "variable x = 5"
        ],
        "correct_option": 1
    },
    {
        "question": "Что делает функция 'print()' в Python?",
        "options": [
            "Выполняет математические вычисления",
            "Удаляет переменные",
            "Выводит текст на экран",
            "Создает цикл"
        ],
        "correct_option": 2
    },
    {
        "question": "Какая функция используется для чтения пользовательского ввода в Python?",
        "options": [
            "input()",
            "read()",
            "get()",
            "scan()"
        ],
        "correct_option": 0
    },
    {
        "question": "Какая конструкция используется для проверки условий в Python?",
        "options": [
            "for-loop",
            "if-else",
            "while-loop",
            "switch-case"
        ],
        "correct_option": 1
    },
    {
        "question": "Что такое список (list) в Python?",
        "options": [
            "Упорядоченная коллекция элементов",
            "Неизменяемая последовательность символов",
            "Ключевое слово для определения функций",
            "Тип данных для хранения целых чисел"
        ],
        "correct_option": 0
    },
    {
        "question": "Как добавить элемент в список в Python?",
        "options": [
            "add()",
            "append()",
            "insert()",
            "extend()"
        ],
        "correct_option": 1
    },
    {
        "question": "Какая функция используется для определения длины списка в Python?",
        "options": [
            "length()",
            "size()",
            "count()",
            "len()"
        ],
        "correct_option": 3
    },
    {
        "question": "Какой символ используется для создания комментария в Python?",
        "options": [
            "//",
            "#",
            "/* */",
            "--"
        ],
        "correct_option": 1
    },
    {
        "question": "Какая функция используется для преобразования строки в целое число в Python?",
        "options": [
            "int()",
            "float()",
            "str()",
            "bool()"
        ],
        "correct_option": 0
    }
]

user_scores = {}

current_question_index = 0


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот-тест по Python. Давай начнем!")

    user_scores[message.chat.id] = 0
    global current_question_index
    current_question_index = 0
    send_question(message.chat.id)


def send_question(chat_id):
    global current_question_index
    if current_question_index < len(test_questions):
        question = test_questions[current_question_index]
        question_text = question["question"]
        options = question["options"]

        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        for option in options:
            markup.add(telebot.types.KeyboardButton(option))

        bot.send_message(chat_id, question_text, reply_markup=markup)
        current_question_index += 1
    else:
        score = user_scores[chat_id]
        bot.send_message(chat_id, f"Тест окончен! Ваш результат: {score}/{len(test_questions)}")
        user_scores.pop(chat_id)


@bot.message_handler(func=lambda message: True)
def check_answer(message):
    chat_id = message.chat.id
    user_answer = message.text

    if chat_id in user_scores:
        question = test_questions[current_question_index - 1]
        correct_option = question["correct_option"]
        options = question["options"]

        if user_answer in options and options.index(user_answer) == correct_option:
            user_scores[chat_id] += 1
            bot.send_message(chat_id, "Правильно!")
        else:
            bot.send_message(chat_id, "Неправильно.")

        send_question(chat_id)
    else:
        bot.send_message(chat_id, "Тест еще не начался. Введите команду /start, чтобы начать игру.")


bot.polling()
