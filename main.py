import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import datetime


token = ("vk1.a.9cE6LmX1JejFa-VfM2ERJ7Ef0mRRQiolfvQK-2rz3u_97tCu1Fx7Iymn5BrxULVyhuRE_gLnh-Yf1VUUeuUnmGV9c6PrfR7seIP"
         "Jn6Yk6rcd4cDGX_SobuaJmYdiUnJfZ0"
         "cehyJFUAtsv0XQh4A3xxoxDBkjHbekoHvN6RVoqXxg6lLWAeZQyF4IQZ51LB-whulcpnDcX8ews7UWT9pQqQ")

session = vk_api.VkApi(token=token)

session._auth_token()

now = datetime.datetime.now()
timeA = now.hour


def send_message(user_id, message=None, keyboard=None):
    post = {
        'user_id': user_id,
        'message': message,
        'random_id': 0,
    }

    if keyboard:
        post['keyboard'] = keyboard.get_keyboard()

    else:
        post = post

    session.method('messages.send', post)


def construct(user_id, name, money, power, farmling_number, farmling_power, greevils_greed, cost_of_farmling,
              cost_up_farmling_power, cost_greevils_greed):
    p = dict()
    p["name"] = name
    p["money"] = money
    p["messegNumb"] = 0
    p["power"] = power
    p["farmling_number"] = farmling_number
    p["farmling_power"] = farmling_power
    p["greevils_greed"] = greevils_greed
    p["cost_of_farmling"] = cost_of_farmling
    p["cost_up_farmling_power"] = cost_up_farmling_power
    p["cost_greevils_greed"] = cost_greevils_greed

    data[str(user_id)] = p

    return "normal"


def savebd():
    with open("data.txt", "w") as file:
        for i in data:  # проходимся по data и получаем id в нем
            p = str(i) + " " + str(data[i]["name"]) + " " + str(data[i]["money"]) + " " + str(
                data[i]["messegNumb"]) + " " + str(int(FARMLING_POWER) * int(NUMBER_OF_FARMLING) +
                                                   int(GREEVILS_GREED)) + " " + str(NUMBER_OF_FARMLING) + " " + str(
                FARMLING_POWER) + " " + str(
                GREEVILS_GREED) + " " + str(COST_OF_FARMLING) + " " + str(COST_UP_FARMLING_POWER) + " " + str(
                COST_GREEVILS_GREED)

            file.write(p + '\n')  # записываем в data.txt построчно пользователей


def loadbd():
    file = open("data.txt", "r")
    datas = file.read()
    datas = datas.splitlines()
    file.close()
    data = dict()

    for i in datas:
        i = i.split()

        if len(i) > 6:  # проверка на полноту данных
            data[str(i[0])] = {}
            data[str(i[0])]["name"] = i[1]
            data[str(i[0])]["money"] = i[2]
            data[str(i[0])]["messegNumb"] = i[3]
            data[str(i[0])]["power"] = int(i[5]) * int(i[6]) + int(i[7])
            data[str(i[0])]["farmling_number"] = i[5]
            data[str(i[0])]["farmling_power"] = i[6]
            data[str(i[0])]["greevils_greed"] = i[7]
            data[str(i[0])]["cost_of_farmling"] = i[8]
            data[str(i[0])]["cost_up_farmling_power"] = i[9]
            data[str(i[0])]["cost_greevils_greed"] = i[10]

    return data


FARMLING = [0, 1]
GREEVILS_GREED = 0

# магазин
COST_OF_FARMLING = 0  # стоимость покупки одного фармлинга
COST_UP_FARMLING_POWER = 50  # стоимость прокачки всех фармлингов
COST_GREEVILS_GREED = 5  # стоимость пасивки алхимика

POWER = 0  # сила фармлингов
NUMBER_OF_FARMLING = FARMLING[0]  # количество фармлингов
FARMLING_POWER = FARMLING[1]

data = loadbd()  # загружаем в переменную data информацию из функции loadbd и файла data.txt

# игровые переменные
for i in data:
    FARMLING = [data[i]["farmling_number"], data[i]["farmling_power"]]  # статы фармлингов [количество, сила]
    GREEVILS_GREED = data[i]["greevils_greed"]
    FARMLING_POWER = FARMLING[1]
    NUMBER_OF_FARMLING = FARMLING[0]  # количество фармлингов
    COST_OF_FARMLING = data[i]['cost_of_farmling']  # стоимость покупки одного фармлинга
    COST_UP_FARMLING_POWER = data[i]['cost_up_farmling_power']  # стоимость прокачки всех фармлингов
    COST_GREEVILS_GREED = data[i]['cost_greevils_greed']
    POWER = FARMLING[1]  # сила фармлингов


