# 🦙 로컬 구동형 AI 음성 메모 2단계 분석 및 상세 요약기

내 컴퓨터의 자원만을 활용하여 **100% 무료 및 오프라인**으로 작동하는 로컬 음성 인식(STT) 및 AI 상세 보고서 생성 프로그램임. 대용량 통화 녹음 파일 처리 시 발생하는 콘텍스트 제한 및 뇌피셜 문제를 해결하기 위해 **받아쓰기(STT)**와 **AI 요약** 파이프라인을 2개의 스크립트로 분리하여 안정성과 정확성을 극대화함.

---

## ✨ 주요 특징 및 파이프라인

1. **1단계: `1_stt_transcriber.py` (음성 ➔ 텍스트 변환)**
   - OpenAI Whisper (Small Model)를 로컬에서 구동하여 30분 이상의 대용량 한국어 음성을 누락 없이 100% 텍스트 본문으로 추출함.
   - LLM 연산 부하를 줄이기 위해 타임라인 연산을 배제하고 순수 대화 원본만 복원하여 속도를 최적화함.

2. **2단계: `2_ai_summarizer.py` (텍스트 ➔ 팩트 기반 상세 보고서)**
   - 로컬 LLM(Ollama Gemma2)을 활용하여 저장된 텍스트 본문을 정밀 분석함.
   - 추상적인 감상문 표현을 철저히 배제하고, 자산(차량), 보험금/행정 서류, 사업 마무리 사항 및 화자별 Action Plan을 팩트 위주로 분류하여 비즈니스 규격 리포트를 생성함.

---

## 🛠 기술 스택

- **Language**: Python 3.12+
- **STT Engine**: OpenAI Whisper (Small Model)
- **LLM Engine**: Ollama (Gemma2 표준 모델)
- **Environment**: VS Code / Virtual Environment (venv)

---

## 🚀 실행 방법

### 1. 가상환경 세팅 및 의존성 설치
python3 -m venv .venv
source .venv/bin/activate
pip install openai-whisper requests tqdm

### 2. 파이프라인 구동 순서
# 1단계: 음성 파일 받아쓰기 실행 (SavedResults/ 폴더 내에 원본본문 생성)
python 1_stt_transcriber.py

# 2단계: 생성된 본문을 바탕으로 AI 상세 보고서 생성 (SavedResults/ 폴더 내에 최종보고서 생성)
python 2_ai_summarizer.py
