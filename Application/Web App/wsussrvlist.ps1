Start-Transcript -Path '' -Append
$srv = ''
$temp = $args[0]
$adminUsername = ""
$adminPassword = ConvertTo-SecureString "" -AsPlainText -Force
$adminCreds = [PSCredential]::new($adminUsername, $adminPassword)
Write-Host "Copying the wsuscms powershell script to WSUS Server"
Copy-Item "path to script on remote computer here \wsuscmd_1.ps1" \\$srv\c$\installer
Write-Host "Copy successful"
Invoke-Command -ComputerName $srv -credential $adminCreds -ArgumentList $temp -ThrottleLimit 1 -ScriptBlock { 
    Set-ExecutionPolicy RemoteSigned -Force 
    & "C:\Installer\wsuscmd.ps1" $using:temp -Verb RunAs
    #Start-Process -FilePath "powershell" -ArgumentList "C:\installer\wsuscmd.ps1",$using:temp -Verb RunAs
    Write-Host "WSUS commands ran successfully"
}

Copy-Item "csv files source here" "destination directory should be same flask app code"
Write-Host "Copying csv complete"
Stop-Transcript