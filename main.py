from jsoner import return_json, save_json_with_ident


import requests
import faker
import time


FILE_NAME = "vacancy.json"

settings = return_json('settings.json').get('data', {})


def send_telegram(uid, message):
    try:
        result = requests.post(
            url = settings.get('host') + '/message',
            json = {
                'id': uid,
                'sender': settings.get('sender'),
                'text': message,
            },
            headers = {
                "token": settings.get('token'),
            }
        )

        print(message)

        return result.status_code == 200 and result.json().get('success')
    except Exception as e:
        print(e)

    return False


def main():
    yandex_api_url = 'https://yandex.ru/jobs/api/publications/'

    fake = faker.Faker(locale='ru')

    yandex_params = {
        'page_size': 1000,
        'cities': 'moscow',
        'professions': 'backend-developer',
        'pro_levels': 'junior',
        'skills': 34,
    }

    yandex_headers = {
        'User-Agent': fake.chrome(),
        'accept-language': 'en-US,en;q=0.9',
        'pragma': 'np-cache',
        'content-type': 'application/json',
        'referer': 'http://yandex.ru/jobs/vacancies',
    }

    result = requests.get(
        url = yandex_api_url,
        params = yandex_params,
        headers = yandex_headers,
    )

    vacancy_data = return_json(FILE_NAME).get('data', {})

    data = result.json()

    for vacancy in data.get('results', []) or []:
        builded_link = f"https://yandex.ru/jobs/vacancies/{vacancy.get('id', 0)}"

        if vacancy.get('is_chief', False) or {'id': 34, 'name': 'Python'} not in vacancy.get('vacancy', {}).get('skills', []):
            continue

        if vacancy_data.get(str(vacancy['id'])):
            continue

        vacancy_data[str(vacancy['id'])] = {
            "link": builded_link,
            "tile": vacancy.get('title'),
            "short_summary": vacancy.get('short_summary'),
            "id": vacancy.get('id'),
            "insert_time": int(time.time())
        }

        if settings.get('host') and settings.get('sender') and settings.get('token'):
            while True:
                result = send_telegram(
                    uid = 'yandex_vacancies_%i' % (
                        vacancy.get('id'),
                    ),
                    message = 'Новая вакансия от яндекс %s' % (
                        builded_link,
                    ),
                )

                if result:
                    break

        print(
            'Новая вакансия от яндекс %s' % (
                builded_link,
            )
        )

    save_json_with_ident(
        FILE_NAME,
        vacancy_data,
        ascii_=False,
    )


if __name__ == '__main__':
    main()