# src/core/processor.py
import json
import logging
from typing import Dict, Any, Tuple

# 로깅 설정 (나중에 파일로 저장하도록 구성 가능)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_raw_json(json_string: str) -> Tuple[Dict[str, Any] | None, str | None]:
    """
    사용자가 입력한 원시 JSON 문자열을 파싱합니다.

    Args:
        json_string: 사용자가 st.text_area에 붙여넣은 텍스트.

    Returns:
        A tuple containing:
        - 파싱된 딕셔너리 객체 (성공 시), None (실패 시)
        - 에러 메시지 문자열 (실패 시), None (성공 시)
    """
    if not json_string or not json_string.strip():
        return None, "입력된 내용이 없습니다. 쉘 스크립트 결과를 붙여넣어 주세요."

    try:
        data = json.loads(json_string)
        if not isinstance(data, dict):
            raise TypeError("최상위 요소는 JSON 객체(딕셔너리)여야 합니다.")
        logging.info("JSON 파싱에 성공했습니다.")
        return data, None
    except json.JSONDecodeError as e:
        error_msg = f"JSON 형식이 올바르지 않습니다: {e}"
        logging.error(error_msg)
        return None, error_msg
    except TypeError as e:
        error_msg = f"데이터 구조가 올바르지 않습니다: {e}"
        logging.error(error_msg)
        return None, error_msg
    except Exception as e:
        error_msg = f"알 수 없는 오류가 발생했습니다: {e}"
        logging.error(error_msg, exc_info=True)
        return None, error_msg
    
# src/core/processor.py 에 아래 함수를 추가하세요.

def merge_contexts(*contexts: dict) -> dict:
    """
    여러 딕셔너리 컨텍스트를 하나로 병합합니다.

    Args:
        *contexts: 병합할 하나 이상의 딕셔너리.

    Returns:
        병합된 단일 딕셔너리.
    """
    merged_context = {}
    for context in contexts:
        if context and isinstance(context, dict):
            merged_context.update(context)
    logging.info(f"병합 완료. 최종 키: {list(merged_context.keys())}")
    return merged_context