from pathlib import Path
import hashlib,json,zipfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
PACKAGE=ROOT/'StudyFlowApp-auth-validation'
files=sorted(p for p in PACKAGE.rglob('*') if p.is_file());changed={str(p.relative_to(PACKAGE)) for p in files}
before=json.loads((ROOT/'before.json').read_text());digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p in files:assert digest(p)==digest(PROJECT/p.relative_to(PACKAGE))
for rel,sha in before.items():
    if rel not in changed:assert digest(PROJECT/rel)==sha,rel
assert all(json.loads((ROOT/'verification.json').read_text()).values())
lint=ET.parse(PROJECT/'app/build/reports/lint-results-debug.xml');assert not [n for n in lint.iter('issue') if n.get('severity') in ['Error','Fatal']]
guide=['''# Проверка заполнения Login и Register

Изменения уже внесены в проект StudyFlowApp.

## Как работают кнопки

**Create Account** активна только когда заполнены Full name, University email, Password и University, пароль содержит минимум 8 символов и установлена галочка согласия. Если очистить любое обязательное поле, сократить пароль или снять галочку, кнопка сразу блокируется и становится бледнее.

**Log In** активна только когда заполнены Email address и Password, а пароль содержит минимум 8 символов. Строки из одних пробелов не считаются заполненными. Проверка формата и существования email не добавлялась.

На обоих экранах у пустого пароля нет подписи; при 1–7 символах появляется красная At least 8 characters, при 8 и более она исчезает. Реакция обновляется и при вводе, и при удалении. Подпись Login размещена под паролем на месте удалённого Remember me; ссылка Forgot password? сохранена справа. Remember me удалён вместе с чекбоксом.

Пока это поведение интерфейса: активные кнопки закрывают клавиатуру, реальный вход и создание аккаунта не подключены.

## Как проверить в Android Studio

1. Открой проект `C:\\Users\\admin\\AndroidStudioProjects\\StudyFlowApp`, выбери **app** и нажми **Run ▶**.
2. На onboarding нажми **Log In**. Поля пустые, кнопка входа неактивна, Remember me отсутствует.
3. Введи тестовый email и пароль из 7 символов — появится красная подпись, кнопка останется неактивной. Добавь восьмой символ — подпись исчезнет и кнопка станет активной. Очисти email — кнопка снова заблокируется.
4. Открой **Create an account**. Заполни имя, email, пароль минимум из 8 символов и университет. При установленной галочке кнопка активируется.
5. Удали значение любого поля или сними галочку — кнопка должна сразу блокироваться.

Сборка assembleDebug и lintDebug прошла без ошибок. В эмуляторе проверены начальные состояния, пробелы вместо значений, граница пароля 7/8 символов, удаление каждого обязательного поля регистрации, согласие и отсутствие Remember me. Тестовые значения очищены повторным открытием экранов.

## Файлы и полный код

Изменены только четыре файла ниже. Вручную копировать код сейчас не требуется. Если нужно восстановить эти версии: открой указанный файл, выдели старое содержимое целиком и вставь соответствующий код ниже. Новые файлы создавать не нужно. Предыдущие версии сохранены в папке backup рядом с этой инструкцией.
''']
for p in files:
    rel=p.relative_to(PACKAGE);lang='kotlin' if p.suffix=='.kt' else 'xml'
    guide.append(f'### `{PROJECT/rel}`\n\n```{lang}\n{p.read_text(encoding="utf-8").rstrip()}\n```')
(ROOT/'Login-и-Register-проверка-полей.md').write_text('\n\n'.join(guide),encoding='utf-8')
with zipfile.ZipFile(ROOT/'StudyFlowApp-auth-validation.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(PACKAGE))
print(f'4 files verified; {len(before)-4} other files preserved. Guide and archive ready.')
