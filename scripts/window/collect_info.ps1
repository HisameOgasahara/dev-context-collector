# scripts/window/collect-base.ps1
#
# 설명: Windows 환경의 필수 기본 시스템 정보만 수집합니다. (짧고 간결함)

$ErrorActionPreference = "SilentlyContinue"
function Escape-JsonString { param($String)
    $escaped = $String -replace '\\', '\\' -replace '"', '\"' -replace "`r`n", '\n' -replace "`n", '\n'
    return $escaped
}

# --- 정보 수집 ---
$raw_os_name = (Get-ComputerInfo).OsName
$raw_os_version = (Get-ComputerInfo).OsVersion
$raw_cpu_info = (Get-CimInstance -ClassName Win32_Processor).Name.Trim()
$raw_hostname = $env:COMPUTERNAME
$raw_working_dir = (Get-Location).Path

# --- 이스케이프 처리 ---
$os_name = Escape-JsonString -String $raw_os_name
$os_version = Escape-JsonString -String $raw_os_version
$cpu_info = Escape-JsonString -String $raw_cpu_info
$hostname = Escape-JsonString -String $raw_hostname
$working_dir = Escape-JsonString -String $raw_working_dir

# --- JSON 생성 ---
$json_output = @"
{
  "system_info": {
    "os_type": "Windows",
    "os_name": "$os_name",
    "os_version": "$os_version",
    "hostname": "$hostname"
  },
  "hardware_info": {
    "cpu": "$cpu_info"
  },
  "path_info": {
    "working_directory": "$working_dir"
  }
}
"@
echo $json_output