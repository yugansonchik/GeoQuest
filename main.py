import os
import serpapi
import json
import random


def run_cities():
    # Open JSON with the list of big Russian cities
    with open('big_russian_cities.json') as json_file:
        cities = json.load(json_file)["cities"]

    # Choose one random city
    city = random.choice(cities)

    # Setting parameters for the id-search
    params_for_id = {
        "engine": "google_maps",
        "q": city["name"],
        "hl": "ru",
        "type": "search",
        "api_key": "d1dd78ada0cdcb4fe90e1b06efdea2928bf3f768b93e321653169bc7f452a301"
    }

    # Getting results of the id-search
    results = client.search(params_for_id)["place_results"]["data_id"]

    # Setting parameters for the photo-search
    params_for_photo = {
        "engine": "google_maps_photos",
        "data_id": results,
        "api_key": "d1dd78ada0cdcb4fe90e1b06efdea2928bf3f768b93e321653169bc7f452a301"
    }

    # Getting 30 first results of the photo-search
    all_photos = client.search(params_for_photo)["photos"][:30]

    # Making the list of five photos
    random_five = random.sample(all_photos, 5)
    links = [random_five[0]["image"], random_five[1]["image"], random_five[2]["image"], random_five[3]["image"],
             random_five[4]["image"]]

    print(links)
    print(city["name"])

    user_answer = input()

    if user_answer == city["name"]:
        print("Great job!", city["name"], "is a correct answer!")
    else:
        print("You are incorrect( The correct answer is", city["name"])


def run_countries():
    available_counties = ['Австралия', 'Австрия', 'Азербайджан', 'Албания', 'Алжир', 'Аргентина', 'Армения',
                          'Афганистан', 'Бангладеш', 'Барбадос', 'Бахрейн', 'Беларусь', 'Бельгия', 'Бермудские Острова',
                          'Болгария','Боливия', 'Босния и Герцеговина', 'Бразилия', 'Ватикан', 'Великобритания',
                          'Венгрия', 'Венесуэла', 'Вьетнам', 'Гаити', 'Германия', 'Гонконг', 'Гренландия', 'Греция',
                          'Грузия', 'Дания', 'Доминиканская Республика', 'Египет', 'Израиль', 'Индия', 'Индонезия',
                          'Иордания', 'Ирак', 'Иран', 'Ирландия', 'Исландия', 'Испания', 'Италия', 'Кабо-Верде',
                          'Казахстан', 'Камбоджа', 'Камерун', 'Канада', 'Катар', 'Кения', 'Кипр', 'Китай', 'Колумбия',
                          'Коста-Рика', 'Куба', 'Кувейт', 'Кыргызстан', 'Лаос', 'Латвия', 'Либерия', 'Ливан', 'Ливия',
                          'Литва', 'Лихтенштейн', 'Люксембург', 'Маврикий', 'Мадагаскар', 'Малайзия', 'Мальдивы',
                          'Мальта', 'Мексика', 'Мозамбик', 'Молдова', 'Монако', 'Монголия', 'Морокко', 'Намибия',
                          'Непал,' 'Нигер', 'Нигерия', 'Нидерланды', 'Новая Зеландия', 'Норвегия',
                          'Объединенные Арабские Эмираты', 'Оман', 'Пакистан', 'Панама', 'Папуа — Новая Гвинея',
                          'Парагвай', 'Перу', 'Польша', 'Португалия', 'Пуэрто-Рико', 'Республика Конго', 'Россия',
                          'Румыния', 'Сальвадор', 'Самоа', 'Сан-Марино',  'Саудовская Аравия', 'Свазиленд',
                          'Северная Корея', 'Сейшельские острова', 'Сербия', 'Сингапур', 'Сирия', 'Словакия',
                          'Словения', 'Соединенные Штаты Америки', 'Сомали', 'Таджикистан', 'Таиланд', 'Тайвань',
                          'Танзания', 'Тунис', 'Туркменистан', 'Турция', 'Узбекистан', 'Украина', 'Уругвай',
                          'Фарерские Острова', 'Фиджи', 'Филиппины', 'Финляндия', 'Франция', 'Хорватия', 'Черногория',
                          'Чехия', 'Чили', 'Швейцария', 'Швеция', 'Шри-Ланка', 'Эквадор', 'Эритрея', 'Эстония',
                          'Эфиопия', 'Южная Корея', 'Южно-Африканская Республика', 'Ямайка', 'Япония']

    # Choose one random country
    country = random.choice(available_counties)

    # Setting parameters for the id-search
    params_for_id = {
        "engine": "google_maps",
        "q": country,
        "hl": "ru",
        "type": "search",
        "api_key": "d1dd78ada0cdcb4fe90e1b06efdea2928bf3f768b93e321653169bc7f452a301"
    }

    # Getting results of the id-search
    results = client.search(params_for_id)["place_results"]["data_id"]

    # Setting parameters for the photo-search
    params_for_photo = {
        "engine": "google_maps_photos",
        "data_id": results,
        "api_key": "d1dd78ada0cdcb4fe90e1b06efdea2928bf3f768b93e321653169bc7f452a301"
    }

    # Getting 30 first results of the photo-search
    all_photos = client.search(params_for_photo)["photos"][:30]

    # Making the list of five photos
    random_five = random.sample(all_photos, 5)
    links = [random_five[0]["image"], random_five[1]["image"], random_five[2]["image"], random_five[3]["image"],
             random_five[4]["image"]]

    print(links)
    print(country)

    user_answer = input()

    if user_answer == country:
        print("Great job!", country, "is a correct answer!")
    else:
        print("You are incorrect( The correct answer is", country)


# Authorization to SerpApi
client = serpapi.Client(api_key=os.getenv("d1dd78ada0cdcb4fe90e1b06efdea2928bf3f768b93e321653169bc7f452a301"))

# Reading the mode
print("Choose mode (Countries/Cities):")
mode = input()

if mode == "Cities":
    run_cities()
else:
    run_countries()