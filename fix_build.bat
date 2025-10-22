@echo off
setlocal enabledelayedexpansion

echo ====================================================
echo     SAD App v2.0 - Correção de Build
echo ====================================================
echo     Corrigindo dependências em falta
echo ====================================================
echo.

REM Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Verificar se o packaging está instalado
echo 🔍 Verificando dependências...
python -c "import packaging; print('✅ packaging:', packaging.__version__)" 2>nul
if !errorlevel! neq 0 (
    echo ❌ Módulo packaging não encontrado!
    echo 🔧 Instalando packaging...
    pip install packaging
) else (
    echo ✅ Módulo packaging já instalado
)

REM Verificar outras dependências críticas do CustomTkinter
echo.
echo 🔍 Verificando outras dependências críticas...

python -c "import customtkinter; print('✅ customtkinter:', customtkinter.__version__)" 2>nul
if !errorlevel! neq 0 (
    echo ❌ CustomTkinter com problemas!
    echo 🔧 Reinstalando CustomTkinter...
    pip uninstall customtkinter -y
    pip install customtkinter
)

python -c "import tkinter; print('✅ tkinter: OK')" 2>nul
if !errorlevel! neq 0 (
    echo ❌ Tkinter não disponível!
    echo ⚠️ Tkinter deve estar incluído no Python
)

python -c "import openpyxl; print('✅ openpyxl:', openpyxl.__version__)" 2>nul
if !errorlevel! neq 0 (
    echo ❌ OpenPyXL com problemas!
    pip install openpyxl
)

python -c "import docx; print('✅ python-docx: OK')" 2>nul
if !errorlevel! neq 0 (
    echo ❌ Python-docx com problemas!
    pip install python-docx
)

python -c "import yaml; print('✅ PyYAML: OK')" 2>nul
if !errorlevel! neq 0 (
    echo ❌ PyYAML com problemas!
    pip install PyYAML
)

echo.
echo 🔍 Verificando módulos do sistema necessários...
python -c "import urllib; print('✅ urllib: OK')" 2>nul
if !errorlevel! neq 0 (
    echo ❌ urllib com problemas!
    echo ⚠️ urllib deve estar incluído no Python
)

python -c "import mimetypes; print('✅ mimetypes: OK')" 2>nul
if !errorlevel! neq 0 (
    echo ❌ mimetypes com problemas!
    echo ⚠️ mimetypes deve estar incluído no Python
)

echo.
echo ====================================================
echo 🚀 Reconstruindo executável com correções...
echo ====================================================

REM Limpar build anterior
echo 🧹 Limpando build anterior...
if exist "build\SAD_App_v2_Optimized" rmdir /s /q "build\SAD_App_v2_Optimized"
if exist "dist\SAD_App_v2_Optimized" rmdir /s /q "dist\SAD_App_v2_Optimized"

REM Rebuild com configuração corrigida
echo 🔨 Executando build corrigido...
pyinstaller SAD_App_v2_Optimized.spec --clean --noconfirm

if !errorlevel! == 0 (
    echo.
    echo ✅ Build corrigido com sucesso!
    echo.
    echo 🧪 Testando executável...
    
    if exist "dist\SAD_App_v2_Optimized\SAD_App_v2.exe" (
        echo 📁 Executável encontrado
        
        REM Verificar se _internal tem o packaging
        if exist "dist\SAD_App_v2_Optimized\_internal" (
            echo 📂 Pasta _internal: ✅
            
            REM Verificar se packaging está incluído
            if exist "dist\SAD_App_v2_Optimized\_internal\packaging" (
                echo 📦 Módulo packaging incluído: ✅
            ) else (
                echo ⚠️ Módulo packaging não encontrado no _internal
            )
            
            REM Verificar outros módulos críticos
            if exist "dist\SAD_App_v2_Optimized\_internal\customtkinter" echo 🎨 CustomTkinter: ✅
            if exist "dist\SAD_App_v2_Optimized\_internal\_tkinter.pyd" echo 🎨 Tkinter Core: ✅
        )
        
        echo.
        echo 🎯 Executável pronto para teste!
        echo 💡 Execute: .\test_optimized_exe.bat
        
    ) else (
        echo ❌ Executável não foi criado!
    )
    
) else (
    echo ❌ Erro no build corrigido!
    echo.
    echo 🔍 Possíveis soluções:
    echo   • Verificar se todas as dependências estão instaladas
    echo   • Executar: pip install --upgrade pyinstaller
    echo   • Verificar logs de erro acima
)

echo.
pause