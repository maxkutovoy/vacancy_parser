import requests
from pprint import pprint

languages = [
    'javascript',
    'java',
    'python',
    'ruby',
    'php',
    'c++',
    'c',
    'go',
    'Objective-C'
]


def predict_rub_salary(vacancy):
    try:
        if vacancy['salary']['currency'] == 'RUR':
            if vacancy['salary']['from']:
                min_salary = vacancy['salary']['from']
            else:
                min_salary = "Не указано"
            if vacancy['salary']['to']:
                max_salary = vacancy['salary']['to']
            else:
                max_salary = "Не указано"
            if min_salary == "Не указано":
                predict_rub_salary = max_salary*0.8
            elif max_salary == "Не указано":
                predict_rub_salary = min_salary*1.2
            else:
                predict_rub_salary = max_salary+min_salary/2
            return predict_rub_salary
    except:
        return None


def main():
    parsed_info = {}
    for language in languages:
        all_mid_salaries = []

        for page in range(100):
            hh_api_url = 'https://api.hh.ru/vacancies'
            params = {
                'text': language,
                'area': '1',
                'page': page
            }
            response = requests.get(hh_api_url, params=params)
            response.raise_for_status()
            all_vacancies = response.json()
            for vacancy in all_vacancies['items']:
                if predict_rub_salary(vacancy) is not None:
                    all_mid_salaries.append(predict_rub_salary(vacancy))
            mid_salary = sum(all_mid_salaries)/len(all_mid_salaries)
            parsed_info[language] = {
                "vacancies_found": all_vacancies['found'],
                "vacancies_processed": len(all_mid_salaries),
                "average_salary": int(mid_salary),
            }
    pprint(parsed_info)


if __name__ == '__main__':
    main()
