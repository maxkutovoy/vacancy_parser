import requests
from terminaltables import AsciiTable

import itertools
import os
from dotenv import load_dotenv


def predict_salary(salary_from, salary_to):
    if not salary_from and not salary_to:
        return None
    elif not salary_from:
        predicted_mid_salary = salary_to * 0.8
    elif not salary_to:
        predicted_mid_salary = salary_from * 1.2
    else:
        predicted_mid_salary = (salary_to+salary_from) / 2
    return predicted_mid_salary


def predict_rub_salary_hh(vacancy):
    if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
        salary_from = vacancy['salary']['from']
        salary_to = vacancy['salary']['to']
        return predict_salary(salary_from, salary_to)


def predict_rub_salary_sj(vacancy):
    if vacancy['currency'] == 'rub':
        salary_from = vacancy['payment_from']
        salary_to = vacancy['payment_to']
        return predict_salary(salary_from, salary_to)


def get_sj_predicted_salaries(vacancies):
    predicted_salaries = []
    for vacancy in vacancies:
        predicted_rub_salary = predict_rub_salary_sj(vacancy)
        if predicted_rub_salary:
            predicted_salaries.append(predicted_rub_salary)
    return predicted_salaries


def get_hh_predicted_salaries(vacancies):
    predicted_salaries = []
    for vacancy in vacancies:
        predicted_rub_salary = predict_rub_salary_hh(vacancy)
        if predicted_rub_salary:
            predicted_salaries.append(predicted_rub_salary)
    return predicted_salaries


def get_average_salary(predicted_salaries):
    try:
        average_salary = sum(predicted_salaries) / len(predicted_salaries)
    except ZeroDivisionError:
        return 0
    return int(average_salary)


def get_sj_vacancies(token, profession):
    cities_indexes = {
        'Moscow': 4,
        'Владивосток': 70,
    }
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': token
    }
    downloaded_vacancies = []
    for page in itertools.count(start=0, step=1):
        payload = {
            'keyword': profession,
            'town': cities_indexes['Moscow'],
            'count': 100,
            'page': page,
        }
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        received_vacancies = response.json()
        downloaded_vacancies += received_vacancies['objects']
        if not received_vacancies['more']:
            break
    vacancies_found = received_vacancies['total']
    return downloaded_vacancies, vacancies_found


def get_all_hh_vacancies(profession):
    cities_indexes = {
        'Moscow': '1',
        'Saint Petersburg': '2',
        'Omsk': '68',
    }
    url = 'https://api.hh.ru/vacancies'
    downloaded_vacancies = []
    for page in itertools.count(start=0, step=1):
        payload = {
            'text': profession,
            'area': cities_indexes['Moscow'],
            'page': page,
            'per_page': 100,
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        received_vacancies = response.json()
        downloaded_vacancies += received_vacancies['items']
        if page is received_vacancies['pages'] - 1:
            break
    vacancies_found = received_vacancies['found']
    return downloaded_vacancies, vacancies_found


def get_superjob_statistic(token, professions):
    professions_statistic = {}
    for profession in professions:
        downloaded_vacancies, vacancies_found = get_sj_vacancies(token, profession)
        predicted_salaries = get_sj_predicted_salaries(downloaded_vacancies)
        average_salary = get_average_salary(predicted_salaries)

        professions_statistic[profession] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(downloaded_vacancies),
            'average_salary': average_salary,
        }
    return professions_statistic


def get_hh_statistic(professions):
    professions_statistic = {}
    for profession in professions:
        downloaded_vacancies, vacancies_found = get_all_hh_vacancies(profession)
        predicted_salaries = get_hh_predicted_salaries(downloaded_vacancies)
        average_salary = get_average_salary(predicted_salaries)

        professions_statistic[profession] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(downloaded_vacancies),
            'average_salary': int(average_salary),
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
    table_instance = AsciiTable(table_data, title)
    return table_instance.table


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

    sj_token = os.getenv('SUPERJOB_TOKEN')
    professions_hh_statistic = get_hh_statistic(professions)
    professions_sj_statistic = get_superjob_statistic(sj_token, professions)
    sj_table_title = 'SuperJob Moscow'
    hh_table_title = 'HeadHunter Moscow'
    print(draw_table(sj_table_title, professions_sj_statistic))
    print(draw_table(hh_table_title, professions_hh_statistic))


if __name__ == '__main__':
    main()
