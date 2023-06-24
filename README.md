# Моя Инициатива Backend
Backend часть проекта "Моя Инициатива", который предоставляет API для взаимодействия с инициативами, проектами и пользователями.

## Описание проекта
"Моя Инициатива" - это платформа, где люди могут предлагать свои инициативы, проекты для развития страны или деловые проекты. Пользователи могут просматривать доступные инициативы, голосовать за понравившиеся инициативы и ставить лайки. Лучшие инициативы будут представлены спонсорам и государственным деятелям.

## Технологии
* Django: Python-фреймворк для разработки веб-приложений.
* Django REST framework: Мощный инструмент для создания API на основе Django.
* База данных: Обычно используется PostgreSQL для хранения данных проблем и пользователей.

## API Endpoints
### Аутентификация
* POST /api/auth/users/ - Регистрация нового пользователя
* POST /api/auth/login/ - Логин. Получить JWT токены
* POST /api/auth/logout/ - Разлогинивание пользователя. Добавляет refresh токен в черный список
* POST /api/auth/jwt/refresh/ - Обновление access токена с помощью refresh токена
* POST /api/auth/users/set_password/ - Смена пароля авторизированного пользователя
* POST /api/auth/phone/getcode/<uuid:pk>/ - Запрос отправки кода на телефон (SMS или звонок) для подтверждения номера телефона
* POST /api/auth/phone/verify/<uuid:pk>/ - Отправка кода, полученного на телефон, для подтверждения номера телефона
* POST /api/auth/phone/getcode/password-reset/ - Первый шаг для сброса забытого пароля. Запрос на отправку кода на телефон для подтверждения владения аккаунтом
* POST /api/auth/phone/verify/password-reset/ - Второй шаг для сброса забытого пароля. Отправка кода, полученного на телефон. Если код верный, то пользователь получает uid и token для сброса пароля
* POST /api/auth/users/reset_password_confirm/ - Последний шаг для сброса забытого пароля.
### Управление аккаунтами
* GET /api/accounts/all/ - Получить список всех аккаунтов
* PUT/PATCH /api/accounts/update/<uuid:pk>/ - Внести изменения в определенный аккаунт
* DELETE /api/accounts/delete/<uuid:pk>/ - Удалить аккаунт
* GET /api/accounts/details/<uuid:pk>/ - Получить полную информацию по аккаунту и профилю пользователя
* PUT/PATCH /api/profile/update/<uuid:pk>/ - Добавить изменения в профиль пользователя
### Категории
* GET /api/categories/all/ - Получить список всех категорий
* POST /api/categories/create/ - Создать новую категорию
* PUT/PATCH/DELETE /api/categories/update/<uuid:pk>/ - Обновить название, иконку категории или удалить категорию
### Проекты
* POST /api/projects/comment/add/ - Написать комментарий под проектом или ответить на комментарий
* PATCH/DELETE /api/projects/comment/update/<uuid:pk>/ - Обновить текст комментария или удалить комментарий
* GET /api/projects/comment/all/<uuid:pk>/ - Получить список комментариев под проектом
* GET /api/projects/comment/replies/<uuid:pk>/ - Получить список всех ответов на комментарий
* POST /api/projects/likedislike/<uuid:pk>/ - Поставить лайк или дизлайк проекту, обновить предыдущий лайк или дизлайк
* POST /api/projects/comment/likedislike/<uuid:pk>/ - Поставить лайк или дизлайк комментарию, обновить предыдущий лайк или дизлайк
* GET /api/projects/details/<uuid:pk>/ - Получить полную информацию по проекту
* POST /api/projects/create/ - Создать новый проект
* DELETE /api/projects/delete/<uuid:pk>/ - Удалить проект
* PATCH /api/projects/update/<uuid:pk>/ - Обновить проект
* PATCH /api/projects/updatesuper/<uuid:pk>/ - Обновить проект (полный доступ)
* GET /api/projects/mylist/ - Получить список созданных своих проектов
* GET /api/projects/approved/ - Получить список всех опубликованных проектов
* GET /api/projects/all/ - Получить список всех проектов
* POST /api/projects/attachment/upload/ - Загрузить файл к проекту
* PATCH /api/projects/attachment/update/<uuid:pk>/ - Заменить загруженный файл на другой
* POST /api/projects/link/add/ - Добавить ссылку к проекту
* PATCH /api/projects/link/update/<uuid:pk>/ - Заменить ссылку на другую

## Установка и настройка проекта
Клонируйте репозиторий на свою локальную машину.
Создайте и активируйте виртуальное окружение.
Установите зависимости, выполнив команду: pip install -r requirements.txt.
Создайте базу данных и настройте подключение к ней в файле settings.py.
Выполните миграции с помощью команды: python manage.py migrate.
Запустите сервер разработки с помощью команды: python manage.py runserver.
Теперь вы можете обращаться к API эндпоинтам, указанным выше, для взаимодействия с приложением.