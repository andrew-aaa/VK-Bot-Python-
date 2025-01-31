from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkApi
import pyowm
import random
import requests
import datetime
from googletrans import Translator
import asyncio

token = 'TOKEN'

# Функция определения погоды по городу
def get_weather(city):
    owm = pyowm.OWM('TOKEN')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    w = observation.weather
    temp = w.temperature('celsius')['temp']
    status = w.detailed_status
    return f'Сейчас в {city} температура {temp:.1f}°C, {status}.'

# Функции для перевода
async def translate_rus_to_eng(text):
    translator = Translator()
    translation = await translator.translate(text, dest='en')
    return translation.text

# Функция музыкальной рекомендации (не работает)
def get_recommended_music(user_id):
    token_music = 'TOKEN'
    session = VkApi(token=token_music)
    api = session.get_api()
    try:
        recommendations = api.audio.getRecommendations(user_id=user_id, count=10)['items']
        
        tracks = []
        for recommendation in recommendations:
            tracks.append({
                'artist': recommendation['artist'],
                'title': recommendation['title']
            })
        
        return tracks
    except Exception as e:
        print(f"Ошибка при получении рекомендаций: {e}")
        return []

# Функция рецептов
def find_recipe(ingredients):
    recipes = {
        'картофель, мясо': 'Жаркое',
        'яйца, мука, молоко': 'Омлет',
        'помидоры, огурцы, лук': 'Салат'
    }
    recipe = recipes.get(', '.join(sorted(ingredients)), None)
    if recipe:
        return f'Можно приготовить {recipe}.'
    else:
        return 'Не нашел подходящего рецепта.'

# Функция напоминание
def water_reminder():
    return 'Не забывайте пить воду! Это важно для вашего здоровья.'

# Функция гороскоп
def get_horoscope(sign):
    today = datetime.date.today()
    horoscopes = {
        'Овен': f'Сегодня, {today.day} {today.strftime("%B")}, Овны могут ожидать приятного сюрприза.',
        'Телец': f'Сегодня, {today.day} {today.strftime("%B")}, Тельцам стоит уделить внимание своему здоровью.',
        'Близнецы': f'Сегодня, {today.day} {today.strftime("%B")}, Близнецам предстоит интересный день, полный новых знакомств.',
        'Рак': f'Сегодня, {today.day} {today.strftime("%B")}, Раки найдут вдохновение в самых неожиданных местах.',
        'Лев': f'Сегодня, {today.day} {today.strftime("%B")}, Львы почувствуют прилив энергии и смогут достичь многого.',
        'Дева': f'Сегодня, {today.day} {today.strftime("%B")}, Девам следует сосредоточиться на своих целях и планах.',
        'Весы': f'Сегодня, {today.day} {today.strftime("%B")}, Весам стоит искать гармонию и равновесие в своей жизни.',
        'Скорпион': f'Сегодня, {today.day} {today.strftime("%B")}, Скорпионы откроют для себя новые возможности.',
        'Стрелец': f'Сегодня, {today.day} {today.strftime("%B")}, Стрельцы будут наслаждаться общением с друзьями и близкими.',
        'Козерог': f'Сегодня, {today.day} {today.strftime("%B")}, Козерогам предстоит продуктивный день, полный успехов.',
        'Водолей': f'Сегодня, {today.day} {today.strftime("%B")}, Водолеи ощутят потребность в творчестве и самовыражении.',
        'Рыбы': f'Сегодня, {today.day} {today.strftime("%B")}, Рыбы должны прислушиваться к своим интуиции и чувствам.'
    }
    return horoscopes.get(sign.capitalize(), f"К сожалению, я не смог найти гороскоп для знака {sign}. Попробуйте еще раз.")

# Функция игра
def play_game(event, longpoll, vk, user_id):
    questions = [
        {'question': 'Какой город является столицей Франции?', 'answer': 'Париж'},
        {'question': 'Как называется самая большая пустыня в мире?', 'answer': 'Антарктическая'}
    ]
    question = random.choice(questions)
    vk.messages.send(user_id=user_id, random_id=0, message=f"Вопрос: {question['question']}")
    
    for new_event in longpoll.listen():
        if new_event.type == VkEventType.MESSAGE_NEW and new_event.to_me and new_event.user_id == event.user_id:
            answer = new_event.text.lower()
            break

    if answer == question['answer'].lower():
        return "Правильно!"
    else:
        return f"Неправильно. Правильный ответ: {question['answer']}"

# Функция задач
def solve_math_problem(event, longpoll, vk, user_id):
    problems = [
        {'problem': 'Сколько будет 2 + 2?', 'solution': '4'},
        {'problem': 'Какое число больше: 5 или 3?', 'solution': '5'}
    ]
    problem = random.choice(problems)
    vk.messages.send(user_id=user_id, random_id=0, message=f"Задача: {problem['problem']}")
    for new_event in longpoll.listen():
        if new_event.type == VkEventType.MESSAGE_NEW and new_event.to_me and new_event.user_id == event.user_id:
            solution = new_event.text.lower()
            break
    
    if solution == problem['solution'].lower():
        return "Верно!"
    else:
        return f"Неверно. Правильное решение: {problem['solution']}"

