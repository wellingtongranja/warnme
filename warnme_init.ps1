# Function to prompt for input and mask sensitive information
function Prompt-Input {
    param (
        [string]$Prompt,
        [string]$VarName,
        [bool]$IsSecret
    )

    if ($IsSecret) {
        $input = Read-Host -Prompt $Prompt -AsSecureString | ConvertFrom-SecureString -AsPlainText
    } else {
        $input = Read-Host -Prompt $Prompt
    }

    $env:$VarName = $input
    Add-Content -Path .env -Value "$VarName=`"$input`""
}

# Clear the .env file
Clear-Content -Path .env

# Prompt for EMAIL configuration
Write-Host "Please enter the EMAIL configuration:"
Prompt-Input -Prompt "SMTP Server" -VarName "WARNME_EMAIL_SMTP_SERVER" -IsSecret $false
Prompt-Input -Prompt "SMTP Port" -VarName "WARNME_EMAIL_SMTP_PORT" -IsSecret $false
Prompt-Input -Prompt "Sender Email" -VarName "WARNME_EMAIL_SENDER_EMAIL" -IsSecret $false
Prompt-Input -Prompt "Sender Password" -VarName "WARNME_EMAIL_SENDER_PASSWORD" -IsSecret $true

# Prompt for DB configuration
Write-Host "Please enter the DB configuration:"
Prompt-Input -Prompt "DB User" -VarName "WARNME_DB_USER" -IsSecret $false
Prompt-Input -Prompt "DB Password" -VarName "WARNME_DB_PASSWORD" -IsSecret $true
Prompt-Input -Prompt "DB Account" -VarName "WARNME_DB_ACCOUNT" -IsSecret $false
Prompt-Input -Prompt "DB Warehouse" -VarName "WARNME_DB_WAREHOUSE" -IsSecret $false
Prompt-Input -Prompt "DB Database" -VarName "WARNME_DB_DATABASE" -IsSecret $false
Prompt-Input -Prompt "DB Schema" -VarName "WARNME_DB_SCHEMA" -IsSecret $false
Prompt-Input -Prompt "DB Role Name" -VarName "WARNME_DB_ROLENAME" -IsSecret $false

# Prompt for TWILIO configuration (optional)
$configure_twilio = Read-Host -Prompt "Do you want to configure Twilio? (y/n)"
if ($configure_twilio -eq "y") {
    Write-Host "Please enter the TWILIO configuration:"
    Prompt-Input -Prompt "Twilio Account SID" -VarName "WARNME_TWILIO_ACCOUNT_SID" -IsSecret $false
    Prompt-Input -Prompt "Twilio Auth Token" -VarName "WARNME_TWILIO_AUTH_TOKEN" -IsSecret $true
    Prompt-Input -Prompt "Twilio From Phone Number" -VarName "WARNME_TWILIO_FROM_PHONE_NUMBER" -IsSecret $false
}

Write-Host "Environment variables set and saved to .env file."