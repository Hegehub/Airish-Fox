# Как восстановиться, если `git pull` дал конфликты

Этот документ нужен для ситуации, когда локальная копия `Airish-Fox` уже содержит часть Django-файлов, а при `git pull` Git показывает конфликтные файлы и не даёт продолжить работу.

## 1. Сначала посмотрите текущее состояние

```bash
git status
```

Если в выводе есть `You have unmerged paths`, значит Git находится в середине merge/rebase и ждёт, пока конфликтные файлы будут либо приняты, либо вручную исправлены и добавлены через `git add`.

Список конфликтных файлов:

```bash
git diff --name-only --diff-filter=U
```

## 2. Если локальные изменения НЕ нужно сохранять

> Внимание: команда ниже удалит незакоммиченные локальные изменения.

```bash
git merge --abort || git rebase --abort || true
git fetch origin
git reset --hard origin/main
```

Если основная ветка называется не `main`, посмотрите ветки:

```bash
git branch -a
```

и замените `origin/main` на нужную ветку, например `origin/master`.

## 3. Если локальные изменения нужно сохранить

Создайте страховочную ветку и stash:

```bash
git branch backup/before-conflict-resolution
git stash push -u -m "backup before resolving Airish Fox pull conflicts"
```

Остановите незавершённый merge/rebase и подтяните актуальную ветку:

```bash
git merge --abort || git rebase --abort || true
git pull --rebase
```

Верните свои изменения:

```bash
git stash pop
```

Если после `stash pop` снова появились конфликты, переходите к разделу ручного разрешения.

## 4. Быстро принять версию из удалённой ветки для конфликтных файлов

Если нужно принять версию, которая пришла из `pull`, для всех конфликтных файлов:

```bash
git diff --name-only --diff-filter=U | xargs git checkout --theirs --
git diff --name-only --diff-filter=U | xargs git add
git commit -m "Resolve pull conflicts using incoming Airish Fox version"
```

## 5. Быстро оставить локальную версию для конфликтных файлов

Если нужно оставить локальную версию для всех конфликтных файлов:

```bash
git diff --name-only --diff-filter=U | xargs git checkout --ours --
git diff --name-only --diff-filter=U | xargs git add
git commit -m "Resolve pull conflicts using local Airish Fox version"
```

## 6. Ручное разрешение конфликтов

Откройте каждый файл из списка:

```bash
git diff --name-only --diff-filter=U
```

Найдите маркеры:

```text
<<<<<<< HEAD
локальная версия
=======
версия из pull
>>>>>>> branch-name
```

Оставьте нужный код, удалите строки `<<<<<<<`, `=======`, `>>>>>>>`, затем выполните:

```bash
git add path/to/conflicted-file
```

Когда все файлы добавлены:

```bash
git status
git commit
```

## 7. Проверка после разрешения конфликтов

После успешного merge/rebase проверьте проект:

```bash
python -m pip install -r requirements.txt
python manage.py check
python manage.py test
python manage.py migrate
```

Если зависимости уже установлены, первую команду можно пропустить.

## 8. Типичные причины конфликтов в этом проекте

- локально уже были созданы Django-файлы, а pull принёс файлы с теми же путями;
- локальная ветка отстала от удалённой;
- одновременно менялись шаблоны, настройки или миграции;
- merge был начат, но конфликтные файлы не были добавлены через `git add` после исправления.

## 9. Что отправить разработчику, если конфликт не получается закрыть

Скопируйте вывод команд:

```bash
git status
git diff --name-only --diff-filter=U
git branch -vv
```

и приложите 1–2 конфликтных файла с маркерами `<<<<<<<`, `=======`, `>>>>>>>`.