# Функцция рекомендации Путешествия
def travel_suggestion(query):
    base_url = "https://ru.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": query,
        "format": "json",
        "namespace": "0",
        "limit": "10"
    }

    response = requests.get(base_url, params=params).json()
    results = response[1]

    if len(results) > 0:
        random_result = random.choice(results)
        return f"Я рекомендую посетить {random_result}. Это одно из популярных туристических направлений."
    else:
        return "К сожалению, я не смог найти подходящие рекомендации для этого запроса. Попробуйте уточнить запрос."

# Функция психологического теста
def psychology_test(event, vk, longpoll):
    tests = [
        {
            'question': 'Часто ли вы испытываете чувство тревоги?',
            'answers': ['Да', 'Иногда', 'Редко'],
            'advice': {
                'Да': 'Возможно, стоит попробовать методы релаксации, такие как глубокое дыхание или медитация.',
                'Иногда': 'Важно находить баланс между работой и отдыхом. Постарайтесь выделять время для расслабления.',
                'Редко': 'Это хорошо! Продолжайте заботиться о своем психическом здоровье.'
            }
        },
        {
            'question': 'Легко ли вам справляться со стрессовыми ситуациями?',
            'answers': ['Да', 'Иногда', 'Трудно'],
            'advice': {
                'Да': 'Отлично! Ваши навыки управления стрессом помогают сохранять спокойствие.',
                'Иногда': 'Попробуйте разработать стратегии для управления стрессом, такие как физические упражнения или ведение дневника.',
                'Трудно': 'Может быть полезно обратиться к специалисту, чтобы научиться эффективным техникам борьбы со стрессом.'
            }
        }
    ]

    def ask_question(question_data, user_id, longpoll):
        vk.messages.send(user_id=user_id, random_id=0, message=f"Вопрос: {question_data['question']}")
        for i, answer in enumerate(question_data['answers']):
            vk.messages.send(user_id=user_id, random_id=0, message=f"{i+1}. {answer}")
        
        for new_event in longpoll.listen():
            if new_event.type == VkEventType.MESSAGE_NEW and new_event.to_me and new_event.user_id == user_id:
                try:
                    choice = int(new_event.text)
                    if 1 <= choice <= len(question_data['answers']):
                        advice = question_data['advice'][question_data['answers'][choice-1]]
                        vk.messages.send(user_id=user_id, random_id=0, message=f"Совет: {advice}")
                        break
                    else:
                        vk.messages.send(user_id=user_id, random_id=0, message=f"Пожалуйста, введите номер от 1 до {len(question_data['answers'])}.")
                except ValueError:
                    vk.messages.send(user_id=user_id, random_id=0, message="Пожалуйста, введите номер.")

    for test in tests:
        ask_question(test, event.user_id, longpoll)

async def main():
    session = VkApi(token=token)
    vk = session.get_api()
    longpoll = VkLongPoll(session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower().split()
            user_id = event.user_id

            if msg[0] == 'привет':
                vk.messages.send(user_id=user_id, random_id=0, message='Привет!\nВведите слово для одного из действийя:\nпогода\nперевод\nрецепт\nвода\nгороскоп\nигра\nзадача\nпутшествие\nтест')

            elif msg[0] == 'погода':
                city = ' '.join(msg[1:])
                weather = get_weather(city)
                vk.messages.send(user_id=user_id, random_id=0, message=weather)

            elif msg[0] == 'перевод':
                word_to_translate = ' '.join(msg[1:])
                translated_word = await translate_rus_to_eng(word_to_translate)
                vk.messages.send(user_id=event.user_id, random_id=0,
                                 message=f'Перевод слова "{word_to_translate}" на английский: {translated_word}')

            elif msg[0] == 'музыка':
                recommended_tracks = get_recommended_music(user_id)
                
                response_message = "Вот несколько рекомендаций:\n\n"
                for track in recommended_tracks:
                    artist = track['artist']
                    title = track['title']
                    url = f'https://vk.com/audio?q={artist}%20{title}'
                    response_message += f"{artist} – {title}\n{url}\n\n"

                vk.messages.send(user_id=event.user_id, random_id=0, message=response_message)

            elif msg[0] == 'рецепт':
                ingredients = msg[1:]
                recipe = find_recipe(ingredients)
                vk.messages.send(user_id=user_id, random_id=0, message=recipe)

            elif msg[0] == 'вода':
                reminder = water_reminder()
                vk.messages.send(user_id=user_id, random_id=0, message=reminder)

            elif msg[0] == 'гороскоп':
                sign = ' '.join(msg[1:])
                horoscope = get_horoscope(sign)
                vk.messages.send(user_id=user_id, random_id=0, message=horoscope)

            elif msg[0] == 'игра':
                result = play_game(event, longpoll, vk, user_id)
                vk.messages.send(user_id=event.user_id, random_id=0, message=result)

            elif msg[0] == 'задача':
                result = solve_math_problem(event, longpoll, vk, user_id)
                vk.messages.send(user_id=event.user_id, random_id=0, message=result)

            elif msg[0] == 'путешествие':
                query = ' '.join(msg[1:])
                suggestion = travel_suggestion(query)
                vk.messages.send(user_id=user_id, random_id=0, message=suggestion)

            elif msg[0] == 'тест':
                psychology_test(event, vk, longpoll)

            else:
                err_msg = 'Введите слово для одного из действийя:\nпогода\nперевод\nрецепт\nвода\nгороскоп\nигра\nзадача\nпутшествие\nтест'
                vk.messages.send(user_id=user_id, random_id=0, message=err_msg)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
