# Туман и кости

Производственная ветка Godot. Этап 0 открывает главное меню, настройки, справочник и запись первого отряда. В меню «Новая партия» выбери двух героев, введи зерно и нажми «Начать партию». «Продолжить» восстанавливает партию с диска. Окно игры поддерживает клавиатуру, мышь и возврат по Esc.

## Запуск на Windows

На компьютере владельца проверен **Godot 4.7.2.stable.official.ed1daf0bf**, стандартная сборка Windows x64. Рендерер GL Compatibility. В менеджере проектов импортируй `godot/project.godot` из ветки `godot-stage-0` и нажми F6 для отдельной открытой сцены или F5 для запуска игры с меню. Команды ниже выполняются в каталоге `godot` из PowerShell.

```powershell
$engine = "$env:USERPROFILE\Desktop\Godot_v4.7.2-stable_win64.exe"
& $engine --version
& $engine --headless --editor --import --path .
& $engine --path .
```

## Данные и проверки

Снимок веб-эталона — [prototype-1.0, b07f194](https://github.com/Ligalug/Game/tree/b07f1941692c605ff76a061647874bc42b00bd75/). Три дизайн-документа и семь JS-файлов идентифицируются по Git blob SHA в `data/catalog.json`. Генератор выполняет исходные JS-функции в Node.js и сохраняет значения, названия и образцы расчётов. Воспроизведение каталога требует того же снимка веб-файлов. Папка выше проекта в этой ветке содержит эти исходники.

```powershell
node tools/reference.mjs .. --check
& $engine --headless --path . -s addons/gut/gut_cmdln.gd -gdir=res://tests -gexit
& $engine --path . --script res://tools/check_ui.gd -- --evidence
```

Тестовый модуль GUT 9.6.1 включён в репозиторий целиком, Git-ревизия `c80954f47bed74a0a2c471d472c0389f98e0a8f6`. Последняя команда проверяет переключение режима реального окна, изменение громкости и скорости, десять циклов создания партии, подтверждение замены сохранения, возврат в меню, загрузку и семь разделов справочника. В обычном режиме Windows файлы лежат в `%APPDATA%\FogAndBones\Kingdom`. Служебный флаг `--evidence` изолирует каждую проверку от игровой партии.

## Сохранения

`campaign.json`, формат 1, хранит начальное зерно, текущее 32-битное состояние игрового генератора, номер хода и индексы двух героев в закреплённом стартовом пуле. Поддерживаются ручная запись, автоматическая запись при старте и восстановление предыдущей записи из `.bak`. Новую игру поверх занятого слота нужно подтвердить. Неизвестная будущая версия даёт сообщение в игре. Параметры окна, микшера и анимаций хранятся отдельно в `preferences.json`. До появления глобальной карты летопись показывает созданный отряд.

## Запись видео

```powershell
$env:FOG_EVIDENCE_DIR = (New-Item -Force -ItemType Directory "$env:TEMP\fog-review").FullName
& $engine --path . --fixed-fps 24 --write-movie "$env:FOG_EVIDENCE_DIR\foundation.avi" --script res://tools/record_menu.gd -- --evidence
```

[Видео и кадры](docs/review/stage-0/README.md) · [Этапы](docs/ROADMAP.md) · [Последняя сессия](docs/PROGRESS.md) · [Вопросы](docs/OPEN_QUESTIONS.md) · [Графика](docs/ART_STYLE.md) · [Звук](docs/AUDIO.md) · [Лицензии](assets/LICENSES.md).

