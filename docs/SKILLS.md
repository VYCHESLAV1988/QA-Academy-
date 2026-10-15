# Skills для QA Academy

Проверено по skills.sh и исходным SKILL.md 15 октября 2026 года.
Это навыки разработчика/Codex, а не вопросы для ученика и не отдельные сервисы приложения.

| Skill | Автор | Роль |
|---|---|---|
| frontend-design | anthropics/skills | Экран урока, композиция, типографика, понятные действия |
| web-design-guidelines | vercel-labs/agent-skills | Доступность, формы, фокус, адаптивность |
| webapp-testing | anthropics/skills | Настоящие проверки интерфейса через Playwright |
| systematic-debugging | obra/superpowers | Причина сбоя до исправления |
| verification-before-completion | obra/superpowers | Утверждения о готовности только после проверок |

## Проверенные источники
- https://skills.sh/anthropics/skills/frontend-design
- https://skills.sh/vercel-labs/agent-skills/web-design-guidelines
- https://skills.sh/anthropics/skills/webapp-testing
- https://skills.sh/obra/superpowers/systematic-debugging
- https://skills.sh/obra/superpowers/verification-before-completion
- https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md
- https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md
- https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/web-design-guidelines/SKILL.md
- https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
- https://raw.githubusercontent.com/obra/superpowers/main/skills/systematic-debugging/SKILL.md
- https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/verification-before-completion/SKILL.md
- https://developers.openai.com/codex/skills
- https://github.com/vercel-labs/skills#readme

## Что сделано, а что нет
Полные инструкции перечисленных skills прочитаны и применены при создании и проверке prototype/lesson.html.
В .agents/skills/qa-academy-development/ добавлен собственный проектный skill: он задаёт процесс выбора и применения этих источников.
Исходные сторонние пакеты НЕ установлены на компьютере пользователя и НЕ включены в эту поставку. Сетевой доступ из рабочей среды для npx отсутствовал. Не объявлять подготовленные команды выполненной установкой.

## Установка оригиналов в среде Codex с интернетом
Запускать из корня репозитория после проверки источников. Команды используют проектную область, не глобальную.

```sh
npx skills add anthropics/skills --skill frontend-design webapp-testing --agent codex --copy
npx skills add vercel-labs/agent-skills --skill web-design-guidelines --agent codex --copy
npx skills add obra/superpowers --skill systematic-debugging verification-before-completion --agent codex --copy
npx skills list --agent codex
```

Не добавлять --all. Установка может запросить подтверждение и требует Node.js/npx. До выполнения вспомогательных скриптов просмотреть их действия и лицензии. После установки проверить пути .agents/skills, сохранить созданный CLI lock-файл, записать фактические версии/хэши и просмотреть git diff. Автообновления не включать. Эти команды не являются lock-файлом и не обещают неизменность будущего upstream.

Для запуска собственного проектного workflow в Codex: `$qa-academy-development`.

## Применение в текущем изменении
frontend-design: спокойный учебный экран, базовый текст 17 px, отдельный пример и таблица, минимальное декоративное движение.
web-design-guidelines: семантические кнопки, label/radio, visible focus, aria-live feedback, мобильная ширина, подтверждение очистки, уважение reduced-motion.
webapp-testing: проверены реальные клики, неверные ответы, отсутствие выбора, повторное нажатие, подсказка, повтор ошибок и клавиатура.
systematic-debugging: выявлена блокировка навигации браузера средой; защитные политики не менялись. Доступный DOM-only режим отмечен отдельно.
verification-before-completion: результаты и ограничения записаны в docs/VERIFICATION.md, без приписывания пропущенных тестов к успешным.
