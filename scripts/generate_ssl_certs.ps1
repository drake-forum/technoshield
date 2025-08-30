# PowerShell script to generate self-signed SSL certificates for TECHNOSHIELD

$certsDir = "..\frontend\ssl"

# Create directory for certificates if it doesn't exist
if (-not (Test-Path $certsDir)) {
    New-Item -ItemType Directory -Path $certsDir -Force | Out-Null
}

# Generate a self-signed certificate
$cert = New-SelfSignedCertificate -DnsName "localhost" -CertStoreLocation "Cert:\LocalMachine\My" -NotAfter (Get-Date).AddDays(365) -KeyAlgorithm RSA -KeyLength 2048

# Export the certificate to a file
$certPassword = ConvertTo-SecureString -String "technoshield" -Force -AsPlainText
$certPath = Join-Path -Path $certsDir -ChildPath "technoshield.pfx"
Export-PfxCertificate -Cert $cert -FilePath $certPath -Password $certPassword | Out-Null

# Export the public key to a .crt file
$crtPath = Join-Path -Path $certsDir -ChildPath "technoshield.crt"
Export-Certificate -Cert $cert -FilePath $crtPath | Out-Null

# Export the private key to a .key file (for Nginx)
$keyPath = Join-Path -Path $certsDir -ChildPath "technoshield.key"
$privateKeyBytes = [System.Security.Cryptography.X509Certificates.RSACertificateExtensions]::GetRSAPrivateKey($cert).Key.Export([System.Security.Cryptography.CngKeyBlobFormat]::Pkcs8PrivateBlob)
[System.IO.File]::WriteAllBytes($keyPath, $privateKeyBytes)

Write-Host "SSL certificates generated successfully in $certsDir"
Write-Host "  - technoshield.pfx: Certificate with private key (password: technoshield)"
Write-Host "  - technoshield.crt: Public certificate"
Write-Host "  - technoshield.key: Private key"