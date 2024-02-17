import requests
### Создание объявление

# response = requests.post(
#     'http://127.0.0.1:5000/announcement/',
#     json = {'title': 'announcement_3'},
# )
#
# print(response.status_code)
# print(response.text)

## Получение объявления по его ID

# response = requests.get(
#     'http://127.0.0.1:5000/announcement/7/',
#
# )
#
# print(response.status_code)
# print(response.text)


### Изменение названия объявления по его ID

# response = requests.patch(
#     'http://127.0.0.1:5000/announcement/1/',
#     json={"title": "announcement_444"}
# )
# print(response.status_code)
# print(response.text)


### Проверка измененного объявления

# response = requests.get(
#     'http://127.0.0.1:5000/announcement/1/',
#
# )
#
# print(response.status_code)
# print(response.text)


###Удаление объявления по его ID

# response = requests.delete(
#     "http://127.0.0.1:5000/announcement/5/",
# )
# print(response.status_code)
# print(response.text)