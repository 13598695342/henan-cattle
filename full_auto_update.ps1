# 河南牛价数据自动更新 PowerShell 脚本

$ErrorActionPreference = "Continue"

Write-Host "========================================="
Write-Host "  Cattle Data - Full Auto Update"
Write-Host "========================================="
Write-Host ""

# 设置 Git 使用 SSH 密钥
$env:GIT_SSH_COMMAND = "ssh -i `"$env:USERPROFILE\.ssh\id_rsa`" -o StrictHostKeyChecking=no"

# 切换到脚本目录
Set-Location $PSScriptRoot

Write-Host "[1/5] Updating data..."
$result = python data_update.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Update failed!"
    exit 1
}
Write-Host "  OK - Data updated!"

Write-Host ""
Write-Host "[2/5] Commit changes..."
git add -A
git commit -m "Auto update $(Get-Date -Format 'yyyy/MM/dd HH:mm:ss')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  No changes to commit"
} else {
    Write-Host "  OK - Committed"
}

Write-Host ""
Write-Host "[3/5] Sync GitHub..."
git pull origin master --rebase 2>$null
git push origin master 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Warning: GitHub push failed"
} else {
    Write-Host "  OK - Synced with GitHub"
}

Write-Host ""
Write-Host "[4/5] Sync Gitee..."
git pull gitee master --rebase 2>$null
git push gitee master 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Warning: Gitee push failed"
} else {
    Write-Host "  OK - Synced with Gitee"
}

Write-Host ""
Write-Host "[5/5] Finished!"
Write-Host ""
Write-Host "Website: https://dulcet-daifuku-4f5ffe.netlify.app/"

exit 0
