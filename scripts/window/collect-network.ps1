# scripts/window/collect-network.ps1
#
# 설명: Windows 환경의 네트워크 진단 정보(ipconfig, ping)만 수집합니다.

$ErrorActionPreference = "SilentlyContinue"
function Escape-JsonString { param($String)
    $escaped = $String -replace '\\', '\\' -replace '"', '\"' -replace "`r`n", '\n' -replace "`n", '\n'
    return $escaped
}

# --- 정보 수집 ---
$raw_ipconfig_output = ipconfig | Out-String
$raw_ping_output = ping 8.8.8.8 -n 4 | Out-String

# --- 이스케이프 처리 ---
$ipconfig_output = Escape-JsonString -String $raw_ipconfig_output
$ping_output = Escape-JsonString -String $raw_ping_output

# --- JSON 생성 ---
$json_output = @"
{
  "network_info": {
    "ipconfig_output": "$ipconfig_output",
    "ping_google_dns": "$ping_output"
  }
}
"@
echo $json_output