while True:
    # добавления монет каждый час пользователя
    # часть игровой механики бота
    now = datetime.datetime.now()
    timeB = now.second

    if timeA < timeB:
        timeA = timeB

        for i in data:
            data[i]["money"] = int(data[i]["money"]) + int(FARMLING_POWER) * int(NUMBER_OF_FARMLING) + int(
                GREEVILS_GREED)

    elif (timeA > timeB) and (timeB == 0):
        timeA = 0
        for i in data:
            data[i]["money"] = int(data[i]["money"]) + int(data[i]["power"])

    messages = session.method("messages.getConversations",
                              {"offset": 0, "count": 20, "filter": "unanswered"})
    if messages["count"] >= 1:
        id = messages["items"][0]["last_message"]["from_id"]
        body = messages["items"][0]["last_message"]["text"]

        # авторизация пользователя в боте
        n = 0
        for i in data:
            if str(id) == i:
                n = 1
        if n == 0:
            construct(id, id, 0, POWER, NUMBER_OF_FARMLING, POWER,
                      GREEVILS_GREED, COST_OF_FARMLING, COST_UP_FARMLING_POWER, COST_GREEVILS_GREED)

        # начало работы
        if body.lower() == "начать":

            keyboard = VkKeyboard()
            keyboard.add_button('Наёмнички', VkKeyboardColor.SECONDARY)
            keyboard.add_button('Профиль', VkKeyboardColor.SECONDARY)
            keyboard.add_button('Команды', VkKeyboardColor.SECONDARY)

            send_message(id, """Поздравляем!
                      Вы стали участником игры Dota Miner
                      Для того что бы получить свой первый заработок,
                      нужно купить своего первого помощника в разделе
                      'Наёмнички'""",
                         keyboard)

        # раздел с помощниками
        elif body.lower() == 'наёмнички':

            keyboard = VkKeyboard()
            keyboard.add_button('Купить фармлинга', VkKeyboardColor.POSITIVE)
            keyboard.add_button('Прокачать фармлинга', VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('Прокачать пасивку алхимика', VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('Профиль', VkKeyboardColor.SECONDARY)
            keyboard.add_button('Вернуться на фонтан', VkKeyboardColor.SECONDARY)

            send_message(id, f"""Прайс:
            Купит одного Фармлинга: {COST_OF_FARMLING}$
            - даёт одного фармлига

            Улучшение работы всех Фармлингов: {COST_UP_FARMLING_POWER}$
            - даёт +1 к силе каждого фармлинга

            Улучшить пасивку алхимика: {COST_GREEVILS_GREED}$
            - даёт +1 к каждой совершённой работе""",
                         keyboard)

        # покупка фармлинга
        elif body.lower() == 'купить фармлинга':

            for i in data:
                if int(data[i]["money"]) >= int(COST_OF_FARMLING):
                    data[i]["money"] = int(data[i]["money"]) - int(COST_OF_FARMLING)
                    COST_OF_FARMLING = round(int(COST_OF_FARMLING) + int(COST_OF_FARMLING) * 0.1 + 50)
                    NUMBER_OF_FARMLING = int(NUMBER_OF_FARMLING) + 1
                    send_message(id, f"""К вам присоединился один Фармлинг
                                                Общее количество фармлингов {NUMBER_OF_FARMLING}
                                                Остаток средств: {data[i]['money']}""")

                else:

                    send_message(id, f"""У вас недостаточно средств :(
                                        {int(data[i]["money"])}$
                                        
                                        Прайс:
                                        Купит одного Фармлинга: {COST_OF_FARMLING}$
                                        - даёт одного фармлига

                                        Улучшение работы всех Фармлингов: {COST_UP_FARMLING_POWER}$
                                        - даёт +1 к силе каждого фармлинга

                                        Улучшить пасивку алхимика: {COST_GREEVILS_GREED}$
                                        - даёт +1 к каждой совершённой работе""")

        # прокачка фармилинга
        elif body.lower() == 'прокачать фармлинга':

            for i in data:
                if data[i]['money'] >= int(COST_UP_FARMLING_POWER):
                    data[i]["money"] = int(data[i]["money"]) - int(COST_UP_FARMLING_POWER)
                    COST_UP_FARMLING_POWER = round(int(COST_UP_FARMLING_POWER) +
                                                   int(COST_UP_FARMLING_POWER) * 0.2 + 100)
                    FARMLING_POWER = int(FARMLING_POWER) + 1
                    send_message(id, f"""Все фармлинги стали сильнее!
                                                Сила одного фармлинга {FARMLING_POWER}
                                                Остаток средств: {data[i]['money']}""")

                else:
                    send_message(id, f"""У вас недостаточно средств :(
                                                            {int(data[i]["money"])}$
                                                            
                                                            Прайс:
                                                            Купит одного Фармлинга: {COST_OF_FARMLING}$
                                                            - даёт одного фармлига

                                                            Улучшение работы всех Фармлингов: {COST_UP_FARMLING_POWER}$
                                                            - даёт +1 к силе каждого фармлинга

                                                            Улучшить пасивку алхимика: {COST_GREEVILS_GREED}$
                                                            - даёт +1 к каждой совершённой работе""")

        # прокачка пасивки алхимика
        elif body.lower() == 'прокачать пасивку алхимика':

            for i in data:
                if data[i]['money'] >= int(COST_GREEVILS_GREED):
                    data[i]["money"] = int(data[i]["money"]) - int(COST_GREEVILS_GREED)
                    COST_OF_FARMLING = round(int(COST_GREEVILS_GREED) + int(COST_GREEVILS_GREED) * 0.02)
                    GREEVILS_GREED = int(GREEVILS_GREED) + 1
                    send_message(id, f"""За каждый случай зарабатка,
                                                вы стали получать ещё больше денег
                                                Стаки пасивки {GREEVILS_GREED}
                                                Остаток средств: {data[i]['money']}""")

                else:
                    send_message(id, f"""У вас недостаточно средств :(
                                                            {int(data[i]["money"])}$
                                                            
                                                            Прайс:
                                                            Купит одного Фармлинга: {COST_OF_FARMLING}$
                                                            - даёт одного фармлига

                                                            Улучшение работы всех Фармлингов: {COST_UP_FARMLING_POWER}$
                                                            - даёт +1 к силе каждого фармлинга

                                                            Улучшить пасивку алхимика: {COST_GREEVILS_GREED}$
                                                            - даёт +1 к каждой совершённой работе""")

        # домашняя страница
        elif body.lower() == "вернуться на фонтан":

            keyboard = VkKeyboard()
            keyboard.add_button('Наёмнички', VkKeyboardColor.SECONDARY)
            keyboard.add_button('Профиль', VkKeyboardColor.SECONDARY)
            keyboard.add_button('Команды', VkKeyboardColor.SECONDARY)

            send_message(id, 'Вы вернулись на базу', keyboard)

        # список команд
        elif body.lower() == "команды":

            keyboard = VkKeyboard()
            keyboard.add_button('Профиль', VkKeyboardColor.SECONDARY)
            keyboard.add_line()
            keyboard.add_button('Вернуться на фонтан', VkKeyboardColor.SECONDARY)

            send_message(id, """Привет!
                      Доступный список команд:
                      Команды - показывает все доступные команды
                      Наёмнички - раздел для покупки помощников
                      Вернуться на фонтан - возвращает на длмашнюю локацию
                      Профиль - выводит всю информацию о вашем игровом профиле
                      Ник - позволяет поменять ваш никнейм (должен состоять из одного слова)""",
                         keyboard)

        # профиль игрока
        elif body.lower() == "профиль":

            keyboard = VkKeyboard()
            keyboard.add_button('Наёмнички', VkKeyboardColor.SECONDARY)
            keyboard.add_button('Профиль', VkKeyboardColor.SECONDARY)
            keyboard.add_line()
            keyboard.add_button('Вернуться на фонтан', VkKeyboardColor.SECONDARY)
            send_message(id, f"""Имя: {str(data[str(id)]["name"])}
                                Баланс: {str(data[str(id)]["money"])}$
                                {int(FARMLING_POWER) * int(NUMBER_OF_FARMLING) + int(GREEVILS_GREED)} доход/в сек
                                Количество Фармлингов {NUMBER_OF_FARMLING}
                                Сила одного Фармлинга {FARMLING_POWER}
                                Стаков пасвки Алхимика {GREEVILS_GREED}""", keyboard)

        # пашалка
        elif body.lower() == "кто я" or body.lower() == "кто я?":

            keyboard = VkKeyboard()
            keyboard.add_button('Наёмнички', VkKeyboardColor.SECONDARY)
            keyboard.add_button('Профиль', VkKeyboardColor.SECONDARY)
            keyboard.add_button('Команды', VkKeyboardColor.SECONDARY)

            send_message(id, """https://www.youtube.com/watch?v=ROQlc57iWY4""",
                         keyboard)

        # пашалка
        elif body.lower() == "невер гона гив ю ап" or body.lower() == "never gonna give you up":  # пашалка

            keyboard = VkKeyboard()
            keyboard.add_button('Наёмнички', VkKeyboardColor.SECONDARY)
            keyboard.add_button('Профиль', VkKeyboardColor.SECONDARY)
            keyboard.add_line()
            keyboard.add_button('Вернуться на фонтан', VkKeyboardColor.SECONDARY)

            send_message(id, """https://www.youtube.com/watch?v=dQw4w9WgXcQ""",
                         keyboard)

        # изменение никнейма
        else:
            # состовные команды
            bodyone = body.split()
            if (bodyone[0].lower() == "ник") and (len(bodyone) > 1):
                bodyone = body.lower().split()
                data[str(id)]["name"] = bodyone[1]  # меняем имя пользователя в боте на новое

                send_message(id, f'Ник изменён на {str(bodyone[1])}')

            else:
                keyboard = VkKeyboard()
                keyboard.add_button('Наёмнички', VkKeyboardColor.SECONDARY)
                keyboard.add_button('Профиль', VkKeyboardColor.SECONDARY)
                keyboard.add_button('Команды', VkKeyboardColor.SECONDARY)

                # если бот не нашел команду которую он может выполнить
                send_message(id, """Нет такой команды""",
                             keyboard)

        savebd()
