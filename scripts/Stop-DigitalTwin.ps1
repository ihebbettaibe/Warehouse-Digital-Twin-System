# Stop-WarehouseDigitalTwin.ps1
# This script stops the Warehouse Digital Twin system

Write-Host "Stopping Warehouse Digital Twin System..." -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Check Docker status
Write-Host "Checking Docker status..." -ForegroundColor White
try {
    $dockerStatus = docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Docker is NOT running!" -ForegroundColor Red
        Write-Host "Services might already be stopped." -ForegroundColor Yellow
        
        $proceed = Read-Host "Do you want to proceed anyway? (y/n)"
        if ($proceed -ne "y") {
            Write-Host "Exiting without stopping services." -ForegroundColor Yellow
            exit 1
        }
    } else {
        Write-Host "Docker is running!" -ForegroundColor Green
    }
}
catch {
    Write-Host "Error checking Docker status." -ForegroundColor Red
    $proceed = Read-Host "Do you want to proceed anyway? (y/n)"
    if ($proceed -ne "y") {
        exit 1
    }
}

# Stop the system with docker-compose
Write-Host "`nStopping all services with docker-compose..." -ForegroundColor White
docker-compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nAll services have been stopped!" -ForegroundColor Green
    
    # Offer to show running containers
    $listContainers = Read-Host "`nWould you like to list any remaining containers? (y/n)"
    if ($listContainers -eq "y") {
        Write-Host "`nRunning containers:" -ForegroundColor White
        docker ps
    }
    
    # Ask if they want to remove volumes as well
    $removeVolumes = Read-Host "`nDo you want to remove all related Docker volumes? (y/n)"
    if ($removeVolumes -eq "y") {
        Write-Host "`nRemoving Docker volumes..." -ForegroundColor Yellow
        docker-compose down -v
        Write-Host "`nVolumes have been removed." -ForegroundColor Green
    }
} else {
    Write-Host "`nFailed to stop services. Check for errors above." -ForegroundColor Red
}
