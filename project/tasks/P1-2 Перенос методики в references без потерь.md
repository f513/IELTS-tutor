---
type: task
id: P1-2
phase: 1
status: готово
priority: высокий
updated: 2026-10-14
tags: [ielts/task]
---
# P1-2 Перенос методики в references без потерь

Сейчас методика продублирована: `.claude/agents/ielts-<skill>.md` и `.claude/skills/ielts-tutor/references/<skill>.md`. Слить в один источник — references — и сделать их самодостаточными (без ссылок на `data/analysis/`).

**Готово, когда:** чек-лист named-техник и «неподтверждённых» фреймворков из старых файлов полностью найден в новых references.

## Результат
4 субагента слили агент + справочник в один `references/<навык>.md`. Чек-листы сохранённых пунктов: [[project/merge-checklists/reading|Reading]] (89) · [[project/merge-checklists/listening|Listening]] (82) · [[project/merge-checklists/speaking|Speaking]] (105) · [[project/merge-checklists/writing|Writing]] (99). Автопроверка: все named-техники и неподтверждённые фреймворки на месте, у каждого пункта есть раздел. Конфликты решены по `data/analysis/`.

← [[project/Roadmap|Roadmap]] · [[00 Дашборд|Дашборд]]
