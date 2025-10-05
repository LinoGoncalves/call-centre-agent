@echo off
REM Quick Fix for PostgreSQL Image Pull Error
REM Run this if you get "unexpected end of JSON input" with postgres:15-alpine

echo ========================================
echo DOCKER POSTGRES IMAGE FIX
echo ========================================
echo.

echo Step 1: Cleaning Docker cache...
docker system prune -f
docker image prune -af

echo.
echo Step 2: Testing alternative PostgreSQL image...
docker pull postgres:15

if %ERRORLEVEL% NEQ 0 (
    echo postgres:15 failed, trying postgres:14-alpine...
    docker pull postgres:14-alpine
    
    if %ERRORLEVEL% NEQ 0 (
        echo postgres:14-alpine failed, trying postgres:13-alpine...
        docker pull postgres:13-alpine
        
        if %ERRORLEVEL% NEQ 0 (
            echo All PostgreSQL images failed to download.
            echo This indicates a network or Docker Hub connectivity issue.
            echo Please check:
            echo 1. Internet connection
            echo 2. Corporate firewall settings
            echo 3. Docker Hub access
            goto :error
        ) else (
            echo SUCCESS: postgres:13-alpine downloaded
            set POSTGRES_IMAGE=postgres:13-alpine
        )
    ) else (
        echo SUCCESS: postgres:14-alpine downloaded  
        set POSTGRES_IMAGE=postgres:14-alpine
    )
) else (
    echo SUCCESS: postgres:15 downloaded
    set POSTGRES_IMAGE=postgres:15
)

echo.
echo Step 3: Creating modified docker-compose file...
copy docker-compose.secure.yml docker-compose-working.yml

REM Replace the PostgreSQL image in the file
powershell -Command "(gc docker-compose-working.yml) -replace 'postgres:15-alpine', '%POSTGRES_IMAGE%' | Out-File -encoding UTF8 docker-compose-working.yml"

echo.
echo SUCCESS: Modified docker-compose-working.yml created with %POSTGRES_IMAGE%
echo.
echo Step 4: Starting services...
docker-compose -f docker-compose-working.yml up --build

goto :end

:error
echo.
echo ERROR: Could not resolve PostgreSQL image issue
echo Please contact support with this error log
pause
exit /b 1

:end
echo.
echo Deployment complete!
pause