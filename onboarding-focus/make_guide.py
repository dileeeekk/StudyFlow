from pathlib import Path
from collections import Counter
import hashlib
import json
import zipfile
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
PACKAGE=HERE/'StudyFlowApp-focus'
files=sorted(p for p in PACKAGE.rglob('*') if p.is_file())
checks=json.loads((HERE/'verification.json').read_text(encoding='utf-8'))
for key in ['forward_through_all_pages','back_through_all_pages','forward_after_back','final_cta_feedback_only','small_screen_actions_reachable']:
    assert checks[key],key
assert all(checks['settings_restored'].values())
protected=json.loads((HERE/'protected-files.json').read_text(encoding='utf-8'))
for rel,digest in protected.items():
    assert hashlib.sha256((PROJECT/rel).read_bytes()).hexdigest()==digest,rel
for p in files:
    assert p.read_bytes()==(PROJECT/p.relative_to(PACKAGE)).read_bytes(),p
    if p.suffix=='.xml': ET.parse(p)
lint=ET.parse(PROJECT/'app/build/reports/lint-results-debug.xml')
errors=[i for i in lint.findall('issue') if i.get('severity') in ('Error','Fatal')]
warnings=[i for i in lint.findall('issue') if i.get('severity')=='Warning']
assert not errors

body=['''# StudyFlow — четвёртый экран «Make Time Work for You»

## 1. Анализ дизайна

Это третий шаг onboarding и четвёртый экран приложения с учётом Splash.
Ваш SVG имеет размер **390 × 859**, тогда как предыдущие onboarding-макеты —
390 × 844. Увеличенную высоту и переносы текста учли при вёрстке.

Использована ваша иллюстрация часов с книгами, PNG 1026 × 840 без изменений.
Тексты, карточка-пример, индикаторы и кнопки созданы отдельными Android Views.
Повторно используются Inter, цвета, фоны, стрелка и тень кнопки из предыдущих экранов.

| Элемент | Параметры |
|---|---|
| Боковые поля | 24dp |
| Карточка иллюстрации | 342 × 332, радиус 30dp |
| Плашка шага | 03; 208 × 22 |
| Заголовок | Inter Bold 32sp; две строки; шаг строк 36sp |
| Описание | Inter Regular 14sp; три строки; шаг строк около 21sp |
| Индикаторы | 7, 7 и 26dp; активен третий |
| Get Started | 342 × 52 при ширине экрана 390dp; радиус 14dp |

Заголовок переносится после «for». В описании первая строка заканчивается
«Turn», вторая — «actually», третья содержит «reach.». На более узких экранах
или с увеличенным шрифтом разрешены дополнительные переносы и прокрутка.

## 2. Какие файлы нужны

Папка проекта: `C:\\Users\\admin\\AndroidStudioProjects\\StudyFlowApp`.
Изменён только `OnboardingActivity.kt`; добавлены разметка, строки и PNG.
Манифест, Gradle, предыдущие XML-экраны и исправленный Splash не менялись.

''']
for p in files:
    rel=p.relative_to(PACKAGE)
    body.append(f'- [{rel.as_posix()}](<{(PROJECT/rel).as_posix()}>)\n')

