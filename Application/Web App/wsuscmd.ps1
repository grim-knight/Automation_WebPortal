Start-Transcript -Path 'C:\installer\log.txt' -Append
$temp = $args[0]
Write-Host $temp
$srv = "" # WSUS server name
$username = "" # domain\service_acc
$passcode = "" # password for the service acc
$credentials = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $username, (ConvertTo-SecureString -String $passcode -AsPlainText -Force)
Invoke-Command -ComputerName $srv -Credential $credentials -ArgumentList $temp -ThrottleLimit 1 -ScriptBlock {
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Force 
    Write-Host "PowerShell script is running with update status: $using:temp"
    # The export should be in the same directory as the py flask app code
    Get-WsusComputer -ComputerTargetGroups Stage -ComputerUpdateStatus $using:temp | Export-Csv '' -NoTypeInformation
    Get-WsusComputer -ComputerTargetGroups Prod -ComputerUpdateStatus $using:temp | Export-Csv '' -NoTypeInformation
    Get-WsusComputer -ComputerTargetGroups Infra -ComputerUpdateStatus $using:temp | Export-Csv '' -NoTypeInformation
    Write-Host "PowerShell script completed"
}
# Copy-Item 'C:\temp.csv' .\dashboard
Stop-Transcript
