# scripts/collect-python.py (최종 안정화 버전)
import sys
import json
import importlib.metadata

def get_python_info():
    """현재 실행 중인 파이썬 환경의 정보를 수집합니다. (importlib.metadata 사용)"""
    
    # 1. 기본 파이썬 정보
    info = {
        "python_environment": {
            "python_version": sys.version,
            "python_executable": sys.executable,
            "packages": [], # 빈 리스트로 초기화
            "cuda_info": {
                "torch_available": False,
                "detail": "N/A"
            }
        }
    }

    # 2. 설치된 패키지 목록 (안정적인 방식)
    try:
        # importlib.metadata를 사용하여 설치된 패키지 목록을 가져옵니다.
        distributions = importlib.metadata.distributions()
        packages = []
        for dist in distributions:
            packages.append({"name": dist.metadata["name"], "version": dist.version})
        info["python_environment"]["packages"] = packages
    except Exception as e:
        info["python_environment"]["packages"] = f"Error getting package list using importlib.metadata: {e}"

    # 3. CUDA 정보 (PyTorch 기준)
    try:
        import torch
        
        is_available = torch.cuda.is_available()
        info["python_environment"]["cuda_info"]["torch_available"] = is_available
        
        if is_available:
            info["python_environment"]["cuda_info"]["detail"] = "PyTorch CUDA is available."
            info["python_environment"]["cuda_info"]["device_count"] = torch.cuda.device_count()
            info["python_environment"]["cuda_info"]["torch_cuda_version"] = torch.version.cuda
            device_names = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
            info["python_environment"]["cuda_info"]["gpu_names"] = device_names
        else:
            info["python_environment"]["cuda_info"]["detail"] = "PyTorch was found, but CUDA is not available."

    except ImportError:
        info["python_environment"]["cuda_info"]["detail"] = "torch is not installed in this environment."
    except Exception as e:
        info["python_environment"]["cuda_info"]["detail"] = f"An error occurred while checking torch/cuda: {e}"

    return info

if __name__ == "__main__":
    print(json.dumps(get_python_info(), indent=2))