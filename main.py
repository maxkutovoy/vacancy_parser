import requests
from terminaltables import AsciiTable

import os
from dotenv import load_dotenv


def predict_salary(salary_from, salary_to):
    if (not salary_from) & (not salary_to):
        return None
    elif not salary_from:
        predict_mid_salary = salary_to * 0.8
    elif not salary_to:
        predict_mid_salary = salary_from * 1.2
    else:
        predict_mid_salary = salary_to + salary_from / 2
    return predict_mid_salary


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


def get_superjob_statistic(token, professions):
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": token
    }
    professions_statistic = {}
    for profession in professions:
        all_mid_salaries = []
        for page in range(2):
            payload = {
                'keyword': profession,
                'town': 4,
                'count': 100,
                'page': page,
            }
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            all_vacancies = response.json()
            for vacancy in all_vacancies['objects']:
                predict_rub_salary = predict_rub_salary_sj(vacancy)
                if predict_rub_salary:
                    all_mid_salaries.append(predict_rub_salary)
        mid_salary = sum(all_mid_salaries) / len(all_mid_salaries)
        professions_statistic[profession] = {
            "vacancies_found": all_vacancies['total'],
            "vacancies_processed": len(all_mid_salaries),
            "average_salary": int(mid_salary),
        }
    return professions_statistic


def get_hh_statistic(professions):
    hh_api_url = 'https://api.hh.ru/vacancies'
    professions_statistic = {}
    for profession in professions:
        all_mid_salaries = []
        for page in range(2):
            params = {
                'text': profession,
                'area': '1',
                'page': page,
                'per_page': 100,
            }
            response = requests.get(hh_api_url, params=params)
            response.raise_for_status()
            all_vacancies = response.json()
            for vacancy in all_vacancies['items']:
                predict_rub_salary = predict_rub_salary_hh(vacancy)
                if predict_rub_salary:
                    all_mid_salaries.append(predict_rub_salary)
        mid_salary = sum(all_mid_salaries) / len(all_mid_salaries)
        professions_statistic[profession] = {
            "vacancies_found": all_vacancies['found'],
            "vacancies_processed": len(all_mid_salaries),
            "average_salary": int(mid_salary),
        }
    return professions_statistic


def draw_table(title, statistic_dict):
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
    ]
    for profession, statistic in statistic_dict.items():
        profession_statistic = [
            profession,
            statistic['vacancies_found'],
            statistic['vacancies_processed'],
            statistic['average_salary']
        ]
        table_data.append(profession_statistic)
    title = title
    table_instance = AsciiTable(table_data, title)
    print(table_instance.table)
    print()


def main():
    load_dotenv()
    professions = [
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

    superjob_token = os.getenv("SUPERJOB_TOKEN")
    professions_sj_statistic = get_superjob_statistic(superjob_token, professions)
    professions_hh_statistic = get_hh_statistic(professions)
    sj_table_title = 'HeadHunter Moscow'
    hh_table_title = 'SuperJob Moscow'
    draw_table(sj_table_title, professions_sj_statistic)
    draw_table(hh_table_title, professions_hh_statistic)


if __name__ == '__main__':
    main()
