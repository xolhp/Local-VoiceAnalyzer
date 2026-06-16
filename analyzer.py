import os
import whisper
import requests
from tqdm import tqdm

def transcribe_and_summarize(audio_file_path, output_dir_path):
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
        print(f"-> 지정하신 저장 경로가 존재하지 않아 새로 생성했습니다: {output_dir_path}")

    base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
    output_file_path = os.path.join(output_dir_path, f"{base_name}_분석결과.txt")

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" 1단계: 로컬 Whisper 모델로 음성 인식 (STT) 시작")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    print("-> Whisper 인공지능 모델을 로드하고 있습니다...")
    # 30분 통화 분량을 완전히 한국어로 건지기 위해 'small' 모델로 강제 고정합니다.
    model = whisper.load_model("small") 
    
    print(f"-> '{audio_file_path}' 파일을 받아쓰기 중입니다. 잠시만 기다려 주세요...")
    result = model.transcribe(audio_file_path, language="ko")
    
    raw_segments = []
    for segment in result['segments']:
        text = segment['text'].strip()
        if text:
            raw_segments.append(text)
    
    full_transcript_input = "\n".join(raw_segments)
    print("✓ 음성 텍스트 변환 성공!")

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" 2단계: 로컬 Ollama 모델로 화자 분리 및 상세 요약")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("-> 로컬 LLM이 문맥을 파악하여 리포트를 생성하는 중입니다...")

    ollama_url = "http://localhost:11434/api/generate"
    
    # ⚠️ 단 하나의 영어 단어도 허용하지 않고, 신분 추측을 절대 금지하는 초강력 프롬프트
    system_prompt = (
        "당신은 대한민국 법원 서기 수준으로 통화 녹음본을 가감 없이 정확하게 기록하는 전문 비서입니다.\n"
        "제공된 텍스트는 한국인 2명이 나눈 대화 원문입니다. 다음 지침을 '단 하나도 빠짐없이' 철저히 준수하여 텍스트 파일을 작성하세요.\n\n"
        
        "[언어 및 표기 절대 규칙]\n"
        "1. 당신은 오직 '한국어(Korean)'로만 답변해야 합니다. 영어 단어, 영어 문장, 영어 Bullet point(Grief and Loss 등)를 단 한 줄도 출력하지 마십시오. 모든 제목과 내용, 서술은 100% 한글이어야 합니다.\n"
        "2. 화자의 신분 관계(형, 오빠, 아들, 딸, 남매, siblings 등)를 절대로 당신 마음대로 추측하거나 단정 지어 리포트에 적지 마십시오. 대화 속에 직접적으로 부르는 호칭이 나오더라도, 리포트 서술 시에는 철저히 [화자 A], [화자 B]로만 칭해야 합니다.\n\n"
        
        "[출력 문서 상세 양식]\n\n"
        "## 1. 대화 요약 리포트\n"
        "* **핵심 요약**: 이 통화의 핵심적인 상황, 대화의 목적, 주요 맥락을 놓치는 부분 없이 꼼꼼하게 서술해 주세요. 대충 요약하지 말고 전체 스토리가 이해되도록 상세히 작성해야 합니다.\n"
        "* **주요 흐름 정리**: 대화 속에서 언급된 주요 대화의 흐름과 사건의 순서를 일목요연하게 정리해 주세요.\n"
        "* **주요 과제 및 해야 할 일**: 대화 중에서 도출된 처리해야 할 행정 업무, 수집해야 할 정보, 구체적인 행동 지침(To-do) 목록을 명확히 추출해 주세요.\n\n"
        
        "## 2. 전체 대화 본문 (화자 분리)\n"
        "대화 문맥을 파악하여 전체 대화 본문을 복원하되, 본문 내에 시간 정보는 빼고 오직 화자 표시와 대화 내용만으로 흐름이 이어지게 옭아매듯 쫘악 작성해 주세요.\n"
        "절대로 본문 내용을 요약하거나 생략하지 말고 모든 대화 내용을 빠짐없이 다 적어야 합니다.\n"
        "포맷 예시:\n"
        "[화자 A]: 대화 내용\n"
        "[화자 B]: 대화 내용"
    )

    payload = {
        "model": "gemma2",
        "prompt": f"{system_prompt}\n\n[분석할 음성 텍스트]:\n{full_transcript_input}",
        "stream": False
    }

    try:
        response = requests.post(ollama_url, json=payload, timeout=300)
        ai_analysis_result = response.json().get("response", "요약 생성 실패")
    except Exception as e:
        print(f"❌ 로컬 LLM(Ollama) 연동 실패: {e}")
        ai_analysis_result = f"--- 로컬 LLM 요약 실패 (원본 텍스트만 저장) ---\n\n{full_transcript_input}"

    print("✓ AI 문맥 분석 및 요약 완료!")

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" 3단계: 최종 결과 텍스트 파일 저장")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(ai_analysis_result)
        
    print(f"🎉 모든 작업이 성공적으로 완료되었습니다!")
    print(f"📄 저장된 파일 위치: {os.path.abspath(output_file_path)}")

# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    AUDIO_FILE = "06.16 신이서 통화.m4a" 
    OUTPUT_DIRECTORY = "./SavedResults" 
    
    if os.path.exists(AUDIO_FILE):
        transcribe_and_summarize(AUDIO_FILE, OUTPUT_DIRECTORY)
    else:
        print(f"❌ '{AUDIO_FILE}' 음성 파일을 찾을 수 없습니다. 경로와 파일명을 다시 확인해 주세요.")