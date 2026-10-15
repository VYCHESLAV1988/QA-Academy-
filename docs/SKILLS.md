# Skills — фактическая установка в проекте

Дата изменения: 2026-10-15.

## Что находится в репозитории
В `.agents/skills/` добавлены пять самодостаточных **проектных адаптаций** прочитанных skills с skills.sh. Это действующие SKILL.md с name/description, инструкциями и лицензиями, а не одни ссылки. Это **не побайтовые копии полных upstream-пакетов** и не результат выполненного `npx skills add`.

| Имя | Источник | Применение |
|---|---|---|
| frontend-design | anthropics/skills, Apache-2.0 | Читаемый учебный интерфейс |
| webapp-testing | anthropics/skills, Apache-2.0 | Playwright-проверки поведения |
| web-design-guidelines | vercel-labs/agent-skills, MIT | Доступность и удобство |
| systematic-debugging | obra/superpowers, MIT | Воспроизведение и причина дефекта |
| verification-before-completion | obra/superpowers, MIT | Доказательства перед заявлением о готовности |

Существующий `qa-academy-development` остаётся координатором. Итого в проекте шесть SKILL.md. Он должен читать локальные проектные версии выше; не считать их установленными глобально на компьютере пользователя.

Адаптации специально не ссылаются на отсутствующие локальные helper scripts: Playwright-тесты пишутся в tests/, а проверки выполняются доступными инструментами. Установка навыка не устанавливает браузер, Python, Java, Selenium или Playwright.

## Источники, прочитанные при подготовке
- https://skills.sh/anthropics/skills/frontend-design
- https://skills.sh/anthropics/skills/webapp-testing
- https://skills.sh/vercel-labs/agent-skills/web-design-guidelines
- https://skills.sh/obra/superpowers/systematic-debugging
- https://skills.sh/obra/superpowers/verification-before-completion
- https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md
- https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md
- https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/web-design-guidelines/SKILL.md
- https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
- https://raw.githubusercontent.com/obra/superpowers/main/skills/systematic-debugging/SKILL.md
- https://raw.githubusercontent.com/obra/superpowers/main/skills/verification-before-completion/SKILL.md
- https://developers.openai.com/codex/skills
- https://github.com/vercel-labs/skills

## Как использовать в Codex
Открыть актуальный checkout репозитория. Codex сканирует `.agents/skills` в корне и родительских папках проекта. Вызвать `$qa-academy-development` или конкретный `$frontend-design`, `$webapp-testing`, `$systematic-debugging` и т. д. Если новая версия не появилась в списке, перезапустить сессию Codex.

Это установка в GitHub-проекте. Наличие актуального checkout и обнаружение навыков на личном компьютере пользователя здесь не проверены. Не объявлять обратное.

## Полные оригинальные пакеты — отдельная необязательная установка
Команды ниже **не выполнялись** в этой сессии. Они нужны только если решено заменить проектные адаптации полными исходными пакетами. Сначала сохранить/сравнить текущие адаптации: возможна перезапись одноимённых папок. Не выполнять автоматически при запуске приложения.

```sh
npx skills add anthropics/skills --skill frontend-design webapp-testing --agent codex --copy
npx skills add vercel-labs/agent-skills --skill web-design-guidelines --agent codex --copy
npx skills add obra/superpowers --skill systematic-debugging verification-before-completion --agent codex --copy
npx skills list --agent codex
```

После такой установки проверить реальные файлы, вспомогательные скрипты, лицензии и diff. Не устанавливать весь каталог, не включать автообновления и не добавлять платные сервисы без разрешения. Источники могут измениться; существующие локальные адаптации зафиксированы историей этого репозитория.

## Границы
Skills помогают разработке, но не генерируют правильный учебный курс автоматически. Количество заданий, качество эталонов, доступность в интерфейсе и тестирование приложения проверяются отдельно. Предыдущий отчёт 11 passed / 3 skipped относится только к прежнему прототипу и не является проверкой нынешней установки или будущего курса.
