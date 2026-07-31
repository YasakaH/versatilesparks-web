try {
    Copy-Item "C:\Users\varas\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Network\Cookies" "C:\Users\varas\personalities\_brave_cookies.db" -Force
    Write-Output "Copied successfully"
} catch {
    Write-Output ("Error: " + $_.Exception.Message)
}