body.append('''
OnboardingActivity выбирает одну из трёх XML-разметок по номеру шага в Intent.
Get Started на первых двух шагах открывает следующий. На последнем шаге эта
кнопка пока даёт только реакцию на нажатие. Системная кнопка «Назад» возвращает
к предыдущему шагу. Номер текущей страницы сохраняется при пересоздании Activity.

## 3. Пошаговая инструкция

Изменения уже установлены. Вставлять код повторно не нужно.

1. В Android Studio откройте **StudyFlowApp**.
2. Выберите конфигурацию **app** и **Medium Phone API 37.0**.
3. Нажмите **Run ▶**.
4. После Splash появится «Track Every Deadline».
5. Нажмите **Get Started** — откроется «Never Miss a Class».
6. Нажмите **Get Started** ещё раз — откроется «Make Time Work for You».
7. Системной кнопкой или жестом **Назад** можно вернуться к предыдущим шагам.

Разметка находится в **app → res → layout → activity_onboarding_focus.xml**.
Для просмотра вместе с кодом выберите **Split**.
Kotlin-файл находится в **app → kotlin+java → com.example.studyflowapp → OnboardingActivity**.

Skip и Log In пока имеют только визуальную реакцию. Регистрация, авторизация,
сохранение данных и загрузка с сервера не добавлены. Свайпы между страницами
пока не подключены. Строка «9 of 12 hours» — демонстрационный текст из макета.

Архив `StudyFlowApp-focus.zip` содержит только четыре файла нового этапа:
он применяется поверх уже готового проекта с предыдущими экранами.

## 4. Готовый код

''')
for p in files:
    rel=p.relative_to(PACKAGE)
    body.append(f'### {p.name}\n\n**Полный путь:** `{PROJECT/rel}`\n\n')
    if p.suffix=='.png':
        body.append('**Действие:** скопировать PNG из архива в `res/drawable-xxhdpi` с именем `onboarding_focus_illustration.png`. Вручную вводить код изображения не нужно.\n\n')
    else:
        if p.suffix=='.kt':
            action='Открыть существующий файл, удалить старое содержимое и вставить весь код ниже.'
        elif 'layout' in p.parts:
            action='В res/layout создать Layout Resource File с именем activity_onboarding_focus.xml и вставить весь код ниже.'
        else:
            action='В res/values создать Values Resource File с именем onboarding_focus_strings.xml и вставить весь код ниже.'
        language='kotlin' if p.suffix=='.kt' else 'xml'
        body.append(f'**Действие:** {action}\n\n```{language}\n{p.read_text(encoding="utf-8")}\n```\n\n')

body.append(f'''## 5. Проверка

- `assembleDebug` и `lintDebug` завершились успешно: ошибок {len(errors)}, предупреждений {len(warnings)}.
- Приложение проверено в эмуляторе API 37.
- Проверены переходы через все три страницы onboarding, два возврата назад
  и повторные переходы вперёд.
- На размере 390 × 859dp проверены переносы текста и координаты:
  карточка — x=24, y=116, ширина 342, высота 332;
  плашка — x=24, y=474, ширина 208, высота 22;
  кнопка — x=24, y≈718, ширина 342, высота 52.
- На экране 360 × 640dp с текстом 130% Get Started и Log In доступны после прокрутки.
- После изменения размеров эмулятора сохраняется третий шаг onboarding.
- Исходные размер, плотность и масштаб текста эмулятора восстановлены.
- Контрольные суммы {len(protected)} остальных исходных файлов не изменились,
  включая MainActivity и тему исправленного Splash.

Отдельного запуска на API 24 не было; совместимость с minSdk 24 проверена
сборкой и Lint. Для межстрочного интервала применён совместимый атрибут
`app:lineHeight` существующего AppCompatTextView.

Предупреждения Lint:

''')
for code,count in Counter(i.get('id') for i in warnings).items():
    example=next(i.get('message') for i in warnings if i.get('id')==code)
    body.append(f'- `{code}` — {count}: {example}\n')
body.append('''
SmallSp относится к размерам 10sp из ваших макетов. Эти размеры сохранены,
как и версии зависимостей проекта. Предупреждения не препятствуют сборке.

Снимки рядом с инструкцией:

- `Make-Time-Work-for-You-390x859.png` — размер макета, снимок в масштабе 3×.
- `Make-Time-Work-for-You-emulator.png` — обычный размер вашего эмулятора.
- `Make-Time-Work-for-You-small-font130.png` — небольшой экран с увеличенным текстом.

Системные часы, значки и нижняя жестовая полоска отображаются Android и могут
отличаться от панелей iPhone, нарисованных в макете.
''')
guide=HERE/'StudyFlow-Make-Time-Work-for-You-инструкция.md'
guide.write_text(''.join(body),encoding='utf-8')
with zipfile.ZipFile(HERE/'StudyFlowApp-focus.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files: z.write(p,p.relative_to(PACKAGE))
    z.write(guide,guide.name)
summary={'installed_files':len(files),'protected_files_unchanged':len(protected),'lint_errors':len(errors),'lint_warnings':len(warnings)}
(HERE/'delivery-check.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary))
