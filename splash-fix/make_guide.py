from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

here=Path(__file__).resolve().parent
project=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
files={
 'MainActivity.kt':'app/src/main/java/com/example/studyflowapp/MainActivity.kt',
 'ic_splash_placeholder.xml':'app/src/main/res/drawable/ic_splash_placeholder.xml',
 'studyflow_splash_theme.xml':'app/src/main/res/values-v31/studyflow_splash_theme.xml',
}
lint=ET.parse(project/'app/build/reports/lint-results-debug.xml')
assert not [i for i in lint.findall('issue') if i.get('severity') in ('Error','Fatal')]
parts=['''# Исправление показа Splash

## Причина

Android 12 и новее сначала показывал свою системную заставку с центральным логотипом.
Таймер перехода в MainActivity запускался в onStart ещё до её исчезновения.
В последних запусках после появления макета оставалось около 0,8 секунды до перехода.

## Что исправлено

Системная центральная иконка заменена прозрачным drawable. После подготовки окна
системная заставка снимается без дополнительной анимации. Отсчёт 1,5 секунды
начинается после появления разметки и снятия системной заставки. Уход приложения
в фон отменяет ожидающий переход. Макеты Splash и onboarding не менялись.

Показ длительностью 1,5 секунды — временное поведение этапа вёрстки, не настоящая
загрузка данных. Когда появится загрузка, переход будет зависеть от её завершения.

До готовности окна Android всё равно может кратко показывать однотонный синий фон.
Системная заставка не поддерживает полный произвольный XML-макет с градиентом:
[документация Android](https://developer.android.com/develop/ui/views/launch/splash-screen).

## Запуск и проверка

Исправление уже установлено; вставлять код повторно не нужно.

1. В Android Studio нажмите **Stop ■**, если приложение запущено.
2. Выберите конфигурацию **app** и эмулятор **Medium Phone API 37.0**.
3. Нажмите **Run ▶**.
4. Вы должны увидеть полный градиентный Splash с надписью StudyFlow,
   а после его показа — onboarding с календарём.

`assembleDebug` и `lintDebug` завершились без ошибок. На эмуляторе API 37
сохранены два последовательных кадра полного Splash, затем подтверждено
открытие OnboardingActivity. Проверка на отдельном Android 7 устройстве не выполнялась.

Это исправление новее кода MainActivity из ранее выданного архива onboarding.
При ручном восстановлении используйте версии ниже поверх готового проекта.

## Файлы и полный код

''']
for name,rel in files.items():
    assert (here/name).read_bytes() == (project/rel).read_bytes()
    code=(here/name).read_text(encoding='utf-8')
    if name.endswith('.xml'): ET.fromstring(code)
    action='Создать новый XML-файл в папке res/drawable.' if name=='ic_splash_placeholder.xml' else 'Открыть существующий файл и полностью заменить содержимое.'
    parts.append(f'### {name}\n\n**Полный путь:** `{project/rel}`\n\n**Действие:** {action}\n\n')
    language='kotlin' if name.endswith('.kt') else 'xml'
    parts.append(f'```{language}\n{code}\n```\n\n')
guide=here/'Исправление-Splash.md'
guide.write_text(''.join(parts),encoding='utf-8')
with zipfile.ZipFile(here/'StudyFlow-splash-fix.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name,rel in files.items(): z.write(here/name,rel)
    z.write(guide,guide.name)
print('Guide and fix archive saved; installed files match; lint errors: 0.')
