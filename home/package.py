from pathlib import Path
import hashlib,json,zipfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
PACKAGE=ROOT/'StudyFlowApp-home'
files=sorted(p for p in PACKAGE.rglob('*') if p.is_file())
changed={str(p.relative_to(PACKAGE)) for p in files}
before=json.loads((ROOT/'before.json').read_text())
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p in files:assert digest(p)==digest(PROJECT/p.relative_to(PACKAGE)),str(p)
for rel,sha in before.items():
    if rel not in changed:assert digest(PROJECT/rel)==sha,rel
checks=json.loads((ROOT/'verification.json').read_text())
for key in ['login_validation_and_home_transition','temporary_checkbox_feedback','register_validation_and_home_transition','small_screen_scrolling_and_fixed_navigation','emulator_settings_restored']:assert checks.get(key),key
lint=ET.parse(PROJECT/'app/build/reports/lint-results-debug.xml')
assert not [n for n in lint.iter('issue') if n.get('severity') in ['Error','Fatal']]
guide=['''# Home dashboard — главный экран StudyFlow

Экран уже добавлен в `C:\\Users\\admin\\AndroidStudioProjects\\StudyFlowApp`. Вручную переносить код сейчас не нужно. Ниже сохранены инструкция и полные версии файлов.

## 1. Анализ дизайна

На экране: дата и приветствие, уведомления, градиентная карточка недельного прогресса с кольцом 75%, ближайший дедлайн, две карточки приоритетов, сегодняшнее занятие и следующее занятие, кнопка «+», нижняя панель Home / Schedule / Tasks / Notes / Profile.

Иконки перенесены из SVG в Vector Drawable; используются существующие шрифты Inter. Фон — #F5F7FC. Вертикальный градиент — #273D86 → #4969E8 (55%) → #9672D6. Карточки и отступы соответствуют макету 390 × 1008. Строка состояния и панель жестов принадлежат Android; их значки и размеры отличаются от iOS-макета.

Содержимое прокручивается на небольшом экране. Нижняя навигация и кнопка «+» закреплены. Текстовые блоки могут увеличиваться при увеличении системного шрифта.

## 2. Какие файлы нужны

Созданы HomeActivity.kt, activity_home.xml, home_strings.xml, home_styles.xml, XML-фоны, векторные иконки и два PNG-ресурса теней. Из существующих файлов изменены только AndroidManifest.xml, LoginActivity.kt и RegisterActivity.kt. Остальные экраны и ресурсы сохранены. Предыдущие версии трёх изменённых файлов находятся в папке `backup` рядом с инструкцией.

## 3. Пошаговая инструкция

1. В Android Studio открой **File → Open** и выбери `C:\\Users\\admin\\AndroidStudioProjects\\StudyFlowApp`, если этот проект ещё не открыт.
2. Дождись завершения синхронизации Gradle.
3. Выбери конфигурацию **app** и эмулятор или подключённый телефон.
4. Нажми зелёную кнопку **Run ▶**.
5. Перейди с onboarding на **Log In**. Введи любой тестовый email и пароль минимум из 8 символов. Нажми **Log In** — откроется Home.
6. Второй путь: **Create an account**, заполни имя, email, пароль и университет, установи галочку согласия. Нажми **Create Account** — откроется тот же Home.

Пока это демонстрационный переход после локальной проверки полей, без создания аккаунта и обращения к серверу. Имя Aruzhan, дата, задачи и проценты взяты из макета и пока не меняются по введённым данным. Галочки задач можно переключать для проверки внешнего вида; они не сохраняются в базе и не пересчитывают прогресс. Уведомления, «+», See all, 4 classes и остальные вкладки пока показывают только реакцию на нажатие. Системная кнопка «Назад» возвращает к форме.

## 4. Готовый код

Полный код приведён ниже с абсолютными путями. Если потребуется перенести изменения вручную, используй архив StudyFlowApp-home.zip: внутри сохранены пути относительно корня проекта. Он содержит только файлы этого этапа.

Для нового Kotlin-файла: в пакете `com.example.studyflowapp` нажми правой кнопкой → **New → Kotlin Class/File → File**, введи **HomeActivity** и вставь код. Для нового XML-файла в указанной папке `res` выбери **New → Android Resource File**, задай имя без `.xml` и тип **Layout**, **Drawable** или **Values**, соответствующий папке. В каждом файле полностью замени содержимое кодом из инструкции. PNG-файлы скопируй из архива в `res/drawable-xxhdpi`; их нельзя вставлять как XML.

Папка `values-v28` содержит настройку высоты строки для Android 9 и новее. При ручном переносе создай её через **res → New → Android Resource Directory → Resource type: values → Version → API level: 28**. Базовый файл в `values` нужен тоже: он обеспечивает совместимость с Android 7–8. Папку `drawable-xxhdpi` при необходимости создай через тот же пункт, выбрав **Drawable → Density → XX-High Density**. При копировании архива эти папки уже подготовлены.
''']
for p in files:
    rel=p.relative_to(PACKAGE)
    guide.append(f'### `{PROJECT/rel}`\n\nДействие: '+('заменить содержимое существующего файла.' if str(rel) in before else 'создать файл по указанному пути.'))
    if p.suffix=='.png':guide.append('Скопировать готовое изображение из архива без переименования.');continue
    lang='kotlin' if p.suffix=='.kt' else 'xml'
    guide.append(f'```{lang}\n{p.read_text(encoding="utf-8").rstrip()}\n```')
guide.append('''## 5. Проверка

Сборка assembleDebug и lintDebug завершились без ошибок. В эмуляторе проверены переходы из обеих форм, блокировка Log In при коротком пароле, блокировка регистрации без согласия, переключение галочки задачи, прокрутка и закреплённая навигация на небольшом экране. Настройки размера экрана и шрифта после проверки восстановлены.

Для сравнения с Figma сохранён Home-390x1008.png. Дополнительно сохранены Home-small-top-font130.png и Home-small-bottom-font130.png для экрана 360 × 640 dp со шрифтом 130%. Lint оставляет рекомендации о небольших размерах текста из макета и сложности иерархии; ошибок компиляции и Lint нет.

При запуске ты должна увидеть свой splash и onboarding, а после заполнения Login или Register — Home с синим градиентом, кольцом 75%, двумя задачами и нижним меню. Если внешний вид на твоём телефоне отличается, пришли скриншот для сравнения.
''')
(ROOT/'Home-инструкция-и-код.md').write_text('\n\n'.join(guide),encoding='utf-8')
with zipfile.ZipFile(ROOT/'StudyFlowApp-home.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(PACKAGE))
print(f'{len(files)} files packaged; {len(before)-len(changed.intersection(before))} existing files unchanged. Guide ready.')
