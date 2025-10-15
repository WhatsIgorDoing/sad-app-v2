@echo off
echo ====================================
echo     SAD App v2.0 - Build Script
echo ====================================
echo.

REM Ativar ambiente virtual
call .venv\Scripts\activate.bat

REM Construir executável
echo 🚀 Construindo executável...
pyinstaller --name=SAD_App_v2 --onefile --windowed --add-data=config;config --add-data=src;src --hidden-import=customtkinter --hidden-import=tkinter --hidden-import=openpyxl --hidden-import=docx --hidden-import=PyPDF2 --hidden-import=yaml --collect-all=customtkinter --noconfirm --clean run.py

if %errorlevel% == 0 (
    echo.
    echo ✅ Executável criado com sucesso!
    echo 📁 Localização: dist\SAD_App_v2.exe
    echo 🎉 Pronto para distribuição!
) else (
    echo.
    echo ❌ Erro na construção do executável
    echo Verifique as mensagens de erro acima
)

echo.
pause