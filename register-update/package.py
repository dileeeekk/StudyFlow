from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
PACKAGE=ROOT/'StudyFlowApp-register-update'
files=sorted(p for p in PACKAGE.rglob('*') if p.is_file())
changed={str(p.relative_to(PACKAGE)) for p in files}
before=json.loads((ROOT/'before.json').read_text())
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p in files:assert digest(p)==digest(PROJECT/p.relative_to(PACKAGE))
for rel,sha in before.items():
    if rel not in changed:assert digest(PROJECT/rel)==sha,rel
assert all(json.loads((ROOT/'verification.json').read_text()).values())
guide=['''# Register — только University

Изменения уже установлены в проект StudyFlowApp.

## Что изменилось

Удалены Year и Group. University теперь обычное пустое поле для ввода названия университета без стрелки и без текста-подсказки. Карточка стала короче на 91 dp; чекбокс, кнопка и ссылка ниже поднялись вместе с ней. Тень пересоздана под новую высоту карточки, чтобы сохранить её скругления и размытие.

На клавиатуре поле пароля теперь предлагает «Далее» к University, а University — «Готово» для закрытия клавиатуры. Новое поле участвует в существующей прокрутке формы при появлении клавиатуры. Сохранение профиля и регистрация не добавлены.

## Как проверить

1. В Android Studio открой StudyFlowApp и нажми Run ▶.
2. Открой Login → Create an account.
3. Под паролем должно остаться только пустое поле University; Year и Group отсутствуют.
4. Нажми University и введи название. Клавиатура должна открыться, введённые буквы — появиться в поле.

Сборка assembleDebug и lintDebug прошла без ошибок. В эмуляторе проверены отсутствие Year/Group, пустое начальное значение, ввод текста в University, клавиатура и возврат на Login. Все остальные исходные файлы сохранены.

## Файлы и полный код

Ниже актуальный полный код. Вручную копировать его сейчас не требуется. Для восстановления открой указанный файл, выдели старое содержимое целиком и замени кодом ниже. Новые файлы создавать не нужно. Предыдущие версии сохранены в папке backup рядом с этой инструкцией.
''']
for p in files:
    rel=p.relative_to(PACKAGE)
    guide.append(f'### `{PROJECT/rel}`\n')
    if p.suffix=='.png':guide.append('Заменить PNG готовым файлом из архива по этому же относительному пути.\n')
    else:
        lang='kotlin' if p.suffix=='.kt' else 'xml'
        guide.append(f'```{lang}\n{p.read_text(encoding="utf-8").rstrip()}\n```\n')
(ROOT/'University-инструкция-и-код.md').write_text('\n\n'.join(guide),encoding='utf-8')
with zipfile.ZipFile(ROOT/'StudyFlowApp-register-update.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(PACKAGE))
print(f'Package ready; {len(before)-len(changed)} other files unchanged.')
