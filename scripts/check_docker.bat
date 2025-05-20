@echo off
echo Checking Docker status...

docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker does not appear to be running.
    echo.
    echo Please make sure Docker Desktop is installed and running.
    echo.
    echo 1. Look for the Docker Desktop icon in your system tray
    echo 2. If not running, launch Docker Desktop from your Start menu
    echo 3. Wait for Docker to fully initialize (look for the green "Docker is running" message)
    echo 4. Then try docker-compose again with: docker-compose up
    echo.
    pause
    exit /b 1
) else (
    echo Docker is running properly.
    echo.
    echo You can now run: docker-compose up
    echo.
    pause
)
