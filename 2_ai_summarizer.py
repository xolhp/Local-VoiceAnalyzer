import os
import requests

def run_ai_summary(text_file_path, output_dir_path):
    if not os.path.exists(text_file_path):
        print(f" 분석할 텍스트 파일이 없습니다: '{text_file_path}'\n-> 1번 코드를 먼저 실행해 주세요.")
        return

    base_name = os.path.splitext(os.path.basename(text_file_path))[0].replace("_원본본문", "")
    output_file_path = os.path.join(output_dir_path, f"{base_name}_최종보고서.txt")

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" 2단계: 로컬 LLM(Gemma2)을 활용한 항목별 상세 보고서 생성")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    with open(text_file_path, "r", encoding="utf-8") as f:
        full_transcript = f.read()

    print("-> 로컬 AI가 대화 속 구체적인 정보를 정밀 분류 중입니다...")
    ollama_url = "http://localhost:11434/api/generate"
    
    # ⚠️ 추상적인 감상문을 100% 차단하고 세부 지표를 강제 도출하게 하는 프롬프트
    system_prompt = (
        "당신은 상속 및 기업 행정 업무를 정리하는 법무 비서이자 분석가입니다.\n"
        "제공된 대화 원본을 바탕으로, 감정적인 미사여구를 모두 배제하고 오직 '구체적인 사실과 업무' 위주로 다음 상세 항목들을 작성하세요.\n"
        "내용을 뭉뚱그리지 말고, 대화에서 언급된 구체적인 단어(서류명, 자산 종류, 조치 사항 등)를 최대한 살려 꼼꼼하게 서술해야 합니다.\n\n"
        
        "[작성 규칙]\n"
        "1. 100% 한국어로만 작성하세요. (영어 제목, 영어 소제목 절대 금지)\n"
        "2. 화자는 오직 [화자 A], [화자 B]로만 명확히 구분하여 서술하세요.\n\n"
        
        "[반드시 포함해야 할 상세 항목 양식]\n"
        "## 1. 종합 개요\n"
        "- 통화가 이루어진 배경과 두 화자가 현재 당면한 전체적인 상황 요약 (5줄 이상 상세히)\n\n"
        
        "## 2. 자산 및 자가용(차량) 관련 논의 사항\n"
        "- 차량의 소유권 변동, 처분 방식(매각, 폐차, 유지 등), 명의 변경 및 이와 관련해 언급된 구체적인 조치 내용들을 상세히 기록하세요.\n\n"
        
        "## 3. 보험금 및 행정/법적 서류 처리 내역\n"
        "- 대화 중 언급된 청구 가능한 보험금 종류, 제출해야 하거나 확인해야 하는 서류 목록, 방문해야 하는 기관 등이 있다면 빠짐없이 분류하여 적어주세요.\n\n"
        
        "## 4. 사업 및 업무 인수인계/마무리 사항\n"
        "- 사업이나 정리해야 하는 비즈니스적 업무, 조율 중인 정산 내용이나 마감 지침에 대해 오간 대화를 구체적으로 요약하세요.\n\n"
        
        "## 5. 향후 실행 과제 및 행동 지침 (Action Plan)\n"
        "- [화자 A]가 해야 할 일 (To-do 목록 2~3개 이상 구체적으로)\n"
        "- [화자 B]가 해야 할 일 (To-do 목록 2~3개 이상 구체적으로)\n"
        "- 추후 서로 공유하거나 재확인하기로 약속한 사항"
    )

    payload = {
        "model": "gemma2",
        "prompt": f"{system_prompt}\n\n[분석할 대화 원본]:\n{full_transcript}",
        "stream": False
    }

    try:
        response = requests.post(ollama_url, json=payload, timeout=300)
        ai_summary_result = response.json().get("response", "요약 생성 실패")
    except Exception as e:
        print(f" 로컬 LLM(Ollama) 연동 실패: {e}")
        return

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(ai_summary_result)
        
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✓ 2단계 완료: 항목별 상세 리포트 생성 성공!")
    print(f" 최종 보고서 파일: {os.path.abspath(output_file_path)}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    TARGET_TEXT_FILE = "./SavedResults/00.00 --- 통화_원본본문.txt"
    OUTPUT_DIRECTORY = "./SavedResults"
    
    run_ai_summary(TARGET_TEXT_FILE, OUTPUT_DIRECTORY)