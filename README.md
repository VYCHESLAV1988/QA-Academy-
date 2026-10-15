# QA Academy — Junior QA / Java Automation

English questions, русские объяснения, английские образцы ответа. Основная опубликованная ветка: `main`.

## Текущий урок: SQL Foundations
В `prototype/lesson.html` доступны шесть основных вопросов SELECT / WHERE / AND / ORDER BY и шесть новых примеров закрепления. Вопросы и варианты показаны на английском с отключаемым переводом. Разбор содержит верную часть выбранного варианта, ошибку, шаги решения, Sample answer и Key terms. Баллы не заменяют объяснение. Служебные описания разработки убраны с учебного экрана.

Это текущий урок, не весь запланированный курс. Материалы `bank.py` сохранены; они ещё не подключены целиком. Цель 1070 заданий остаётся незавершённой. Расширение выполняется по [стандарту обучения](docs/TEACHING-STANDARD.md), а не за счёт дублирования формулировок. Вопросы авторские: они не выдаются за закрытые экзамены ISTQB или подтверждённые вопросы конкретных компаний Израиля.

## Запуск
Скачать актуальный `main` целиком, открыть `prototype/lesson.html`. Рядом должны быть `lesson.css`, `lesson.js`, `sql-foundations.js`, `tutor-feedback.js`, `interview-language.js`. Старые файлы на компьютере автоматически не обновляются.

Либо из корня проекта: `python -m http.server 8765 --bind 127.0.0.1 --directory prototype`, затем `http://127.0.0.1:8765/lesson.html`.

Ответы сохраняются в localStorage этого браузера. После смены пути локального файла может использоваться другое место хранения. Идентификаторы и правильные ответы редакции 2 сохранены; перевод и разбор не переоценивают старые ответы. Долговременное сохранение в среде пользователя ещё не проверено.

Нет серверной базы аккаунтов, AI-оценки свободного текста, исполнения произвольного Java/SQL или защищённого экзамена. В примерах SQL показаны заранее проверенные результаты. Эти ограничения относятся к текущей реализации, не к плану полной платформы.

## Проверки
Текущий целевой прогон трёх файлов тестов: **34 tests: 29 passed, 5 skipped**. Выполнялись реальные DOM-проверки в Chromium и SQL-примеры в SQLite. Навигация по HTTP заблокирована средой до загрузки приложения; проверки reload/storage поэтому не выданы за успешные. Подробности: [docs/LESSON-EN-RU-VERIFICATION.md](docs/LESSON-EN-RU-VERIFICATION.md).

В обычной среде с Playwright и Chromium: `python -m unittest discover -s tests -v`. Исторические отчёты: [SQL-REVIEW](docs/SQL-REVIEW.md), [VERIFICATION](docs/VERIFICATION.md). Они не являются проверкой текущего приложения.

## Skills и разработка
В `.agents/skills/` сохранены проектные адаптации frontend-design, web-design-guidelines, webapp-testing, systematic-debugging, verification-before-completion и координатор qa-academy-development. Это не полные upstream-пакеты; установка инструкций не устанавливает Python, Java или браузеры. Лицензии и источники: [docs/SKILLS.md](docs/SKILLS.md). Проверка структуры: `python tools/check_skills.py`.

Перед учебными изменениями читать [TEACHING-STANDARD](docs/TEACHING-STANDARD.md) и AGENTS.md. Браузерные JS-файлы обслуживают интерфейс; учебный язык автоматизации — **Java, не JavaScript**. Все записи GitHub — только через `VYCHESLAV1988`, в этот репозиторий, без force push. Не коммитить личную базу, пароли, токены или историю ученика.

Целевая архитектура: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). Статус skills: [docs/INSTALLATION-STATUS.md](docs/INSTALLATION-STATUS.md).
