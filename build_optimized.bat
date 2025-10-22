@echo off
setlocal enabledelayedexpansion

echo ====================================================
echo     SAD App v2.0 - Build Script Otimizado
echo ====================================================
echo     Estrutura: Executavel + _internal
echo     Otimizacao: Carregamento Rapido
echo ====================================================
echo.

REM Verificar se ambiente virtual existe
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Ambiente virtual não encontrado!
    echo 💡 Execute: python -m venv .venv
    echo.
    pause
    exit /b 1
)

REM Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Verificar se PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if !errorlevel! neq 0 (
    echo ❌ PyInstaller não encontrado!
    echo 🔧 Instalando PyInstaller...
    pip install pyinstaller
)

REM Limpar builds anteriores
echo 🧹 Limpando builds anteriores...
if exist "build\SAD_App_v2_Optimized" rmdir /s /q "build\SAD_App_v2_Optimized"
if exist "dist\SAD_App_v2_Optimized" rmdir /s /q "dist\SAD_App_v2_Optimized"

REM Construir executável otimizado
echo.
echo 🚀 Construindo executável otimizado...
echo ⚡ Usando estrutura _internal para carregamento rápido...
echo.

pyinstaller SAD_App_v2_Optimized.spec --clean --noconfirm

REM Verificar resultado
if !errorlevel! == 0 (
    echo.
    echo ✅ Build concluído com sucesso!
    echo.
    echo 📊 Informações do Build:
    echo ========================================
    
    REM Verificar estrutura criada
    if exist "dist\SAD_App_v2_Optimized\SAD_App_v2.exe" (
        echo 📁 Executável: dist\SAD_App_v2_Optimized\SAD_App_v2.exe
        
        REM Tamanho do executável
        for %%A in ("dist\SAD_App_v2_Optimized\SAD_App_v2.exe") do (
            set /a size=%%~zA/1024/1024
            echo 💾 Tamanho EXE: !size! MB
        )
        
        REM Verificar _internal
        if exist "dist\SAD_App_v2_Optimized\_internal" (
            echo 📂 Estrutura: _internal ✅
            
            REM Contar arquivos no _internal
            set count=0
            for /f %%i in ('dir /b /a-d "dist\SAD_App_v2_Optimized\_internal" 2^>nul ^| find /c /v ""') do set count=%%i
            echo 📦 Arquivos _internal: !count!
            
            REM Tamanho total da pasta
            set total_size=0
            for /f "tokens=3" %%a in ('dir "dist\SAD_App_v2_Optimized" /s /-c ^| find "bytes"') do set total_size=%%a
            set /a total_mb=!total_size!/1024/1024
            echo 💽 Tamanho Total: !total_mb! MB
        ) else (
            echo ⚠️ Pasta _internal não encontrada!
        )
        
        echo.
        echo 🎉 Pronto para distribuição!
        echo 💡 Para testar: .\test_optimized_exe.bat
        
    ) else (
        echo ❌ Executável não foi criado!
    )
    
) else (
    echo.
    echo ❌ Erro na construção do executável
    echo 🔍 Verifique as mensagens de erro acima
    echo 💡 Logs detalhados em: build\SAD_App_v2_Optimized\
)

echo.
echo ========================================
pause