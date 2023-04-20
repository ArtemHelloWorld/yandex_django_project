<h1 align="center">FlavorVerse - поэзия вкуса</h1>

[![Python | flake8 & black](https://github.com/arsyst/ya-django-project/actions/workflows/python-package.yml/badge.svg)](https://github.com/arsyst/ya-django-project/actions/workflows/python-package.yml)
[![django | tests](https://github.com/arsyst/ya-django-project/actions/workflows/django-tests.yml/badge.svg)](https://github.com/arsyst/ya-django-project/actions/workflows/django-tests.yml)


<h2>О ПРОЕКТЕ</h2>
<p>FlavorVerse - это веб-сайт для людей, умеющих и любящих готовить которые ищут новые идеи для своих кулинарных шедевров и которые хотят попасть в комьюнити с такими же, как они, энтузиастами и получить опыт от именитых поваров.</p>
<p>Главная особенность нашего сайта в том, что любой пользователь сможет подобрать рецепт по списку продуктов, которые есть у него в холодильнике, и составить список недостающих продуктов. </p>


<h2>КАК ЗАПУСТИТЬ</h2>

1. <h4>Установите зависимости</h4>

<h5>Основные | Django & transliterate & dotenv</h5>
<pre><code>$ pip install -r requirements/requirements-prod.txt</code></pre>

<h5>Дополнительные</h5>
Для разработки | toolbar & black & flake8 & isort <pre><code>$ pip install -r requirements/requirements-dev.txt</code></pre>
Для тестов | freezegun & parameterized<pre><code>$ pip install -r requirements/requirements-test.txt</code></pre>


2. <h4>Добавьте в корневой каталог файл .env(Пример можно посмотреть в файле .env-example), содержащий поля:</h4>

* SECRET_KEY | Используйте надежный ключ, содержащий больше 50 символов

* DEBUG | Установите True, если проект на стадии разработки(Требуется также установить дополнительные зависимости для разработки)

* ALLOWED_HOSTS | Используйте запятую(без пробелов) для указания нескольких доступных хостов

* DJANGO_SUPERUSER_USERNAME; DJANGO_SUPERUSER_EMAIL; DJANGO_SUPERUSER_PASSWORD | Укажите, чтобы создать супер юзера командной  initdata  (ниже описано использование команды)

* DEFAULT_FROM_EMAIL | Почта для отправки сообщений

* ACTIVATE_USERS | Установите False, если хотите, чтобы для регистрации пользоватеям было необходимо подтвердить свою почту

* MAX_FAILED_LOGIN_ATTEMPTS | Максимальное число попыток входа в аккаунт

* RATE_LIMIT_MIDDLEWARE | Установите True, чтобы ограничить количество запросов с одного IP

* REQUESTS_PER_SECOND | Максимальное количество запросов в секунду. Понадобится, если RATE_LIMIT_MIDDLEWARE равен True

* EMAIL_HOST; EMAIL_PORT; EMAIL_HOST_USER; EMAIL_HOST_PASSWORD; EMAIL_USE_TLS; EMAIL_USE_SSL | Укажите для отправки электронных писем


3. <h4>Запустите локальный сервер </h4><pre><code>$ python project/manage.py runserver</code></pre>



<h2>создание базы данных</h2>
Чтобы создать бд, необходимо выполнить миграции<pre><code>$ python project/manage.py migrate</code></pre>
Чтобы добавить тестовые данные, воспользуйтесь фикстурами. Пример с загрузкой данных из приложения catalog: <pre><code>$ python project/manage.py loaddata project/dishes/fixtures/fixture.json</code></pre>



<h2>ИНИЦИАЛИЗАЦИЯ ДАННЫХ</h2>
После установки необходимых зависимостей вы можете воспользоваться кастомной командой initdata<pre><code>$ python project/manage.py initdata</code></pre>Эта команда выполнит следующие шаги:

1. Проверит базу данных на все миграции. --skip-checking-database для отключения

2. Загрузит необходимые данные из фикстур. --skip-loading-data для отключения

3. Создаcт супер пользователя. --skip-creating-superuser для отключения. Данные администратора можно указать слудующими способами:

* Указать в виртуальном окружении(.env) следующие поля: DJANGO_SUPERUSER_USERNAME; DJANGO_SUPERUSER_EMAIL; DJANGO_SUPERUSER_PASSWORD

* Ввести вручную, добавив в команду аргумент --interactive

<h2>диаграмма базы данных</h2>

![alt text](https://github.com/arsyst/ya-django-project/blob/51e0e7e6188a028107ef3eb7e285e56ae8bc8022/er_models/db.png)
