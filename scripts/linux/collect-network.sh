#!/bin/bash
#
# 설명: Linux 환경의 네트워크 진단 정보(ip addr, ping)만 수집합니다.

# JSON 문자열에 포함될 수 있는 특수문자(백슬래시, 큰따옴표, 줄바꿈)를 이스케이프하는 함수
escape_json_string() {
  echo "$1" | sed 's/\\/\\\\/g; s/"/\\"/g' | awk '{printf "%s\\n", $0}' | sed '$ s/\\n$//'
}

# --- 정보 수집 ---
# ifconfig 보다 최신인 ip addr 사용. 없는 경우 ifconfig 시도.
if command -v ip &> /dev/null; then
    IPCONFIG_OUTPUT=$(ip addr)
else
    IPCONFIG_OUTPUT=$(ifconfig)
fi
PING_OUTPUT=$(ping -c 4 8.8.8.8) # -c 4는 4회 실행

# --- 이스케이프 처리 ---
ipconfig_output_esc=$(escape_json_string "$IPCONFIG_OUTPUT")
ping_output_esc=$(escape_json_string "$PING_OUTPUT")

# --- printf를 사용하여 안정적으로 JSON 생성 ---
printf "{\n"
printf "  \"network_info\": {\n"
printf "    \"ipconfig_output\": \"%s\",\n" "$ipconfig_output_esc"
printf "    \"ping_google_dns\": \"%s\"\n" "$ping_output_esc"
printf "  }\n"
printf "}\n"