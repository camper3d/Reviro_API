API создаёт, читает, обновляет и удаляет задачи. Использует БД Sqlite.
Каждая задача содержит заголовок, описание, дату выполнения и статус. 
Поддерживается фильтрация задач по статусу и дате, а также простая авторизация с использованием токена.

Устанавливаем зависимости при помощи команды: pip install -r requirements.txt
Запуск приложения с помощью команды: uvicorn app.main:app --reload

Запросы curl:

- Получить задачи со статусом new, с авторизацией:

curl -X GET "http://localhost:8000/tasks?status=new" \
-H "Authorization: Bearer ReviroTopCompany777"

- Получить задачу по ID:

curl -X GET "http://localhost:8000/tasks/1" \
-H "Authorization: Bearer ReviroTopCompany777"

- Создать новую задачу:

curl -X POST "http://localhost:8000/tasks" \
-H "Authorization: Bearer ReviroTopCompany777" \
-H "Content-Type: application/json" \
-d '{
  "title": "Купить продукты",
  "description": "Молоко, яйца, хлеб",
  "due_date": "2025-06-10",
  "status": "new"
}'

- Обновить задачу:

curl -X PUT "http://localhost:8000/tasks/1" \
-H "Authorization: Bearer ReviroTopCompany777" \
-H "Content-Type: application/json" \
-d '{
  "title": "Купить продукты и напитки",
  "status": "in_progress"
}'

- Удалить задачу:

curl -X DELETE "http://localhost:8000/tasks/1" \
-H "Authorization: Bearer ReviroTopCompany777"

Рефлексия:

1. Самым сложным было организовать импорты в модулях,
не запутаться в crud операциях и эндпоинтах
2. Мне понравилась моя структура проекта, авторизация,
Работа с БД
3. Заморочился бы больше по обработке ошибок, добавил бы тестирование с pytest,
логирование, сложную авторизацию
4. Выполнение задания заняло примерно 7-8 часов
5. Научился лучше структурировать модули, разделять логику,
укрепил знания по FastAPI,Pydantic,Sqlalchemy