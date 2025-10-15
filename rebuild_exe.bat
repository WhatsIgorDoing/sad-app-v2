@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo    SAD App v2.0 - Rebuild Executável
echo ===================================================
echo.

REM Verificar se ambiente virtual está ativado
if not defined VIRTUAL_ENV (
    echo [AVISO] Ambiente virtual não está ativado.
    echo         Recomendado ativar usando: .venv\Scripts\Activate.ps1
    echo.
    set /p CONTINUE="Continuar mesmo assim? (S/N): "
    if /i "!CONTINUE!" neq "S" exit /b
    echo.
)

REM Verificar se PyInstaller está instalado
py -m pip show pyinstaller > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERRO] PyInstaller não está instalado.
    echo        Instalando PyInstaller...
    py -m pip install pyinstaller
    if %ERRORLEVEL% neq 0 (
        echo [ERRO] Falha ao instalar PyInstaller. Saindo.
        exit /b 1
    )
    echo [OK] PyInstaller instalado com sucesso.
    echo.
)

REM Remover executável antigo se existir
echo [1/4] Verificando executável antigo...
if exist "dist\SAD_App_v2.exe" (
    echo      Removendo executável antigo...
    del "dist\SAD_App_v2.exe" 2>nul
    if exist "dist\SAD_App_v2.exe" (
        echo [ERRO] Não foi possível remover o executável antigo.
        echo        Verifique se ele está em uso por outro processo.
        exit /b 1
    ) else (
        echo [OK] Executável antigo removido.
    )
) else (
    echo [OK] Nenhum executável antigo encontrado.
)
echo.

REM Limpar diretórios de build se existirem
echo [2/4] Limpando diretórios de build...
if exist "build" rmdir /s /q "build"
if exist "dist" (
    REM Manter a pasta dist, mas remover conteúdo
    for /d %%d in (dist\*) do rmdir /s /q "%%d"
    del /q dist\* 2>nul
) else (
    mkdir "dist"
)
echo [OK] Diretórios limpos.
echo.

REM Gerar novo executável
echo [3/4] Gerando novo executável...
echo      Este processo pode demorar alguns minutos...
echo.

py -m PyInstaller --name=SAD_App_v2 --onefile --windowed ^
    --add-data=config;config ^
    --add-data=src;src ^
    --hidden-import=customtkinter ^
    --hidden-import=tkinter ^
    --hidden-import=openpyxl ^
    --hidden-import=docx ^
    --hidden-import=PyPDF2 ^
    --hidden-import=yaml ^
    --collect-all=customtkinter ^
    --noconfirm ^
    --clean ^
    run.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERRO] Falha ao gerar o executável.
    exit /b 1
)
echo.

REM Verificar se o executável foi criado
echo [4/4] Verificando resultado...
if exist "dist\SAD_App_v2.exe" (
    echo.
    echo ===================================================
    echo [SUCESSO] Executável gerado com sucesso!
    echo.
    echo Arquivo: dist\SAD_App_v2.exe
    for %%A in ("dist\SAD_App_v2.exe") do set size=%%~zA
    set /a "size_mb=size/1048576"
    set /a "size_kb=(size%%1048576)/1024"
    echo Tamanho: !size_mb!.!size_kb! MB
    echo ===================================================
) else (
    echo.
    echo [ERRO] O executável não foi encontrado no diretório 'dist'.
    echo        Verifique os logs acima para possíveis erros.
    exit /b 1
)

exit /b 0
