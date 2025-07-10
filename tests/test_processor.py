# tests/test_processor.py (최종 정리 버전)
import pytest
from core.processor import parse_raw_json, merge_contexts

def test_parse_valid_json():
    """정상적인 JSON 문자열을 파싱하는 경우"""
    json_str = '{"key": "value", "number": 123}'
    data, error = parse_raw_json(json_str)
    assert error is None
    assert data is not None
    assert data["key"] == "value"

def test_parse_invalid_json():
    """문법적으로 틀린 JSON 문자열을 파싱하는 경우"""
    json_str = '{"key": "value",}'
    data, error = parse_raw_json(json_str)
    assert data is None
    assert "JSON 형식이 올바르지 않습니다" in error

def test_parse_empty_string():
    """빈 문자열을 입력하는 경우"""
    data, error = parse_raw_json("")
    assert data is None
    assert error == "입력된 내용이 없습니다. 쉘 스크립트 결과를 붙여넣어 주세요."

def test_parse_whitespace_string():
    """공백만 있는 문자열을 입력하는 경우"""
    data, error = parse_raw_json("   \n\t  ")
    assert data is None
    assert error == "입력된 내용이 없습니다. 쉘 스크립트 결과를 붙여넣어 주세요."
    
def test_parse_not_a_json_object():
    """JSON 배열 등 객체가 아닌 경우"""
    json_str = '[1, 2, 3]'
    data, error = parse_raw_json(json_str)
    assert data is None
    assert "최상위 요소는 JSON 객체(딕셔너리)여야 합니다" in error

def test_merge_contexts():
    """두 개의 유효한 딕셔너리를 병합하는 경우"""
    context1 = {"system": {"os": "Windows"}}
    context2 = {"network": {"ping": "OK"}}
    merged = merge_contexts(context1, context2)
    assert "system" in merged
    assert "network" in merged
    assert merged["system"]["os"] == "Windows"

def test_merge_with_none_and_empty():
    """None이나 빈 딕셔너리가 포함된 경우"""
    context1 = {"system": {"os": "Windows"}}
    context2 = None
    context3 = {}
    merged = merge_contexts(context1, context2, context3)
    assert merged == context1