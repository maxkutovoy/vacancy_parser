import requests


def main():
    hh_api_url = 'https://api.hh.ru/vacancies'
    params = {
        "text": "программист"
    }
    response = requests.get(hh_api_url, params=params)
    response.raise_for_status()
    print(response.url)
    print(response.json())


if __name__ == '__main__':
    main()
