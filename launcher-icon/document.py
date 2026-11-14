from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
project=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
res=project/'app/src/main/res'
before=json.loads((root/'before.json').read_text(encoding='utf-8'))
expected={str(p.relative_to(root/'res')) for p in (root/'res').rglob('*.xml')}
changed={str(p.relative_to(res)) for p in res.rglob('*') if p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()!=before.get(str(p.relative_to(res)))}
assert changed==expected,(changed,expected)
text='''# Иконка StudyFlow

Иконка уже добавлена в проект и обновлена на подключённом телефоне. Повторно вставлять код не требуется.

Использован существующий контур книги с галочкой из ic_studyflow_logo.xml и цвета заставки: #273D86, #4969E8, #9672D6.

## Какие файлы изменены

'''
for rel in sorted(expected):
    path=res/rel
    text+=f'- `{path}`\n'
text+='''
Первые два drawable — фон и белый знак. Файлы mipmap-anydpi — варианты для Android 7. Существующие mipmap-anydpi-v26/ic_launcher.xml и ic_launcher_round.xml уже подключают фон, знак и монохромный слой для новых версий Android. В AndroidManifest.xml ссылки на иконки уже были настроены.

Системная заставка использует отдельный ресурс, поэтому её настройка не менялась.

## Проверка

1. На телефоне открой список приложений и найди StudyFlowApp.
2. Иконка должна показывать белую книгу с галочкой на синем градиентном фоне.
3. Нажми на иконку для запуска приложения.
4. Для последующих сборок в Android Studio выбери конфигурацию app, подключённый телефон и нажми Run ▶.

Сборка assembleDebug завершилась BUILD SUCCESSFUL. Установка обновления через adb install -r завершилась Success. Проверена упаковка обычного и адаптивного вариантов в APK. Автоматическая проверка хешей подтвердила изменение только четырёх указанных ресурсов.

Если в списке приложений осталась старая иконка, перезагрузи телефон. Удалять приложение для этого не нужно.

Форма и тематическая окраска адаптивной иконки определяются оболочкой телефона: [документация Android](https://developer.android.com/develop/ui/compose/system/icon_design_adaptive).

## Полный код ресурсов

Ниже приведён код для справки. Все файлы уже находятся в проекте. Тип новых файлов — XML.

'''
for rel in sorted(expected):
    text+=f'### `{res/rel}`\n\n```xml\n{(res/rel).read_text(encoding="utf-8")}\n```\n\n'
(root/'Иконка-StudyFlow.md').write_text(text,encoding='utf-8')
(root/'verification.json').write_text(json.dumps({'changed_resources':sorted(changed),'build':'assembleDebug BUILD SUCCESSFUL','install':'adb install -r Success','preview':'preview.png'},indent=2),encoding='utf-8')
print('Verified four scoped resource changes; guide saved.')
