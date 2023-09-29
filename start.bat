@echo off
set Selection=

:whileloop
set /p Selection="Which file do you want to run? Enter 0.111 or 0.222: "
if "%Selection%"=="0.111" (
    set RubyPath=C:\Ruby27-x64\bin\ruby.exe
    if exist "%RubyPath%" (
        "%RubyPath%" foundmir/foundoublemirror/Program.rb
        exit /b
    ) else (
        echo Ruby is not installed.
    )
) else if "%Selection%"=="0.222" (
    python foundmir/foundoublemirror/data/main.py
    exit /b
) else (
    echo Invalid selection.
)
goto :whileloop