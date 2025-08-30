# PowerShell script to generate a strong JWT secret key

function Generate-StrongKey {
    param (
        [int]$Length = 64
    )
    
    # Generate random bytes
    $randomBytes = New-Object byte[] $Length
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $rng.GetBytes($randomBytes)
    
    # Convert to URL-safe base64 string
    $base64 = [Convert]::ToBase64String($randomBytes)
    $base64 = $base64.Replace("+", "-").Replace("/", "_").Replace("=", "")
    
    return $base64
}

function Update-EnvFile {
    param (
        [string]$Key
    )
    
    $envPath = Join-Path -Path $PSScriptRoot -ChildPath "../.env"
    $envExamplePath = Join-Path -Path $PSScriptRoot -ChildPath "../.env.example"
    
    # Check if .env file exists
    if (Test-Path $envPath) {
        # Read existing .env file
        $content = Get-Content $envPath -Raw
        
        # Check if JWT_SECRET_KEY already exists
        if ($content -match "JWT_SECRET_KEY=.*") {
            # Replace existing key
            $content = $content -replace "JWT_SECRET_KEY=.*", "JWT_SECRET_KEY=$Key"
        } else {
            # Add key if it doesn't exist
            $content += "`nJWT_SECRET_KEY=$Key"
        }
        
        # Write updated content back to .env file
        Set-Content -Path $envPath -Value $content
    } else {
        # Create new .env file if it doesn't exist
        # First check if .env.example exists and copy from it
        if (Test-Path $envExamplePath) {
            $content = Get-Content $envExamplePath -Raw
            
            # Replace or add JWT_SECRET_KEY
            if ($content -match "JWT_SECRET_KEY=.*") {
                $content = $content -replace "JWT_SECRET_KEY=.*", "JWT_SECRET_KEY=$Key"
            } else {
                $content += "`nJWT_SECRET_KEY=$Key"
            }
            
            Set-Content -Path $envPath -Value $content
        } else {
            # Create minimal .env file
            Set-Content -Path $envPath -Value "JWT_SECRET_KEY=$Key"
        }
    }
}

# Generate a strong key
$key = Generate-StrongKey
Write-Host "Generated JWT secret key: $key"

# Update .env file
Update-EnvFile -Key $key
Write-Host "Updated .env file with new JWT secret key"