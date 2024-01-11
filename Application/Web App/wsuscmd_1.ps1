# This file should be in a shared directory for copy or place it in the WSUS server C:\Installer
$temp = $args[0]
Write-Host $temp
Write-Host "PowerShell script is running with update status: $temp"
Get-WsusComputer -ComputerTargetGroups AWS-Stage -ComputerUpdateStatus $temp | Export-Csv '' -NoTypeInformation
Get-WsusComputer -ComputerTargetGroups AWS-Prod -ComputerUpdateStatus $temp | Export-Csv '' -NoTypeInformation
Get-WsusComputer -ComputerTargetGroups AWS-Infra-InfoSec -ComputerUpdateStatus $temp | Export-Csv '' -NoTypeInformation
Get-WsusComputer -ComputerTargetGroups AWS-Demo -ComputerUpdateStatus $temp | Export-Csv '' -NoTypeInformation
Write-Host "Completed remote execution"
Write-Host "PowerShell script completed"