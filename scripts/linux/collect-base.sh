#!/bin/bash
#
# 설명: Linux 환경의 필수 기본 시스템 정보만 수집합니다.

# JSON 문자열에 포함될 수 있는 특수문자(백슬래시, 큰따옴표)를 이스케이프하는 함수
escape_json_string() {
  echo "$1" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\n/\\n/g'
}

# --- 정보 수집 ---
# /etc/os-release 파일이 있는 경우 더 정확한 정보를 사용
if [ -f /etc/os-release ]; then
    OS_NAME=$(grep PRETTY_NAME /etc/os-release | cut -d'=' -f2 | tr -d '"')
    OS_VERSION="" # PRETTY_NAME에 버전 정보가 포함되는 경우가 많음
else
    OS_NAME=$(uname -s)
    OS_VERSION=$(uname -r)
fi

HOSTNAME=$(hostname)
CPU_INFO=$(grep "model name" /proc/cpuinfo | head -1 | cut -d: -f2 | sed 's/^[ \t]*//')
WORKING_DIR=$(pwd)

# --- 이스케이프 처리 ---
os_name_esc=$(escape_json_string "$OS_NAME")
os_version_esc=$(escape_json_string "$OS_VERSION")
cpu_info_esc=$(escape_json_string "$CPU_INFO")
hostname_esc=$(escape_json_string "$HOSTNAME")
working_dir_esc=$(escape_json_string "$WORKING_DIR")

# --- printf를 사용하여 안정적으로 JSON 생성 ---
printf "{\n"
printf "  \"system_info\": {\n"
printf "    \"os_type\": \"Linux\",\n"
printf "    \"os_name\": \"%s\",\n" "$os_name_esc"
printf "    \"os_version\": \"%s\",\n" "$os_version_esc"
printf "    \"hostname\": \"%s\"\n" "$hostname_esc"
printf "  },\n"
printf "  \"hardware_info\": {\n"
printf "    \"cpu\": \"%s\"\n" "$cpu_info_esc"
printf "  },\n"
printf "  \"path_info\": {\n"
printf "    \"working_directory\": \"%s\"\n" "$working_dir_esc"
printf "  }\n"
printf "}\n"