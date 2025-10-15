@echo off
echo ====================================
echo     SAD App v2.0 - Teste Executável
echo ====================================
echo.

if exist "dist\SAD_App_v2.exe" (
    echo 🚀 Executando SAD_App_v2.exe...
    echo.
    start "" "dist\SAD_App_v2.exe"
    echo ✅ Executável iniciado!
    echo 💡 Se a aplicação não abrir, verifique se não há bloqueios do Windows Defender
) else (
    echo ❌ Executável não encontrado!
    echo 💡 Execute build.bat primeiro para criar o executável
)

echo.
pause