import requests
from pprint import pprint

import os
from dotenv import load_dotenv

languages = [
    'javascript',
    'java',
    'python',
    # 'ruby',
    # 'php',
    # 'c++',
    # 'c',
    # 'go',
    # 'Objective-C'
]
load_dotenv()


def predict_salary(salary_from, salary_to):
    if (salary_from is None or salary_from == 0) & (salary_to is None or salary_to == 0):
        return None
    elif salary_from is None or salary_from == 0:
        predict_rub_salary = salary_to * 0.8
    elif salary_to is None or salary_to == 0:
        predict_rub_salary = salary_from * 1.2
    else:
        predict_rub_salary = salary_to + salary_from / 2
    return predict_rub_salary


def predict_rub_salary_hh(vacancy):
    if vacancy['salary']:
        if vacancy['salary']['currency'] == 'RUR':
            salary_from = vacancy['salary']['from']
            salary_to = vacancy['salary']['to']
            return predict_salary(salary_from, salary_to)
    else:
        return None


def predict_rub_salary_sj(vacancy):
    if vacancy['currency'] == 'rub':
        salary_from = vacancy['payment_from']
        salary_to = vacancy['payment_to']
        return predict_salary(salary_from, salary_to)
    else:
        return None


def superjob_parser():
    superjob_token = os.getenv("SUPERJOB_TOKEN")
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": superjob_token
    }
    language_statistic = {}
    for language in languages:
        all_mid_salaries = []
        for page in range(5):
            payload = {
                'keyword': language,
                'town': 4,
                'count':100,
                'page': page,
            }
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            all_vacancies = response.json()
            for vacancy in all_vacancies['objects']:
                predict_rub_salary = predict_rub_salary_sj(vacancy)
                if predict_rub_salary is not None:
                    all_mid_salaries.append(predict_rub_salary)
        mid_salary = sum(all_mid_salaries) / len(all_mid_salaries)
        language_statistic[language] = {
            "vacancies_found": all_vacancies['total'],
            "vacancies_processed": len(all_mid_salaries),
            "average_salary": int(mid_salary),
        }
    pprint(language_statistic)


def hh_parser():
    hh_api_url = 'https://api.hh.ru/vacancies'
    language_statistic = {}
    for language in languages:
        all_mid_salaries = []
        for page in range(20):
            params = {
                'text': language,
                'area': '1',
                'page': page,
                'per_page': 100,
            }
            response = requests.get(hh_api_url, params=params)
            response.raise_for_status()
            all_vacancies = response.json()
            for vacancy in all_vacancies['items']:
                predict_rub_salary = predict_rub_salary_hh(vacancy)
                if predict_rub_salary is not None:
                    all_mid_salaries.append(predict_rub_salary)
        mid_salary = sum(all_mid_salaries)/len(all_mid_salaries)
        language_statistic[language] = {
            "vacancies_found": all_vacancies['found'],
            "vacancies_processed": len(all_mid_salaries),
            "average_salary": int(mid_salary),
        }
    pprint(language_statistic)


def main():
    superjob_parser()
    hh_parser()



if __name__ == '__main__':
    main()
