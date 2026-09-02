@echo off
setlocal enabledelayedexpansion
echo Configurando o ambiente e mapeando scripts automaticamente...

:: Pega o caminho absoluto da pasta atual
set "PASTA_ATUAL=%~dp0"
set "PASTA_ATUAL=%PASTA_ATUAL:~0,-1%"

echo [1/2] Adicionando pasta ao PATH do Windows (para o CMD)...
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USER_PATH=%%b"
echo %USER_PATH% | findstr /i "%PASTA_ATUAL%" >nul
if errorlevel 1 (
    setx PATH "%USER_PATH%;%PASTA_ATUAL%"
)

echo [2/2] Mapeando scripts para o PowerShell...

:: Cria o arquivo ps1 linha por linha usando criacao de diretorio recursiva (.NET)
echo $profilePath = $PROFILE > "%TEMP%\atualizar_perfil.ps1"
echo $profileDir = Split-Path -Parent $profilePath >> "%TEMP%\atualizar_perfil.ps1"
echo [System.IO.Directory]::CreateDirectory($profileDir) ^| Out-Null >> "%TEMP%\atualizar_perfil.ps1"
echo if (!(Test-Path $profilePath)) { New-Item -ItemType File -Path $profilePath -Force ^| Out-Null } >> "%TEMP%\atualizar_perfil.ps1"
echo. >> "%TEMP%\atualizar_perfil.ps1"
echo $content = Get-Content $profilePath -ErrorAction SilentlyContinue >> "%TEMP%\atualizar_perfil.ps1"
echo $cleanContent = @() >> "%TEMP%\atualizar_perfil.ps1"
echo $skip = $false >> "%TEMP%\atualizar_perfil.ps1"
echo foreach($line in $content) { >> "%TEMP%\atualizar_perfil.ps1"
echo     if($line -eq '# --- INICIO SCRIPTS AUTO ---') { $skip = $true; continue } >> "%TEMP%\atualizar_perfil.ps1"
echo     if($line -eq '# --- FIM SCRIPTS AUTO ---') { $skip = $false; continue } >> "%TEMP%\atualizar_perfil.ps1"
echo     if(!$skip) { $cleanContent += $line } >> "%TEMP%\atualizar_perfil.ps1"
echo } >> "%TEMP%\atualizar_perfil.ps1"
echo. >> "%TEMP%\atualizar_perfil.ps1"
echo $cleanContent += '# --- INICIO SCRIPTS AUTO ---' >> "%TEMP%\atualizar_perfil.ps1"

:: Varre todos os arquivos .bat da pasta e cria uma funcao automatica para cada um
for %%f in ("%PASTA_ATUAL%\*.bat") do (
    if /i not "%%~nxf"=="instalar.bat" (
        echo $cleanContent += "function %%~nf { & '%PASTA_ATUAL%\%%~nxf' @args }" >> "%TEMP%\atualizar_perfil.ps1"
    )
)

echo $cleanContent += '# --- FIM SCRIPTS AUTO ---' >> "%TEMP%\atualizar_perfil.ps1"
echo Set-Content $profilePath $cleanContent >> "%TEMP%\atualizar_perfil.ps1"

:: Executa o script gerado e o apaga em seguida
powershell -ExecutionPolicy Bypass -File "%TEMP%\atualizar_perfil.ps1"
del "%TEMP%\atualizar_perfil.ps1"

echo.
echo ========================================================
echo TUDO PRONTO! 
echo Todos os scripts atuais e futuros (.bat) foram mapeados.
echo Feche e abra o CMD ou PowerShell novamente para usar.
echo ========================================================
pause