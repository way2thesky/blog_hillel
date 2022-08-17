.. celebrities_stand_up_for_ukraine
.. README.rst


Celebrities Stand Up for Ukraine documentation
==============================================


.. contents::

Description
-----------

24.02 AT 5:00 AM THE WAR BEGAN IN UKRAINE

the Project is all about Celebrities and World Leaders Stand Up for Ukraine

Local development third-party services
--------------------------------------

Install, configure and create next services users/hosts/etc if needed.

* `PostgreSQL <https://www.postgresql.org/>`_

Local development bootstrap pre-requirements
--------------------------------------------

Install and configure:

* `pyenv <https://github.com/pyenv/pyenv/>`_: used to manage project local python interpreter version.
* `direnv <https://github.com/direnv/direnv/>`_: used to set-up local virtualenv and setting up environment variables.
* GNU/Make: used to shorten some useful things calls.

Local development bootstrap
---------------------------

1. Run ``$ make bootstrap ENV=dev``. Or ``$ make setup-env``, ``$ make install-requirements ENV=dev`` and ``$ make install-pre-commit-hook``.
2. Edit ``.env`` on your taste.
3. Run ``$ make migrate``.
4. Create superuser: ``$ make createsuperuser``.
5. Run ``$ make runserver``.
6. Run: ``$ xdg-open http://localhost:8080/`` and Voila.

Additional helpful actions with their descriptions available in ``Makefile`` help.
Just run ``$ make help``.

Local Docker development bootstrap pre-requirements
---------------------------------------------------

Install and configure:

* `Docker <https://www.docker.com/>`_
* `docker-compose <https://docs.docker.com/compose/>`_

Docker development bootstrap
----------------------------

1. Run ``$ make setup-env`` and ``$ make install-pre-commit-hook``.
2. Edit ``.env`` on your taste.
3. Build images: ``$ make build``.
4. Run migrate ``$ make migrate-d``.
5. Run containers: ``$ make up``.
6. Create superuser: ``$ make createsuperuser-d``.
7. Run: ``$ xdg-open http://localhost:8080/`` and Voila.

Additional docker specific actions with their descriptions available in ``Makefile`` help.
Most of them have ``-d`` suffix.
Just run ``$ make help``.


# Practical work Blog built with Django
# http://way2thesky.pythonanywhere.com/blog/

## Technology Stack:
JQuery, AJAX, Docker, DRF, Nginx, PostgreSQL, Redis, Rabbitmq, Celery

## Этот проект включает:!!!

* Регистрация!
* Функции CRUD (создание или убирать их в заготовки, чтение, обновление, удаление)
* Анонимные пользователи могут публиковать комментарии
* Комментарии модерируется перед публикацией
* Администратор получает уведомление на почту о новом посте или комментарии (в консоль)
* Пользователь получает уведомление о новом комментарии под постом с сылкой на пост (в консоль)
* Поделиться постом через email
* Templetags*
* HTML, CSS
* Ajax Форма обратной связи с админом  (в консоль)









