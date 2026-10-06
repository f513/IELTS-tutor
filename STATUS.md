# STATUS — читай это первым при возвращении к задаче

См. `PLAN.md` для полного плана и архитектуры. Этот файл — текущий срез:
что сделано, что в процессе, что дальше. Обновляется по ходу работы.

## Текущая стадия (2026-10-06): полный eval-цикл для Claude Skill ЗАВЕРШЁН, жду фидбек пользователя

Агентная архитектура (Task #1-7, разделы ниже) была готова раньше.
Пользователь затем попросил **"сгруппируй всё в skill для клода"** —
превратить `.claude/agents/ielts-*.md` в единый Claude Skill
`.claude/skills/ielts-tutor/` (SKILL.md + `references/{reading,listening,
speaking,writing}.md`), и прогнать **полный eval-цикл** (не лёгкое
тестирование) по методике skill-creator.

**Сделано в этой фазе:**
- `.claude/skills/ielts-tutor/SKILL.md` + 4 reference-файла — готовы, в репо.
- `.claude/skills/ielts-tutor/evals/evals.json` — 5 тест-кейсов (reading/
  matching-headings, listening-stuck-6.5, speaking-full-mock, writing-essay-
  grading, honesty-rule-ppf-method).
- Все 10 прогонов (5 evals × with_skill/without_skill) выполнены субагентами,
  сохранены в `.claude/skills/ielts-tutor-workspace/iteration-1/<eval-name>/
  {with_skill,without_skill}/outputs/response.md` + `timing.json`.
- **Градация пройдена инлайн** (не отдельным grader-субагентом — сам прочитал
  все 10 response.md против assertions из eval_metadata.json и записал
  `grading.json` в каждую директорию, строго по схеме skill-creator:
  `expectations[].{text,passed,evidence}` + `summary` + `timing` + `claims`
  + `eval_feedback`).
- `benchmark.json`/`benchmark.md` собраны **вручную** (не через
  `aggregate_benchmark.py` — скрипт ожидает layout `eval-N/with_skill/run-N/`,
  а у нас описательные имена папок без вложенного `run-N`; схема взята из
  `skill-creator/references/schemas.md`, провалидирован `json.load`).
- **Результат:** with_skill 100% pass rate (29/29 assertions) vs without_skill
  ~94% (27/29). Два реальных провала baseline: (1) reading-eval — baseline
  вообще отказался дать band-оценку по одному passage; (2) speaking-eval —
  baseline не предупредил ЗАРАНЕЕ (только в самом конце), что это
  текстовый формат и произношение не может быть оценено по-настоящему.
  На остальных 3 evals (listening/writing/honesty) оба прогона прошли все
  assertions — ассерты там не дискриминирующие относительно сильного
  baseline (see `eval_feedback` в соответствующих `grading.json` — там же
  предложения по усилению assertions на будущее, напр. проверка на
  упоминание именованных channel-фреймворков типа "100% Rule"/"Peacock
  vocabulary", а не только на корректность).
- `review.html` сгенерирован через `eval-viewer/generate_review.py --static`
  (headless-окружение, без браузера) и отправлен пользователю файлом.
- Всё закоммичено и запушено в `claude/clever-galileo-9k9c0v` (ветка была
  смержена с `origin/main` перед push — PR #2 на тот момент уже был смержен,
  см. раздел про divergence в истории коммитов).

**Следующий шаг (Task #12, pending):** ждать, когда пользователь посмотрит
`review.html`, оставит фидбек через встроенную форму (сохранится в
`feedback.json` при клике "Submit All Reviews" — в headless-режиме это
скачается как файл, нужно будет попросить пользователя прислать его обратно
или положить в workspace вручную). После фидбека — доработать SKILL.md/
reference-файлы (не переобучаясь только на этих 5 примерах!), при
необходимости перегнать evals в `iteration-2/`, и в конце — упаковать через
`scripts/package_skill.py` + финальный commit/push.

## 🎉 Проект завершён (2026-10-06)
- `.claude/agents/ielts-reading.md`, `ielts-listening.md`, `ielts-speaking.md`,
  `ielts-writing.md` — 4 агента-специалиста, построены на `data/analysis/*.md`.
- `.claude/agents/ielts-tutor.md` — главный оркестратор: делегирует специалистам
  через Task tool (или читает их файлы напрямую как fallback), умеет сам
  давать советы, создавать вопросы по всем 4 направлениям, оценивать
  writing/speaking, создавать+оценивать reading, объяснять listening
  (текстовый формат, т.к. аудио генерировать не может), и проводить
  полный мок-экзамен по всем 4 секциям с итоговым band estimate.
- Все честно помечают, что подтверждено каналом (с цитатами из реальных
  транскриптов), а что — общие IELTS-знания для восполнения пробелов.

**Как пользоваться:** в Claude Code с этим репозиторием — просто писать
запросы по IELTS, главный агент (`ielts-tutor`) должен подхватываться
автоматически для общих/межсекционных вопросов; для прямого вызова
конкретного специалиста это нормально сработает через обычный Task-вызов
Claude Code с именем агента.

## ✅ Уточнение анализов реальными транскриптами ЗАВЕРШЕНО (2026-10-06)
Все 4 файла `data/analysis/*.md` переписаны с учётом 8 реальных транскриптов.
Ключевые новые находки (ранее были только названы, механика неизвестна):
- **Reading**: точный алгоритм Matching Headings и True/False/Not Given.
- **Listening**: механика Maps/Multiple Choice/Sentence Completion стратегий;
  подтверждено, что table/note completion, matching, short-answer канал
  вообще нигде не разбирает (не только не описано — реально нет контента).
- **Speaking**: правило "systematic error" для грамматики (Band 6 vs 9),
  "100% rule" для словаря, реальные формулировки фидбека на 3 уровнях
  (6.5/7.5/8). Фреймворки PPF Method/9 Sentence Patterns по-прежнему НЕ
  подтверждены — не найдены ни в одном из 3 транскриптов.
- **Writing**: точные вердикты по популярным советам (что реально
  повышает/понижает балл), новые методики "Coffee Shop Method" и
  "100% Rule" для словаря. Family Fortunes Method всё ещё не раскрыт.

## 🎉 Пользователь прислал реальные транскрипты вручную (2026-10-06)
Zip с 8 .txt файлами (по timestamp-формату `[m:ss] текст`), разложенными по
папкам L/R/S/W. Все 8 успешно сопоставлены с видео по содержанию/длительности
и сохранены в `data/raw/subs/<id>.txt` + пересобраны в `data/videos/<id>.md`:

| Файл | Video ID | Название | Было в priority_videos.md? |
|---|---|---|---|
| L/1 | q7xCHfDRdug | The ONLY IELTS Listening Course You Need | да, #1 |
| R/1 | 3KDP8P-pvEw | How to Answer ANY IELTS Reading Question | да, #1 |
| R/2 | OtmUQwPVLko | The ONLY IELTS Reading Course You Need 2026 | да, #2 |
| S/1 | UpaYHuz1Aoc | IELTS Speaking Test with Feedback - Band 7.5 | да, #1 |
| S/2 | ZDv9njERj0s | IELTS Speaking Mock Test - Band 8 | да, #2 |
| S/3 | Ek9Lk8_bzeY | IELTS Speaking Test- Band 6.5 | бонус (не было в списке) |
| W/1 | 684xymRpBc0 | Every IELTS Writing Tip Explained in 39 Minutes | да, #2 |
| W/2 | p-r65jaSz4o | IELTS Writing Tips You MUST Know Before Your Test | да, #3 |

7 из 9 приоритетных + 1 бонус. Не хватает: Ox0M8W2HDJE (Reading,
Matching Headings short), UuNgt9Zjh4Y (Speaking, Band 8.5 vs 9),
ui08O7TbFKg (Writing, Family Fortunes Method) — все три очень короткие,
не критично.

**Важно:** если контекст сброшен и видишь это — проверь, не прислал ли
пользователь ЕЩЁ транскриптов (спроси). Raw .txt из upload лежат в
`data/raw/manual_uploads/` (gitignored, только локально в этом контейнере —
если контейнер пересоздастся, эти 8 .txt всё равно сохранены в
`data/raw/subs/*.txt` и встроены в `data/videos/*.md`, так что не потеряются,
но САМ исходный zip/upload — нет, не переживёт пересоздание контейнера).

**Следующий шаг:** уточнить 4 анализа (`data/analysis/*.md`) используя эти
8 реальных транскриптов — именно они закрывают места, помеченные как GAP
(механика Matching Headings/TFNG, полная программа Listening-курса,
формулировки фидбека на mock-тестах Speaking, рейтинг советов Writing).

## Итог этапов 1-3
- Метаданные (title+description+date): **421/421** — `data/raw/info/*.json`, собраны в `data/videos/*.md`.
- Транскрипты: **0/421**, недостижимы (см. раздел про капчу ниже). Пробовал 3 пути:
  YouTube напрямую, headless-браузер на YouTube, сторонний сайт
  downloadyoutubesubtitles.com (упёрся в Cloudflare Turnstile). Пользователь
  пока не выбрал финальный вариант (ждать / делать самому / идти без
  транскриптов) — **следующий, кто продолжает эту задачу, должен уточнить
  у пользователя, если дошло до анализа методологии и не хватает глубины.**
- Классификация: **421/421**, `needs_review` снижен с 99 до **8** после
  второго прохода с описаниями (2 субагента). Итоговое распределение:
  speaking 179, writing 108, general 92, reading 25, listening 17 (по
  разделам); advice 156, training 111, exam 87, tips 67 (по подтипам).
  ⚠️ Speaking/writing сильно доминируют — вероятно реальная специфика
  канала (много speaking mock-тестов и success-story шортсов), но держать
  в уме при анализе reading/listening (данных заметно меньше).
  Оставшиеся 8 needs_review — см. `data/classification.json` (обычно это
  видео, называющие 2 навыка сразу, или с пустым описанием).

## ⚠️ ВАЖНОЕ ОТКРЫТИЕ: верботим-транскрипты через автоматизацию недостижимы
Проверено headless Chromium (Playwright) + прямые HTTP-запросы к
`/api/timedtext`: все запросы к timedtext либо возвращают HTTP 200 с
ПУСТЫМ телом, либо при обычной навигации на watch-страницу отдают
буквальную HTML-форму reCAPTCHA (`recaptcha/enterprise`, `id="captcha-form"`).
Это не рейт-лимит, который можно переждать — это каптча, которую скрипт
не может пройти. Дальше это пробовать не имеет смысла (и не стоит —
это обход антибот-защиты).
**Решение:** `scripts/scrape.py` — выборка субтитров отключена
(`FETCH_TRANSCRIPTS = False`). Собираем только title + description +
publishDate — этого обычно достаточно (описания у канала развёрнутые,
с конкретными пунктами техники), но без точных цитат из речи.
Метаданные (watch-страница) продолжают скачиваться нормально — это НЕ
капча-стена, просто изредка (видимо) словит её же и уходит в cooldown.

**ФИНАЛЬНОЕ РЕШЕНИЕ (2026-10-06, после проверки ещё 2 сторонних сайтов):**
двигаемся дальше на title+description, транскрипты больше не добываем
автоматически. Пробовали 4 независимых пути — все упёрлись в защиту:
1. YouTube напрямую (HTTP) — капча/429 на общем IP окружения.
2. YouTube через headless-браузер — та же капча (reCAPTCHA).
3. downloadyoutubesubtitles.com — Cloudflare Turnstile, headless не проходит
   даже после 60+ сек ожидания (подтверждено повторной проверкой).
4. videotranscriber.ai — требует вход через Google-аккаунт после нажатия
   «Транскрибировать» (не капча, а registration/paywall gate) — это я не
   могу пройти за пользователя.
Если пользователь сам захочет скачать транскрипты вручную (свой браузер,
свой Google-аккаунт) и прислать файлы — можно будет доинтегрировать позже
без переделки остального пайплайна (просто положить .vtt/.txt в
data/raw/subs/<id>.* и перезапустить build_video_md.py + повторный анализ).

Доп. проверено по просьбе пользователя: en1.savefrom.net/113-youtube-transcript.html —
сайт реально пытается вытащить субтитры с YouTube на своём backend (не
капча), но стабильно отвечает "Something went wrong while fetching the
captions" (проверено дважды, в т.ч. со свежим HTML) — похоже на их
собственную серверную проблему, не связанную с нашим IP. Не рабочий путь.

**Как проверять (не чаще раза в 2-3 часа!):**
`python3 scripts/probe_transcripts.py` — один лёгкий тест (2 запроса:
watch-страница + один caption track). Если напечатает `SUCCESS` и создаст
`data/raw/transcripts_unblocked.flag` — значит блок снялся: открой
`scripts/scrape.py`, поставь `FETCH_TRANSCRIPTS = True`, перезапусти
скрапер (команда в разделе выше), подожди полного прогона (новый проход
по всем 421, но он пропустит уже существующие info.json — поэтому нужно
ещё и удалить старые info.json ИЛИ добавить отдельную логику добора только
субтитров для уже скачанных — это TODO, пока не делал, т.к. блок не снят).
Если напечатает что-то про `soft-blocked` / `BLOCKED` / `still blocked` —
блок всё ещё стоит, просто обновить дату последней проверки в этом файле
и подождать ещё.

**Последняя проверка:** 2026-10-06 ~03:50 UTC — всё ещё заблокировано.
Интересная деталь: теперь `playabilityStatus` в самом ответе плеера
явно говорит `LOGIN_REQUIRED` / "Sign in to confirm you're not a bot" —
то есть строгость блокировки колеблется (во время массового скрапинга
метаданных в основном проходило нормально, сейчас строже). Это
подтверждает, что это живая репутационная система Google, а не
статичный блок — технически ускорить нечем, только ждать.

**Контейнер может перезапускаться сам по себе** (однажды фоновый процесс
scrape.py умер без видимой причины, видимо из-за простоя контейнера) —
ВСЕГДА проверяй `ps aux | grep scrape.py` перед тем как ждать прогресса,
и перезапускай при необходимости (команда ниже, идемпотентно).

## Сделано
- [x] Канал определён: IELTS Advantage, @Ieltsadvantage, 421 видео (219 шортс <90с, 202 длинных).
- [x] Получен полный список видео (`data/raw/uploads.json`) через uploads playlist.
- [x] Обнаружена и диагностирована капча-блокировка Google на общем IP окружения
      (HTTP 302 → google.com/sorry). Пользователь выбрал стратегию "ждать и
      медленно повторять".
- [x] Написан `scripts/scrape.py` (durable, resumable, с долгим cooldown при
      блоке — 25 мин, повтор того же видео). Запущен в фоне (PID в
      `data/raw/scrape.pid`), сейчас в cooldown после первого блока.
- [x] Написан `scripts/build_video_md.py` (сборка data/videos/<id>.md).
- [x] PLAN.md / STATUS.md заведены.
- [x] Коммит + push в origin/claude/clever-galileo-9k9c0v сделан (scaffolding).
- [x] **Первая волна классификации по заголовкам готова для всех 421 видео.**
      6 параллельных subagent-ов классифицировали input_1..6.json →
      output_1..6.json. Смерджено скриптом `scripts/build_catalog.py` в
      `data/classification.json` + `data/catalog.md`.
      Распределение по разделам: speaking 172, general 122, writing 87,
      reading 24, listening 16. По подтипам: advice 162, training 110,
      exam 76, tips 73. **needs_review=true у 99 видео** (в основном короткие
      шортсы/истории успеха без явно названного навыка в заголовке — их
      нужно доуточнить по description/transcript после скрапинга, скрипт
      `build_catalog.py` просто перезапустить когда данные появятся — нужно
      доработать его логику уточнения, см. ниже).
      ⚠️ Распределение сильно смещено в сторону speaking/writing — это,
      вероятно, реальная специфика канала (много speaking-тестов как
      Shorts), но стоит перепроверить после уточнения needs_review.

## В процессе / далее
- [ ] **(новое)** Доработать уточнение needs_review: когда appear description/
      transcript в data/raw/info/*.json — для видео с needs_review=true
      перезапустить классификацию (subagent) уже с описанием/транскриптом,
      не только заголовком. Пока build_catalog.py НЕ делает этот второй проход
      автоматически — это TODO.
- [ ] Проверять `data/raw/scrape.log` на прогресс (`tail -40 data/raw/scrape.log`).
      Посчитать готовые файлы: `ls data/raw/info | wc -l` (из 421).
      **Если скрипт не жив (`ps aux | grep scrape.py` пусто) — перезапусти:**
      `cd /home/user/IELTS-tutor && nohup python3 scripts/scrape.py >> data/raw/scrape_stdout.log 2>&1 &`
      (resumable, пропускает уже скачанные id).
- [ ] Когда метаданные+транскрипты наберутся — прогнать `scripts/build_video_md.py`
      (идемпотентно, можно запускать многократно) и улучшить классификацию
      needs_review-видео по описанию/транскрипту.
- [ ] Анализ по разделам (Task #4) — 4 subagent-а, каждый читает видео своего
      раздела и пишет `data/analysis/<section>.md`.
- [ ] Создание 4 агентов-специалистов + оркестратора (Task #5, #6) в
      `.claude/agents/`.
- [ ] Commit & push (Task #7) — делать периодически, не только в конце.

## Важные решения/договорённости
- `data/raw/info/` и `data/raw/subs/` теперь в `.gitignore` (слишком много
  мелких файлов — по одному на видео, коммитить каждый по отдельности не
  нужно). Источник правды, который коммитим — `data/videos/<id>.md`
  (собирается из raw через `scripts/build_video_md.py`) и `data/catalog.md`/
  `data/classification.json`. Raw-данные при потере контейнера придётся
  перескачать (scrape.py resumable, но под текущей блокировкой это небыстро) —
  поэтому периодически гонять `build_video_md.py` и коммитить `data/videos/`,
  не дожидаясь 100% скрапинга.
- Пользователь просил: собрать весь канал → разложить на Reading/Listening/
  Speaking/Writing × (training/exam/advice/tips) → анализ → 4 агента-
  специалиста + 1 оркестратор над ними с конкретными способностями (см.
  PLAN.md, раздел "Главный агент").
- Транскрипты качаем только для видео длиннее 90 секунд (шортсы — только
  метаданные), чтобы не плодить лишние запросы под блокировкой.
- Все промежуточные скрипты и данные живут в репозитории (`scripts/`,
  `data/raw/`), а не в scratchpad — scratchpad не переживает новую сессию,
  репозиторий переживает.

## Если контекст сбросился — что делать
1. Прочитать этот файл и `PLAN.md`.
2. Проверить, жив ли фоновый процесс: `ps aux | grep scrape.py`.
3. Проверить прогресс: `ls data/raw/info | wc -l`, `tail -40 data/raw/scrape.log`.
4. Если процесс не жив и есть недоскачанные видео — перезапустить (команда выше).
5. Продолжить с первого невыполненного пункта в разделе "В процессе / далее".
