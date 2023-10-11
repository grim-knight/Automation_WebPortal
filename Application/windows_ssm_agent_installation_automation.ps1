"""
This script allow you to install the ssm agent across a fleet of windows servers.
Make sure you copy the ssm agent installation script in a shared directory path
From where all the servers can access and copy the scripts localy to their installer folder in C drive.
"""

$SL_Location = ''
$SL_FileName = ''
$srvlist = @(Get-Content -Path $SL_Location$SL_FileName'.txt')
$srvlist #.count

foreach ($srv in $srvList) {

        Write-Host -ForegroundColor Cyan "$srv"

        $Path = ""

        Write-Output "$srv   - Copying SSMAgent installation script to C:\installer"
        Copy-Item "$Path" \\$srv\c$\installer
        Write-Output "$srv   - Successfully copied SSMAgent installation script to C:\installer"

        Invoke-Command -ComputerName $srv -ThrottleLimit 1 -ScriptBlock { 
            Start-Process -FilePath "powershell" -ArgumentList "C:\installer\hybridactivation_ssm.ps1" -Verb RunAs -NoNewWindow
        }
}
