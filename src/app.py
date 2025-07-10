# src/app.py (파이썬 정보 수집 기능 추가)

import streamlit as st
import pyperclip
import json
import os
import subprocess
from core.processor import parse_raw_json, merge_contexts

# --- 1. 페이지 설정 및 초기화 ---
st.set_page_config(page_title="Dev Context Collector", layout="wide")
st.title("👨‍💻 LLM 개발 환경 컨텍스트 수집기")

if 'final_context' not in st.session_state:
    st.session_state.final_context = None
if 'python_json_output' not in st.session_state:
    st.session_state.python_json_output = ""


# --- 2. 모듈식 정보 입력 UI ---
st.header("1. 정보 붙여넣기")
col1, col2 = st.columns(2)

with col1:
    base_json_input = st.text_area(
        "**필수:** `collect-base.ps1` 결과를 여기에 붙여넣으세요.",
        height=250, help="OS, CPU, 경로 등 핵심 정보를 담습니다."
    )
with col2:
    network_json_input = st.text_area(
        "**(선택) 네트워크:** `collect-network.ps1` 결과를 여기에 붙여넣으세요.",
        height=250, help="ipconfig, ping 등 네트워크 진단 정보가 필요할 때 사용합니다."
    )

st.divider()

# --- 3. 파이썬 환경 정보 수집 UI ---
st.header("2. 파이썬 환경 정보 (선택)")

py_exe_path = st.text_input(
    "대상 가상환경의 python.exe 경로",
    placeholder=r"예: C:\Users\MyUser\projects\my-dl-project\venv\Scripts\python.exe",
    help="정보를 수집할 프로젝트의 가상환경에 있는 파이썬 실행 파일의 전체 경로를 입력하세요."
)

if st.button("해당 파이썬 환경 정보 가져오기"):
    app_dir = os.path.dirname(__file__)
    script_path = os.path.abspath(os.path.join(app_dir, '..', 'scripts', 'collect-python.py'))
    if py_exe_path and os.path.exists(py_exe_path) and os.path.exists(script_path):
        try:
            with st.spinner("파이썬 환경 정보를 수집하는 중... (torch 로딩 시 시간이 걸릴 수 있습니다)"):
                result = subprocess.run(
                    [py_exe_path, script_path],
                    capture_output=True, text=True, check=True, encoding='utf-8'
                )
            st.session_state.python_json_output = result.stdout.strip()
            st.toast("✅ 파이썬 환경 정보를 성공적으로 가져왔습니다!")
        except subprocess.CalledProcessError as e:
            st.error(f"스크립트 실행 중 오류 발생:\n{e.stderr}")
        except Exception as e:
            st.error(f"알 수 없는 오류 발생: {e}")
    else:
        st.warning("유효한 파이썬 경로와 `collect-python.py` 스크립트가 모두 필요합니다.")

python_json_input = st.text_area(
    "**파이썬 정보 결과:**",
    value=st.session_state.python_json_output,
    height=250
)

st.divider()

# --- 4. 사용자 직접 입력 UI ---
st.header("3. 추가 정보 입력")
# ... (이전과 동일한 코드)
col1, col2 = st.columns(2)
with col1:
    st.subheader("개발 환경")
    ide = st.selectbox("IDE", ["Cursor", "VS Code", "Visual Studio", "Jupyter Notebook", "Other"])
    shell = st.selectbox("Shell", ["PowerShell", "CMD", "Git Bash", "WSL (Bash)", "Other"])
    use_docker = st.toggle("Docker 사용 여부", value=False)
with col2:
    st.subheader("DevOps 및 인프라")
    ci_provider = st.selectbox("CI 도구", ["GitHub Actions", "GitLab CI", "Jenkins", "None", "Other"])
    deployment_target = st.selectbox("배포 환경", ["AWS", "GCP", "Azure", "Cloudflare", "Hugging Face", "Streamlit Cloud", "None", "Other"])
    github_account = st.selectbox("GitHub 계정", ["https://github.com/HisameOgasahara", "https://github.com/AriannaHeartbell", "직접 입력"])
    if github_account == "직접 입력":
        github_account = st.text_input("GitHub 계정 URL을 입력하세요:")

# src/app.py의 "최종 병합 및 출력" 섹션 전체를 교체하세요.

# --- 5. 최종 병합 및 출력 ---
st.divider()
st.header("4. 최종 결과 생성 및 확인")

if st.button("모든 컨텍스트 생성 및 병합", type="primary"):
    # 항상 최종 컨텍스트를 초기화
    st.session_state.final_context = None
    
    # 파싱 시도 및 성공한 데이터만 리스트에 수집
    valid_contexts = []
    
    # 1. 기본 정보 파싱
    base_data, base_error = parse_raw_json(base_json_input)
    if base_data:
        valid_contexts.append(base_data)
    elif base_error != "입력된 내용이 없습니다. 쉘 스크립트 결과를 붙여넣어 주세요.": # 진짜 오류만 표시
        st.warning(f"⚠️ 기본 정보 파싱 실패: {base_error}")

    # 2. 네트워크 정보 파싱
    network_data, network_error = parse_raw_json(network_json_input)
    if network_data:
        valid_contexts.append(network_data)
    elif network_error != "입력된 내용이 없습니다. 쉘 스크립트 결과를 붙여넣어 주세요.":
        st.warning(f"⚠️ 네트워크 정보 파싱 실패: {network_error}")

    # 3. 파이썬 정보 파싱
    python_data, python_error = parse_raw_json(python_json_input)
    if python_data:
        valid_contexts.append(python_data)
    elif python_error != "입력된 내용이 없습니다. 쉘 스크립트 결과를 붙여넣어 주세요.":
        st.warning(f"⚠️ 파이썬 정보 파싱 실패: {python_error}")

    # 4. 사용자 직접 입력 정보 추가
    user_edits = {
        "user_development_environment": {"ide": ide, "shell": shell},
        "devops_and_infrastructure_plan": {"useDocker": use_docker, "ciProvider": ci_provider, "deploymentTarget": deployment_target, "gitRepoURL": github_account}
    }
    valid_contexts.append(user_edits)

    # 5. 성공적으로 파싱된 모든 컨텍스트 병합
    if valid_contexts:
        st.session_state.final_context = merge_contexts(*valid_contexts) # Unpacking the list
        st.success("컨텍스트 병합 완료!")

        # --- 로그 파일 생성 로직 ---
        from datetime import datetime
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file_path = os.path.join(log_dir, f"final_context_{timestamp}.json")
        
        try:
            with open(log_file_path, "w", encoding="utf-8") as f:
                json.dump(st.session_state.final_context, f, indent=2, ensure_ascii=False)
            st.info(f"결과가 로그 파일에 저장되었습니다: `{log_file_path}`")
        except Exception as e:
            st.error(f"로그 파일 저장 중 오류 발생: {e}")
            
    else:
        st.error("병합할 유효한 데이터가 하나도 없습니다.")


# --- 최종 결과 표시 로직 (수정 없음) ---
if st.session_state.final_context:
    st.json(st.session_state.final_context)
    if st.button("최종 컨텍스트 클립보드로 복사"):
        pyperclip.copy(json.dumps(st.session_state.final_context, indent=2, ensure_ascii=False))
        st.toast("✅ 최종 컨텍스트가 클립보드에 복사되었습니다!")
else:
    st.info("정보를 입력/선택하고 '모든 컨텍스트 생성 및 병합' 버튼을 눌러주세요.")