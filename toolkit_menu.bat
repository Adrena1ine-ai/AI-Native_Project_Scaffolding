@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: AI Toolkit - Interactive Menu
:: Запуск из AI-Native_Project_Scaffolding

title AI Toolkit - Interactive Menu

:MAIN_MENU
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🦊 AI Toolkit - Interactive Menu                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Запрос пути к проекту
if "%PROJECT_PATH%"=="" (
    echo 📁 Введите путь к проекту:
    echo    (например: C:\Users\Antaras\Downloads\archive_2060_22472222\opt\bots\FaberlicFamilyBot)
    echo    или нажмите Enter для текущей директории
    echo.
    set /p PROJECT_PATH="Путь: "
    
    if "!PROJECT_PATH!"=="" (
        set PROJECT_PATH=%CD%
    )
    
    :: Проверка существования пути
    if not exist "!PROJECT_PATH!" (
        echo.
        echo ❌ Ошибка: Путь не существует: !PROJECT_PATH!
        echo.
        pause
        set PROJECT_PATH=
        goto MAIN_MENU
    )
    
    :: Преобразование в абсолютный путь
    cd /d "!PROJECT_PATH!" 2>nul
    if errorlevel 1 (
        echo.
        echo ❌ Ошибка: Не удалось перейти в директорию: !PROJECT_PATH!
        echo.
        pause
        set PROJECT_PATH=
        goto MAIN_MENU
    )
    set PROJECT_PATH=%CD%
    cd /d "%~dp0"
)

echo.
echo 📂 Текущий проект: %PROJECT_PATH%
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  Выберите действие:                                         ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║  1. 🔍 Диагностика проекта (doctor --report)                ║
echo ║  2. 🔧 Авто-исправление проблем (doctor --auto)             ║
echo ║  3. 🧹 Deep Clean - переместить тяжелые файлы                ║
echo ║  4. 🗑️  Переместить мусорные файлы в garbage               ║
echo ║  5. 📊 Обновить PROJECT_STATUS.md и CURRENT_CONTEXT_MAP.md ║
echo ║  6. 🔄 Восстановить файлы из Deep Clean (--restore)         ║
echo ║  7. 📝 Показать статус проекта (status)                    ║
echo ║  8. 🏗️  Архитектурная реструктуризация (architect)          ║
echo ║  9. 🔄 Сменить проект                                       ║
echo ║  0. ❌ Выход                                                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
set /p CHOICE="Ваш выбор (0-9): "

if "%CHOICE%"=="1" goto DIAGNOSTIC
if "%CHOICE%"=="2" goto AUTO_FIX
if "%CHOICE%"=="3" goto DEEP_CLEAN
if "%CHOICE%"=="4" goto GARBAGE_CLEAN
if "%CHOICE%"=="5" goto UPDATE_DOCS
if "%CHOICE%"=="6" goto RESTORE
if "%CHOICE%"=="7" goto STATUS
if "%CHOICE%"=="8" goto ARCHITECT
if "%CHOICE%"=="9" goto CHANGE_PROJECT
if "%CHOICE%"=="0" goto EXIT

echo.
echo ❌ Неверный выбор. Попробуйте снова.
timeout /t 2 >nul
goto MAIN_MENU

:DIAGNOSTIC
cls
echo.
echo 🔍 Диагностика проекта...
echo.
python -m src.cli doctor "%PROJECT_PATH%" --report
echo.
pause
goto MAIN_MENU

:AUTO_FIX
cls
echo.
echo 🔧 Авто-исправление проблем...
echo.
python -m src.cli doctor "%PROJECT_PATH%" --auto
echo.
pause
goto MAIN_MENU

:DEEP_CLEAN
cls
echo.
echo 🧹 Deep Clean - перемещение тяжелых файлов
echo.
echo Выберите режим:
echo   1. Предпросмотр (--dry-run)
echo   2. Выполнить (--auto)
echo   3. Настроить порог токенов
echo.
set /p DEEP_CHOICE="Ваш выбор (1-3): "

if "%DEEP_CHOICE%"=="1" (
    python -m src.cli doctor "%PROJECT_PATH%" --deep-clean --dry-run
) else if "%DEEP_CHOICE%"=="2" (
    python -m src.cli doctor "%PROJECT_PATH%" --deep-clean --auto
) else if "%DEEP_CHOICE%"=="3" (
    set /p THRESHOLD="Введите порог токенов (по умолчанию 1000): "
    if "!THRESHOLD!"=="" set THRESHOLD=1000
    python -m src.cli doctor "%PROJECT_PATH%" --deep-clean --threshold !THRESHOLD! --auto
) else (
    echo ❌ Неверный выбор
)
echo.
pause
goto MAIN_MENU

:GARBAGE_CLEAN
cls
echo.
echo 🗑️  Перемещение мусорных файлов в garbage
echo.
echo Выберите режим:
echo   1. Предпросмотр (--dry-run)
echo   2. Выполнить (--auto)
echo.
set /p GARBAGE_CHOICE="Ваш выбор (1-2): "

if "%GARBAGE_CHOICE%"=="1" (
    python -m src.cli doctor "%PROJECT_PATH%" --garbage-clean --dry-run
) else if "%GARBAGE_CHOICE%"=="2" (
    python -m src.cli doctor "%PROJECT_PATH%" --garbage-clean --auto
) else (
    echo ❌ Неверный выбор
)
echo.
pause
goto MAIN_MENU

:UPDATE_DOCS
cls
echo.
echo 📊 Обновление документации...
echo.
python -m src.cli status "%PROJECT_PATH%" --skip-tests
echo.
pause
goto MAIN_MENU

:RESTORE
cls
echo.
echo 🔄 Восстановление файлов из Deep Clean...
echo.
python -m src.cli doctor "%PROJECT_PATH%" --restore
echo.
pause
goto MAIN_MENU

:STATUS
cls
echo.
echo 📝 Статус проекта...
echo.
python -m src.cli status "%PROJECT_PATH%"
echo.
pause
goto MAIN_MENU

:ARCHITECT
cls
echo.
echo 🏗️  Архитектурная реструктуризация...
echo.
python -m src.cli architect "%PROJECT_PATH%"
echo.
pause
goto MAIN_MENU

:CHANGE_PROJECT
set PROJECT_PATH=
goto MAIN_MENU

:EXIT
cls
echo.
echo 👋 До свидания!
echo.
timeout /t 2 >nul
exit /b 0

