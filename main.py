import requests
from pprint import pprint

import os
from dotenv import load_dotenv

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
load_dotenv()


def predict_salary(salary_from, salary_to):
    try:
        min_salary = salary_from
        max_salary = salary_to

        if (min_salary is None or min_salary == 0) & (max_salary is None or max_salary == 0):
            return None
        if min_salary is None or min_salary == 0:
            predict_rub_salary = max_salary * 0.8
        elif max_salary is None or max_salary == 0:
            predict_rub_salary = min_salary * 1.2
        else:
            predict_rub_salary = max_salary + min_salary / 2
        return predict_rub_salary
    except:
        return None


# def predict_rub_salary_for_superJob(vacancy):
#     try:
#         if vacancy['currency'] == 'rub':
#             min_salary = vacancy['payment_from']
#             max_salary = vacancy['payment_to']
#
#             if min_salary == 0 & max_salary == 0:
#                 return None
#             if min_salary == 0:
#                 predict_rub_salary = max_salary*0.8
#             elif max_salary == 0:
#                 predict_rub_salary = min_salary*1.2
#             else:
#                 predict_rub_salary = max_salary+min_salary/2
#             return predict_rub_salary
#     except:
#         return None


def superjob_parser():
    superjob_token = os.getenv("SUPERJOB_TOKEN")
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": superjob_token
    }

    for language in languages:
        all_mid_salaries = []
        language_statistic = {}
        for page in range(5):
            payload = {
                "t": "4",
                'keyword': language,
                'town': 4,
                'count':100,
                'page': page,
            }
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            all_vacancies = response.json()

            for vacancy in all_vacancies['objects']:
                salary_from = vacancy['payment_from']
                salary_to = vacancy['payment_to']
                predict_rub_salary = predict_salary(salary_from, salary_to)
                if predict_rub_salary is not None:
                    all_mid_salaries.append(predict_rub_salary)
        mid_salary = sum(all_mid_salaries)/len(all_mid_salaries)
        language_statistic[language] = {
            "vacancies_found": all_vacancies['total'],
            "vacancies_processed": len(all_mid_salaries),
            "average_salary": int(mid_salary),
        }
                # print(f"Профессия: {vacancy['profession']}, регион: {vacancy['town']['title']}, ожидаемая зарплата: {predict_rub_salary}")
        pprint(language_statistic)

superjob_parser()

        # def predict_rub_salary(vacancy):
        #     try:
        #         if vacancy['salary']['currency'] == 'RUR':
        #             if vacancy['salary']['from']:
        #                 min_salary = vacancy['salary']['from']
        #             else:
        #                 min_salary = "Не указано"
        #             if vacancy['salary']['to']:
        #                 max_salary = vacancy['salary']['to']
        #             else:
        #                 max_salary = "Не указано"
        #             if min_salary == "Не указано":
        #                 predict_rub_salary = max_salary*0.8
        #             elif max_salary == "Не указано":
        #                 predict_rub_salary = min_salary*1.2
        #             else:
        #                 predict_rub_salary = max_salary+min_salary/2
        #             return predict_rub_salary
        #     except:
        #         return None
        #
        #
        # def main():
        #     language_statistic = {}
        #         for page in range(20):
        #             hh_api_url = 'https://api.hh.ru/vacancies'
        #             params = {
        #                 'text': language,
        #                 'area': '1',
        #                 'page': page
        #                 'per_page': 100
        #             }
        #             response = requests.get(hh_api_url, params=params)
        #             response.raise_for_status()
        #             all_vacancies = response.json()
        #             for vacancy in all_vacancies['items']:
        #                 if predict_rub_salary(vacancy) is not None:
        #                     all_mid_salaries.append(predict_rub_salary(vacancy))
        #             mid_salary = sum(all_mid_salaries)/len(all_mid_salaries)
        #             language_statistic[language] = {
        #                 "vacancies_found": all_vacancies['found'],
        #                 "vacancies_processed": len(all_mid_salaries),
        #                 "average_salary": int(mid_salary),
        #             }
        #     pprint(language_statistic)
        #
        #
        # if __name__ == '__main__':
        #     main()
