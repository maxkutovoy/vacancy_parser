# Сервис для рассчета средней ожидаемой зарплаты

Сервис собирает информацию по указанным зарплам с сайтов [hh.ru](https://hh.ru) и [suprejob.ru](https://suprejob.ru)
по указанным профессиям и выдает средний результат

## Как установить

### Установить зависимости

 Python3 должен быть уже установлен. Далее используйте `pip` (или `pip3`, есть конфликт с python2) для установки зависимостей:

```
pip install -r requirements.txt
```

### Получить токен

Для сбора информации с сайта  [suprejob.ru](https://suprejob.ru) необходимо получить ключ к API (токен).

Инструкция для получения токена [здесь](https://api.superjob.ru/) 

Полученный токен нужно присвоить переменной `SUPERJOB_TOKEN` в файле `.env`. Файл необходимо создать в корневом 
каталоге проекта. Содержимое файла должно выглядеть так:

```
SUPERJOB_TOKEN="ваш_токен"
```

## Как использовать

Сервис не требует дополнительных параметорв для запуска. Список профессий находится в переменной `professions`. Его 
можно менять на свое усмотрение

Команда для запуска в терминале Widows:

```
python main.py
```

и для MacOS и Linux:

```
python3 main.py
```

## Цель проекта

Код написан в образовательных целях на курсе для web-разработчиков [dvmn.org](https://dvmn.org/)