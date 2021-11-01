import requests
from terminaltables import AsciiTable

import os
from dotenv import load_dotenv


def predict_salary(salary_from, salary_to):
    if (not salary_from) & (not salary_to):
        return None
    elif not salary_from:
        predicted_mid_salary = salary_to * 0.8
    elif not salary_to:
        predicted_mid_salary = salary_from * 1.2
    else:
        predicted_mid_salary = (salary_to+salary_from)/2
    return predicted_mid_salary


def predict_rub_salary_hh(vacancy):
    if vacancy['salary']:
        if vacancy['salary']['currency'] == 'RUR':
            salary_from = vacancy['salary']['from']
            salary_to = vacancy['salary']['to']
            return predict_salary(salary_from, salary_to)


def predict_rub_salary_sj(vacancy):
    if vacancy['currency'] == 'rub':
        salary_from = vacancy['payment_from']
        salary_to = vacancy['payment_to']
        return predict_salary(salary_from, salary_to)


def get_all_sj_predicted_salaries(all_vacancies):
    all_predicted_salaries = []
    for vacancy in all_vacancies:
        predicted_rub_salary = predict_rub_salary_sj(vacancy)
        if predicted_rub_salary:
            all_predicted_salaries.append(predicted_rub_salary)
    return all_predicted_salaries


def get_all_hh_predicted_salaries(all_vacancies):
    all_predicted_salaries = []
    for vacancy in all_vacancies:
        predicted_rub_salary = predict_rub_salary_hh(vacancy)
        if predicted_rub_salary:
            all_predicted_salaries.append(predicted_rub_salary)
    return all_predicted_salaries


def get_average_salary(all_predicted_salaries):
    average_salary = sum(all_predicted_salaries) / len(all_predicted_salaries)
    return int(average_salary)


def get_all_sj_vacancies(url, headers, profession):
    all_sj_vacancies = []
    for page in range(20):
        payload = {
            'keyword': profession,
            'town': 4,
            'count': 100,
            'page': page,
        }
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        received_vacancies = response.json()
        all_sj_vacancies += list(received_vacancies['objects'])
        if not received_vacancies['more']:
            break
    return all_sj_vacancies


def get_all_hh_vacancies(url, profession):
    all_hh_vacancies = []
    for page in range(10):
        payload = {
            'text': profession,
            'area': '1',
            'page': page,
            'per_page': 100,
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        received_vacancies = response.json()
        if received_vacancies['items']:
            all_hh_vacancies += list(received_vacancies['items'])
        else:
            break
    return all_hh_vacancies


def get_superjob_statistic(token, sj_api_url, professions):
    headers = {
        "X-Api-App-Id": token
    }
    professions_statistic = {}
    for profession in professions:
        all_sj_vacancies = get_all_sj_vacancies(sj_api_url, headers, profession)
        all_predicted_salaries = get_all_sj_predicted_salaries(all_sj_vacancies)
        average_salary = get_average_salary(all_predicted_salaries)
        vacancies_found = len(all_sj_vacancies)

        professions_statistic[profession] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": len(all_predicted_salaries),
            "average_salary": average_salary,
        }
    return professions_statistic


def get_hh_statistic(hh_api_url, professions):
    professions_statistic = {}
    for profession in professions:
        all_hh_vacancies = get_all_hh_vacancies(hh_api_url, profession)
        all_predicted_salaries = get_all_hh_predicted_salaries(all_hh_vacancies)
        average_salary = get_average_salary(all_predicted_salaries)
        vacancies_found = len(all_hh_vacancies)

        professions_statistic[profession] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": len(all_predicted_salaries),
            "average_salary": int(average_salary),
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

    hh_api_url = 'https://api.hh.ru/vacancies'
    sj_api_url = "https://api.superjob.ru/2.0/vacancies/"
    sj_token = os.getenv("SUPERJOB_TOKEN")
    professions_hh_statistic = get_hh_statistic(hh_api_url, professions)
    professions_sj_statistic = get_superjob_statistic(sj_token, sj_api_url, professions)
    sj_table_title = 'SuperJob Moscow'
    hh_table_title = 'HeadHunter Moscow'
    print(draw_table(sj_table_title, professions_sj_statistic))
    print(draw_table(hh_table_title, professions_hh_statistic))


if __name__ == '__main__':
    main()
