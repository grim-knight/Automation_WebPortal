"""
This script allow you to install the ssm agent across a fleet of windows servers.
Make sure you copy the ssm agent installation script in a shared directory path
From where all the servers can access and copy the scripts localy to their installer folder in C drive.
"""

$SL_Location = '' # Location of the server list txt file
$SL_FileName = '' # Specify the list of servers in which the ssm agent must be installed
$srvlist = @(Get-Content -Path $SL_Location$SL_FileName'.txt')
$srvlist #.count

foreach ($srv in $srvList) {
#
        # Only for DOTNET  - folder CORE
        Write-Host -ForegroundColor Cyan "$srv"
        # Pass the path to the shared directory where the installation script is located at
        $Path = "\windows_ssm_agent_instalation_script.ps1"


        Write-Output "$srv   - Copying SSMAgent installation script to C:\installer"
        Copy-Item "$Path" \\$srv\c$\installer
        Write-Output "$srv   - Successfully copied SSMAgent installation script to C:\installer"

     
        Invoke-Command -ComputerName $srv -ThrottleLimit 1 -ScriptBlock { 
            "C:\Installer\hybridactivation_ssm.ps1"
        }
}
