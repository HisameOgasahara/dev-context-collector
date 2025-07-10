# 👨‍💻 Dev Context Collector

[![Test Linux Scripts](https://github.com/HisameOgasahara/dev-context-collector/actions/workflows/test-linux-scripts.yml/badge.svg)](https://github.com/HisameOgasahara/dev-context-collector/actions/workflows/test-linux-scripts.yml)

**LLM(Large Language Model) 기반 코딩 지원 도우미에게 정확한 개발 환경 컨텍스트를 제공하여, 코드 생성의 정확도와 효율을 극대화하는 개인용 생산성 도구입니다.**

이 프로젝트는 원격 서버, 로컬 PC, Docker 컨테이너 등 다양한 환경에서 실행 가능한 독립형 스크립트를 통해 시스템 정보를 추출하고, 직관적인 Streamlit 웹 UI를 통해 이를 손쉽게 편집하고 보강하여 최종 컨텍스트 파일(`context.json`)을 생성합니다.

---

## ✨ 핵심 기능 (Features)

*   **💻 크로스플랫폼 정보 수집**: Windows(PowerShell) 및 Linux(Bash) 환경을 모두 지원하는 독립 실행형 스크립트.
*   **🧩 모듈식 아키텍처**: 기본 시스템 정보, 네트워크 진단, Python 가상환경 등 필요한 정보를 모듈 단위로 선택적으로 수집 및 병합.
*   **✍️ 인터랙티브 편집기**: Streamlit 기반의 웹 UI를 통해 수집된 정보를 검토하고, IDE, Docker 사용 여부 등 추가적인 개발 컨텍스트를 손쉽게 입력.
*   **📋 원클릭 복사**: 최종적으로 완성된 JSON 컨텍스트를 버튼 클릭 한 번으로 클립보드에 복사하여 LLM 프롬프트에 즉시 사용 가능.
*   **🔍 디버깅 지원**: 생성된 모든 컨텍스트는 타임스탬프와 함께 `logs/` 폴더에 자동으로 저장되어 이력 추적 및 디버깅에 용이.
*   **✅ CI를 통한 안정성 확보**: GitHub Actions를 통해 Linux 쉘 스크립트의 유효성을 자동으로 검증하여 안정적인 품질 유지.

## 🚀 시작하기 (Getting Started)

### 설치 및 실행 (Installation & Usage)

1.  **리포지토리 클론:**
    ```bash
    git clone https://github.com/HisameOgasahara/dev-context-collector.git
    cd dev-context-collector
    ```

2.  **가상환경 생성 및 활성화:**
    ```bash
    # Windows (PowerShell)
    python -m venv venv
    .\venv\Scripts\Activate.ps1

    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **의존성 설치:**
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

4.  **Streamlit 애플리케이션 실행:**
    ```bash
    streamlit run src/app.py
    ```

##  workflow)

1.  **수집 (Collect):** 대상 환경(로컬, 원격 서버, Docker)에서 필요한 스크립트(`collect-base`, `collect-network` 등)를 실행합니다.
2.  **복사 (Copy):** 터미널에 출력된 JSON 텍스트 전체를 복사합니다.
3.  **편집 (Edit):** 실행된 Streamlit 앱의 해당 입력창에 붙여넣고, 추가 정보를 UI를 통해 입력합니다.
4.  **병합 및 생성 (Generate):** "모든 컨텍스트 생성 및 병합" 버튼을 클릭하여 최종 결과물을 확인하고 클립보드로 복사합니다.

## 🛠️ 기술 스택 (Tech Stack)

*   **언어**: Python 3.13, PowerShell, Bash
*   **프레임워크**: Streamlit
*   **테스팅**: Pytest, GitHub Actions
*   **데이터 형식**: JSON

---