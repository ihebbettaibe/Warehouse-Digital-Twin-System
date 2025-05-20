# Start-WarehouseDigitalTwin.ps1
# This script starts the Warehouse Digital Twin system

Write-Host "Starting Warehouse Digital Twin System..." -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Check Docker status
Write-Host "Checking Docker status..." -ForegroundColor White
try {
    $dockerStatus = docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Docker is NOT running!" -ForegroundColor Red
        Write-Host "Please start Docker Desktop first and wait for it to initialize." -ForegroundColor Yellow
        
        $startDocker = Read-Host "Would you like to try starting Docker Desktop now? (y/n)"
        if ($startDocker -eq "y") {
            try {
                Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
                Write-Host "Docker Desktop launch requested. Please wait for it to initialize..." -ForegroundColor Yellow
                Write-Host "This script will wait for 60 seconds..." -ForegroundColor Yellow
                
                # Wait for Docker to start
                $timeout = 60
                for ($i = 1; $i -le $timeout; $i++) {
                    Write-Progress -Activity "Waiting for Docker to start" -Status "$i / $timeout seconds elapsed" -PercentComplete ($i / $timeout * 100)
                    Start-Sleep -Seconds 1
                    
                    # Check if Docker is running now
                    if ((docker info 2>&1) -and $LASTEXITCODE -eq 0) {
                        Write-Progress -Activity "Waiting for Docker to start" -Completed
                        Write-Host "Docker is now running!" -ForegroundColor Green
                        break
                    }
                    
                    if ($i -eq $timeout) {
                        Write-Progress -Activity "Waiting for Docker to start" -Completed
                        Write-Host "Timeout reached. Docker may not be fully initialized yet." -ForegroundColor Red
                        Write-Host "Please try again in a few moments." -ForegroundColor Yellow
                        exit 1
                    }
                }
            }
            catch {
                Write-Host "Error trying to start Docker Desktop. Please start it manually." -ForegroundColor Red
                exit 1
            }
        } else {
            Write-Host "Exiting. Please start Docker Desktop manually and try again." -ForegroundColor Yellow
            exit 1
        }
    } else {
        Write-Host "Docker is running!" -ForegroundColor Green
    }
}
catch {
    Write-Host "Error checking Docker status. Please ensure Docker Desktop is installed." -ForegroundColor Red
    exit 1
}

# Start the system with docker-compose
Write-Host "`nStarting all services with docker-compose..." -ForegroundColor White
docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nAll services are starting!" -ForegroundColor Green
    
    # Wait for services to initialize
    Write-Host "`nWaiting for services to initialize. This may take a few minutes..." -ForegroundColor Yellow
    Start-Sleep -Seconds 15
    
    # Show running containers
    Write-Host "`nRunning containers:" -ForegroundColor White
    docker-compose ps
    
    # Provide helpful information
    Write-Host "`nAccess the dashboard at: http://localhost:5000" -ForegroundColor Cyan
    Write-Host "Access NiFi UI at: http://localhost:8080/nifi" -ForegroundColor Cyan
    Write-Host "`nImportant note: NiFi may take 2-3 minutes to fully initialize." -ForegroundColor Yellow
    
    # Offer to show logs
    $showLogs = Read-Host "`nWould you like to follow the logs? (y/n)"
    if ($showLogs -eq "y") {
        Write-Host "`nShowing logs (press Ctrl+C to exit log view)..." -ForegroundColor Yellow
        docker-compose logs -f
    } else {
        Write-Host "`nYou can check service status with: .\Check-Services.ps1" -ForegroundColor White
        Write-Host "You can view logs later with: docker-compose logs -f" -ForegroundColor White
    }
} else {
    Write-Host "`nFailed to start services. Check for errors above." -ForegroundColor Red
}
