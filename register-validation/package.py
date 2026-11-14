from pathlib import Path
import hashlib,json,zipfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
PACKAGE=ROOT/'StudyFlowApp-register-validation'
files=sorted(p for p in PACKAGE.rglob('*') if p.is_file());changed={str(p.relative_to(PACKAGE)) for p in files}
before=json.loads((ROOT/'before.json').read_text());digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p in files:assert digest(p)==digest(PROJECT/p.relative_to(PACKAGE))
for rel,sha in before.items():
    if rel not in changed:assert digest(PROJECT/rel)==sha,rel
assert all(json.loads((ROOT/'verification.json').read_text()).values())
lint=ET.parse(PROJECT/'app/build/reports/lint-results-debug.xml');assert not [n for n in lint.iter('issue') if n.get('severity') in ['Error','Fatal']]
guide=['''# Register — согласие и подпись пароля

Изменения уже установлены в проект.

## Поведение

- Если снять галочку согласия, Create Account становится бледнее и не реагирует на нажатие. При установке галочки кнопка снова активна. Начальное состояние галочки сохранено как раньше.
- При пустом пароле подписи нет. При 1–7 символах под полем появляется красная надпись At least 8 characters. При 8 и более символах она исчезает. При удалении символов состояние обновляется сразу.
- Место под подпись сохранено, чтобы форма не прыгала во время ввода.
- Изменена только локальная реакция интерфейса. Реальная регистрация не подключалась; блокировка кнопки сейчас зависит от согласия, проверка длины показывает подпись.

## Проверка

В Android Studio нажми Run ▶, затем Login → Create an account. Сними/установи галочку. В поле Password введи 7 символов, затем восьмой, затем удали символы. Ожидаемое поведение описано выше.

assembleDebug и lintDebug прошли без ошибок. В эмуляторе проверены блокировка и включение кнопки, отсутствие подписи при пустом поле, её появление при 7 символах, исчезновение при 8 и обратное обновление при удалении. Тестовый пароль затем очищен повторным открытием экрана.

## Файлы и полный код

Изменены только три файла ниже. Вручную копировать сейчас ничего не нужно. Для восстановления открой соответствующий файл и полностью замени содержимое приведённым кодом. Новые файлы создавать не требуется. Предыдущие версии находятся в папке backup рядом с этой инструкцией.
''']
for p in files:
    rel=p.relative_to(PACKAGE);lang='kotlin' if p.suffix=='.kt' else 'xml'
    guide.append(f'### `{PROJECT/rel}`\n\n```{lang}\n{p.read_text(encoding="utf-8").rstrip()}\n```')
(ROOT/'Согласие-и-пароль-инструкция.md').write_text('\n\n'.join(guide),encoding='utf-8')
with zipfile.ZipFile(ROOT/'StudyFlowApp-register-validation.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(PACKAGE))
print(f'3 files verified; {len(before)-3} other files unchanged.')
