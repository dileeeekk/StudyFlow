from pathlib import Path
import hashlib
import json
import zipfile
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
PACKAGE=HERE/'StudyFlowApp-classes'
files=sorted(p for p in PACKAGE.rglob('*') if p.is_file())
checks=json.loads((HERE/'verification.json').read_text(encoding='utf-8'))
for key in ['forward_navigation','back_navigation','forward_after_back','last_page_cta_feedback_only','small_screen_actions_reachable']:
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

body=['''# StudyFlow — третий экран «Never Miss a Class»

## 1. Анализ дизайна

Это второй шаг onboarding и третий экран приложения после Splash и
«Track Every Deadline». Основа — ваш SVG 390 × 844 и PNG 1026 × 840.
Иллюстрация скопирована без изменений. Тексты, карточки и кнопки остаются
отдельными Android Views в XML.

Сохраняются боковые поля 24dp, карточка 342 × 332 с радиусом 30dp,
полупрозрачная подпись, заголовок Inter Bold 32sp, описание Inter 14sp,
кнопка высотой 52dp с радиусом 14dp и цветом #4564ED. Все общие фоны,
шрифты, цвета, иконка стрелки и тень кнопки используются из предыдущего этапа.

Отличия нового экрана:

- Иллюстрация расписания с меткой места.
- Подписи «Right class. Right place.» и «Calculus II · Room B-204».
- Плашка шага 02 шириной 208dp.
- Заголовок «Never Miss a Class» и новые две строки описания.
- Средний индикатор активен: ширина 26dp; крайние — по 7dp.

## 2. Какие файлы нужны

Папка проекта: `C:\\Users\\admin\\AndroidStudioProjects\\StudyFlowApp`.
Изменён только существующий `OnboardingActivity.kt`. Добавлены три файла:
разметка, строки и иллюстрация. Манифест, MainActivity, исправление Splash,
Gradle и ресурсы первого onboarding не менялись.

''']
for p in files:
    rel=p.relative_to(PACKAGE)
    body.append(f'- [{rel.as_posix()}](<{(PROJECT/rel).as_posix()}>)\n')

body.append('''
Одна OnboardingActivity показывает соответствующий XML по номеру страницы,
переданному через Intent. Этот номер сохраняется при пересоздании Activity.
При переходе предыдущий экран остаётся в стандартном стеке Android, поэтому
системная кнопка «Назад» возвращает на первый onboarding. Повторное быстрое
нажатие Get Started не должно создавать несколько копий следующего экрана.

## 3. Пошаговая инструкция

Файлы уже установлены в проект. Копировать код повторно не нужно.

1. Откройте **StudyFlowApp** в Android Studio.
2. Вверху выберите **app** и **Medium Phone API 37.0**.
3. Нажмите **Run ▶**.
4. После Splash появится «Track Every Deadline».
5. Нажмите **Get Started** — откроется «Never Miss a Class».
6. Нажмите системную кнопку или выполните жест **Назад** для возврата на первый экран.

Для просмотра XML откройте **app → res → layout → activity_onboarding_classes.xml**
и выберите **Split**. Kotlin-код находится в **app → kotlin+java →
com.example.studyflowapp → OnboardingActivity**.

Переход по Get Started на первом экране временно используется для просмотра
готовых макетов. На втором onboarding кнопки Get Started, Skip и Log In пока
дают только визуальную реакцию. Следующие переходы подключим после получения
соответствующих макетов. Свайпы между страницами пока не добавлены.

Если потребуется ручное восстановление, архив `StudyFlowApp-classes.zip`
содержит только изменения этого этапа и применяется поверх готового проекта
с предыдущими экранами. Папка `app` в архиве соответствует папке `app` проекта.

## 4. Готовый код

''')
for p in files:
    rel=p.relative_to(PACKAGE)
    body.append(f'### {p.name}\n\n**Полный путь:** `{PROJECT/rel}`\n\n')
    if p.suffix=='.png':
        body.append('**Действие:** скопировать PNG из архива в папку `res/drawable-xxhdpi`. Если папки нет, создать её. Имя файла должно быть `onboarding_classes_illustration.png`. Вручную вводить код изображения не нужно.\n\n')
    else:
        if p.suffix=='.kt':
            action='Открыть существующий файл, удалить старое содержимое и вставить полный код ниже.'
        elif 'layout' in p.parts:
            action='В папке res/layout создать Layout Resource File с именем activity_onboarding_classes.xml и вставить полный код ниже.'
        else:
            action='В папке res/values создать Values Resource File с именем onboarding_classes_strings.xml и вставить полный код ниже.'
        body.append(f'**Действие:** {action}\n\n')
        language='kotlin' if p.suffix=='.kt' else 'xml'
        body.append(f'```{language}\n{p.read_text(encoding="utf-8")}\n```\n\n')

body.append(f'''## 5. Проверка

- `assembleDebug` и `lintDebug` выполнены успешно: ошибок {len(errors)}, предупреждений {len(warnings)}.
- Запуск приложения и переход с первого onboarding на второй проверены на API 37.
- Проверены возврат назад и повторный переход вперёд.
- При смене размера эмулятора второй экран сохраняется.
- При 390 × 844dp карточка занимает x=24, y=116, ширину 342, высоту 332;
  плашка занимает x=24, y=474, ширину 208, высоту 22.
- При 360 × 640dp и шрифте 130% Get Started и Log In доступны после прокрутки.
- Размер, плотность и масштаб текста эмулятора после проверки восстановлены.
- Контрольные суммы {len(protected)} других файлов исходников совпали с состоянием
  до этого этапа. Это включает исправленный MainActivity и тему запуска Splash.

Отдельного запуска на API 24 не было: совместимость с минимальной версией
проверена сборкой и Lint. Системные часы, значки и жестовая полоска принадлежат
Android и могут отличаться от нарисованных в Figma.

Предупреждения Lint:

''')
for i in warnings: body.append(f'- `{i.get("id")}`: {i.get("message")}\n')
body.append('''
Предупреждения SmallSp относятся к размерам 10sp, заданным в ваших макетах.
Эти размеры сохранены. Новые зависимости и обновления инструментов не добавлялись.

Снимки результата находятся рядом с инструкцией:

- `Never-Miss-a-Class-390x844.png` — размер макета, снимок в масштабе 3×.
- `Never-Miss-a-Class-emulator.png` — обычные настройки вашего эмулятора.
- `Never-Miss-a-Class-small-font130.png` — небольшой экран с увеличенным текстом.
''')
guide=HERE/'StudyFlow-Never-Miss-a-Class-инструкция.md'
guide.write_text(''.join(body),encoding='utf-8')
with zipfile.ZipFile(HERE/'StudyFlowApp-classes.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files: z.write(p,p.relative_to(PACKAGE))
    z.write(guide,guide.name)
summary={'installed_files':len(files),'protected_files_unchanged':len(protected),'lint_errors':len(errors),'lint_warnings':len(warnings)}
(HERE/'delivery-check.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary))
