from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
PACKAGE=ROOT/'StudyFlowApp-register'
files=sorted(p for p in PACKAGE.rglob('*') if p.is_file())
changed={str(p.relative_to(PACKAGE)) for p in files}
before=json.loads((ROOT/'before.json').read_text())
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p in files:assert digest(p)==digest(PROJECT/p.relative_to(PACKAGE))
protected=[rel for rel in before if rel not in changed]
for rel in protected:assert digest(PROJECT/rel)==before[rel],rel
for p in files:
    if p.suffix=='.xml':ET.parse(p)
lint=ET.parse(PROJECT/'app/build/reports/lint-results-debug.xml')
assert not [i for i in lint.iter('issue') if i.get('severity') in ['Error','Fatal']]
checks=json.loads((ROOT/'verification.json').read_text())
for key in ['six_fields_empty','inputs_and_password_toggle','agreement_toggle','navigation_and_no_authentication','small_screen_actions_reachable','settings_restored']:assert checks[key],key
guide=['''# StudyFlowApp — Register

## 1. Анализ дизайна

Экран реализован по Register.svg размером 390×929: фон #F5F7FC, стрелка назад, Create account, заголовок A fresh start, in flow., описание и белая карточка со скруглением 22 dp. Поля имеют высоту 52 dp. Year и Group расположены в одной строке. Под карточкой — чекбокс, Create Account и ссылка Log In.

По твоей просьбе все шесть полей изначально пустые: Full name, University email, Password, University, Year и Group. Под паролем оставлена согласованная подпись At least 8 characters. Она не является проверкой надёжности пароля.

Иконки email, глаза, стрелки кнопки, фон полей, фон карточки, шрифты Inter и базовые стили переиспользованы из Login/onboarding. Системные часы, значки и нижняя полоса жестов отображаются Android; их оформление зависит от устройства.

## 2. Какие файлы нужны

Экран уже установлен в проект. Вручную вставлять код сейчас не требуется.

Из существующих файлов изменены только LoginActivity.kt (переход по Create an account) и AndroidManifest.xml (регистрация новой Activity). Остальные перечисленные ниже файлы созданы для Register:
''']
for p in files:
    rel=p.relative_to(PACKAGE);status='изменён' if str(rel) in before else 'создан'
    guide.append(f'- `{PROJECT/rel}` — {status}.')
guide.append('''
## 3. Пошаговая инструкция

1. Открой Android Studio и проект `C:\\Users\\admin\\AndroidStudioProjects\\StudyFlowApp`.
2. Выбери конфигурацию **app** и эмулятор, нажми зелёную кнопку **Run ▶**.
3. После splash открой **Log In** на onboarding.
4. Внизу Login нажми **Create an account**. Откроется новая регистрация.
5. Проверь, что все поля пустые. В Full name, University email и Password можно вводить текст. Значок глаза показывает и скрывает введённый пароль.
6. Чекбокс согласия переключается. Его начальное состояние отмечено, как на макете. Create Account пока закрывает клавиатуру и остаётся на экране — аккаунт не создаётся.
7. University, Year и Group пока воспроизводят внешний вид выбора со стрелками и реакцией на нажатие. Списки вариантов и логика выбора не добавлены, поскольку их содержимое и макеты ещё не заданы.
8. Стрелка сверху, системная кнопка «Назад» и нижняя ссылка **Log In** возвращают на Login. При открытой клавиатуре системная кнопка «Назад» сначала закрывает её.

Текст Terms of Service и Privacy Policy пока только оформлен цветом, как в макете; страницы документов и их адреса не заданы. База данных, регистрация, запросы, сохранение профиля и проверка пароля не добавлялись.

Для переноса в копию этого же проекта распакуй StudyFlowApp-register.zip и скопируй его папку app в корень проекта, объединив папки. Архив содержит только файлы этого этапа и требует существующие ресурсы Login/onboarding. Резервные копии двух изменённых файлов находятся в папке backup рядом с этой инструкцией.

## 4. Готовый код

Ниже полный код каждого текстового файла.

Для нового Kotlin-файла: в Android Studio открой основную группу kotlin+java → com.example.studyflowapp (без test/androidTest), нажми правой кнопкой → New → Kotlin Class/File → File, имя RegisterActivity. Замени содержимое кодом ниже.

Для XML-разметки: res → layout → New → Layout Resource File, имя activity_register. Открой вкладку Code и вставь код целиком.

Для остальных XML: в соответствующей папке res/drawable или res/values выбери New → Drawable Resource File / Values Resource File, введи имя из указанного пути без .xml, затем полностью вставь код.

Для существующих LoginActivity.kt и AndroidManifest.xml: открой именно указанный файл, выдели старый код целиком и замени соответствующим кодом ниже. Эти версии сохраняют код предыдущих экранов.

PNG тени не нужно создавать вручную: скопируй готовый register_card_shadow.png из архива в app/src/main/res/drawable-xxhdpi. Эта папка уже есть в проекте.
''')
for p in files:
    rel=p.relative_to(PACKAGE);guide.append(f'### Файл: `{PROJECT/rel}`\n')
    if p.suffix=='.png':guide.append('Действие: скопировать готовый PNG из архива по этому же относительному пути.\n')
    else:
        lang='kotlin' if p.suffix=='.kt' else 'xml'
        guide.append('Действие: создать файл, если его нет, или полностью заменить содержимое следующим кодом.\n')
        guide.append(f'```{lang}\n{p.read_text(encoding="utf-8").rstrip()}\n```\n')
guide.append(f'''## 5. Проверка

- assembleDebug и lintDebug: успешно, ошибок 0. Lint отмечает подпись 10 sp под паролем как SmallSp; размер взят из макета. Остальные предупреждения существовали до этого этапа.
- Эмулятор API 37: подтверждены шесть пустых полей, отсутствие автоматического фокуса при открытии, ввод имени/email/пароля, показ и скрытие пароля, переключение чекбокса.
- Проверены открытие Register из Login, возврат по верхней стрелке и нижнему Log In, повторное открытие, отсутствие реальной регистрации по Create Account.
- Снято сравнение при 390×929 dp и проверен экран 360×640 dp с текстом 130%. На небольшом экране форма прокручивается, кнопки доступны, клавиатура не перекрывает активное поле после прокрутки.
- {len(protected)} прежних файлов проверены по SHA-256 и не изменены. Настройки размера экрана, плотности и шрифта эмулятора восстановлены. Настройки клавиатуры Gboard не менялись.
- Сохранён minSdk 24; отдельный запуск на Android 7/API 24 не выполнялся.

Скриншоты: Register-390x929.png, Register-emulator.png, Register-small-font130.png, Register-small-keyboard.png. Результаты проверок: verification.json.
''')
(ROOT/'Register-инструкция-и-код.md').write_text('\n\n'.join(guide),encoding='utf-8')
with zipfile.ZipFile(ROOT/'StudyFlowApp-register.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(PACKAGE))
print(f'Guide and archive ready: {len(files)} files, {len(protected)} existing files unchanged.')
