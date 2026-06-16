import os
import whisper

def run_stt(audio_file_path, output_dir_path):
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
    # 결과 파일명: SavedResults/00.00 000 통화_원본본문.txt
    output_file_path = os.path.join(output_dir_path, f"{base_name}_원본본문.txt")

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" 1단계: 로컬 Whisper 모델로 음성 받아쓰기 시작")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    print("-> Whisper 'small' 모델을 로드하고 있습니다...")
    model = whisper.load_model("small") 
    
    print(f"-> '{audio_file_path}' 파일을 받아적는 중입니다...")
    result = model.transcribe(audio_file_path, language="ko")
    
    # 시간 표기 없이 줄바꿈만 주어 옭아매듯 쫘악 저장
    raw_segments = []
    for segment in result['segments']:
        text = segment['text'].strip()
        if text:
            raw_segments.append(text)
    
    full_transcript = "\n".join(raw_segments)
    
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(full_transcript)
        
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✓ 1단계 완료: 음성 텍스트 변환 및 원본 본문 저장 성공!")
    print(f" 생성된 본문 파일: {os.path.abspath(output_file_path)}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    AUDIO_FILE = "00.00 --- 통화.m4a" 
    OUTPUT_DIRECTORY = "./SavedResults" 
    
    if os.path.exists(AUDIO_FILE):
        run_stt(AUDIO_FILE, OUTPUT_DIRECTORY)
    else:
        print(f" '{AUDIO_FILE}' 음성 파일을 찾을 수 없습니다.")