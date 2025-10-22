@echo off
setlocal enabledelayedexpansion

echo ====================================================
echo     SAD App v2.0 - Automação Completa
echo ====================================================
echo     Build + Teste + Análise + Distribuição
echo ====================================================
echo.

REM Menu de opções
:menu
echo 🎯 Escolha uma ação:
echo.
echo [1] 🚀 Build Completo (Otimizado)
echo [2] 🧪 Testar Executável
echo [3] 📊 Analisar Performance  
echo [4] 📦 Preparar Distribuição
echo [5] 🔄 Processo Completo (1+2+3+4)
echo [6] 🧹 Limpar Builds
echo [0] ❌ Sair
echo.
set /p choice="Digite sua escolha (0-6): "

if "%choice%"=="1" goto build
if "%choice%"=="2" goto test
if "%choice%"=="3" goto analyze
if "%choice%"=="4" goto package
if "%choice%"=="5" goto full_process
if "%choice%"=="6" goto clean
if "%choice%"=="0" goto exit
goto menu

:build
echo.
echo ====================================================
echo 🚀 INICIANDO BUILD OTIMIZADO
echo ====================================================
call build_optimized.bat
goto menu

:test
echo.
echo ====================================================
echo 🧪 TESTANDO EXECUTÁVEL
echo ====================================================
call test_optimized_exe.bat
goto menu

:analyze
echo.
echo ====================================================
echo 📊 ANALISANDO PERFORMANCE
echo ====================================================
call analyze_performance.bat
goto menu

:package
echo.
echo ====================================================
echo 📦 PREPARANDO DISTRIBUIÇÃO
echo ====================================================
echo.

if not exist "dist\SAD_App_v2_Optimized\SAD_App_v2.exe" (
    echo ❌ Build otimizado não encontrado!
    echo 💡 Execute o build primeiro (opção 1)
    echo.
    pause
    goto menu
)

echo 🔧 Criando pacote de distribuição...

REM Criar pasta de distribuição
if not exist "release" mkdir release

REM Criar timestamp para versionamento
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "timestamp=%dt:~0,4%-%dt:~4,2%-%dt:~6,2%_%dt:~8,2%-%dt:~10,2%"

set "release_name=SAD_App_v2_Optimized_%timestamp%"
set "release_path=release\%release_name%"

echo 📁 Criando: %release_name%

REM Copiar build otimizado
xcopy "dist\SAD_App_v2_Optimized" "%release_path%" /E /I /Q

REM Criar arquivo README para distribuição
echo # SAD App v2.0 - Versão Otimizada > "%release_path%\README.txt"
echo. >> "%release_path%\README.txt"
echo Data do Build: %timestamp% >> "%release_path%\README.txt"
echo. >> "%release_path%\README.txt"
echo ## Como usar: >> "%release_path%\README.txt"
echo 1. Execute SAD_App_v2.exe >> "%release_path%\README.txt"
echo 2. Mantenha a pasta _internal junto com o executável >> "%release_path%\README.txt"
echo 3. Para mover o programa, mova toda a pasta >> "%release_path%\README.txt"
echo. >> "%release_path%\README.txt"
echo ## Estrutura: >> "%release_path%\README.txt"
echo - SAD_App_v2.exe: Executável principal >> "%release_path%\README.txt"
echo - _internal/: Bibliotecas e recursos necessários >> "%release_path%\README.txt"

REM Criar arquivo ZIP
echo 🗜️ Criando arquivo ZIP...
if exist "%release_path%.zip" del "%release_path%.zip"

REM Usar PowerShell para criar ZIP
powershell -command "Compress-Archive -Path '%release_path%' -DestinationPath '%release_path%.zip' -Force"

if exist "%release_path%.zip" (
    echo ✅ Distribuição criada com sucesso!
    echo.
    echo 📦 Arquivos criados:
    echo   📁 Pasta: %release_path%
    echo   🗜️ ZIP: %release_path%.zip
    echo.
    
    REM Informações do pacote
    for %%A in ("%release_path%.zip") do (
        set /a zip_size=%%~zA/1024/1024
        echo 💾 Tamanho do ZIP: !zip_size! MB
    )
    
    echo 🎯 Pronto para distribuição!
) else (
    echo ❌ Erro ao criar arquivo ZIP
)

echo.
pause
goto menu

:full_process
echo.
echo ====================================================
echo 🔄 PROCESSO COMPLETO
echo ====================================================
echo.

echo 🚀 1/4 - Executando build...
call build_optimized.bat

echo.
echo 🧪 2/4 - Testando executável...
timeout /t 3 /nobreak >nul
call test_optimized_exe.bat

echo.
echo 📊 3/4 - Analisando performance...
timeout /t 3 /nobreak >nul
call analyze_performance.bat

echo.
echo 📦 4/4 - Preparando distribuição...
timeout /t 3 /nobreak >nul
goto package

:clean
echo.
echo ====================================================
echo 🧹 LIMPEZA DE BUILDS
echo ====================================================
echo.

echo ⚠️ Isso removerá todos os builds e caches
set /p confirm="Tem certeza? (S/N): "

if /i "%confirm%"=="S" (
    echo 🧹 Removendo builds...
    
    if exist "build" rmdir /s /q "build"
    if exist "dist" rmdir /s /q "dist"
    if exist "__pycache__" rmdir /s /q "__pycache__"
    if exist ".cache" rmdir /s /q ".cache"
    if exist "release" rmdir /s /q "release"
    
    REM Limpar cache Python recursivamente
    for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
    
    echo ✅ Limpeza concluída!
) else (
    echo ❌ Limpeza cancelada
)

echo.
pause
goto menu

:exit
echo.
echo 👋 Obrigado por usar o SAD App v2.0!
echo.
exit /b 0