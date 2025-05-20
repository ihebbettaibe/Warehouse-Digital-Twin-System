# Check if Docker is running
function Test-DockerRunning {
    try {
        $result = docker info 2>&1
        $isRunning = $LASTEXITCODE -eq 0
        return $isRunning
    }
    catch {
        return $false
    }
}

# Main execution
Write-Host "Checking Docker status..." -ForegroundColor Cyan

if (Test-DockerRunning) {
    Write-Host "Docker is running properly." -ForegroundColor Green
    Write-Host ""
    Write-Host "You can run the following command to start the system:" -ForegroundColor White
    Write-Host "docker-compose up" -ForegroundColor Yellow
} else {
    Write-Host "Docker does not appear to be running." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please make sure Docker Desktop is installed and running:" -ForegroundColor White
    Write-Host "1. Look for the Docker Desktop icon in your system tray" -ForegroundColor White
    Write-Host "2. If not running, launch Docker Desktop from your Start menu" -ForegroundColor White
    Write-Host "3. Wait for Docker to fully initialize (look for the green 'Docker is running' message)" -ForegroundColor White
    Write-Host "4. Then try docker-compose again with: docker-compose up" -ForegroundColor Yellow
    
    $launchDocker = Read-Host "Would you like to attempt to start Docker Desktop now? (y/n)"
    if ($launchDocker -eq "y") {
        Write-Host "Attempting to start Docker Desktop..." -ForegroundColor Cyan
        try {
            Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
            Write-Host "Docker Desktop launch requested. Please wait for Docker to initialize." -ForegroundColor Yellow
            Write-Host "This may take a few minutes. Watch for the Docker icon in your system tray." -ForegroundColor White
        }
        catch {
            Write-Host "Unable to start Docker automatically. Please start it manually." -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
