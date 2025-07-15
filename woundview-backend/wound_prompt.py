import openai
import os

from dotenv import load_dotenv
load_dotenv()

def generate_advice_openai(
    predict_result,
    wound_size,
    redness,
    swelling,
    heat,
    pain,
    function_loss,
    history_data,
    current_season,
    current_climate,
    date,
    body_part,
    cause
):
    # 환경변수에서 OpenAI 키 로딩 (직접 문자열로 넣어도 됨)
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"""너는 상처 분석 전문가로서, 딥러닝 모델이 예측한 상처 정보와 사용자가 체크박스로 입력한 염증 증상(피부가 빨개졌는지, 부어 있는지, 열이 나는지, 아픈지, 움직이기 어려운지)을 바탕으로 다음 항목을 마크다운 형식으로 순차적으로 출력해줘.
    [입력 항목]
    - 상처의 발생일자: {date}
    - 상처의 발생부위: {body_part}
    - 상처의 발생원인: {cause}
    
    - 상처 종류: {predict_result}
    - 상처 크기: {wound_size} (단위: cm, [가로, 세로])
    - 사용자 입력 염증 증상:
    - 피부가 빨개졌나요? → {redness}
    - 부어 있나요? → {swelling}
    - 만지면 뜨겁게 느껴지나요? → {heat}
    - 아프거나 따끔거리나요? → {pain}
    - 움직이기 어렵거나 사용이 불편한가요? → {function_loss}
    - (선택) 과거 상처 기록: {history_data}
    - (선택) 현재 계절: {current_season}
    - (선택) 현재 기후 상태: {current_climate}

    [출력 항목 형식 (JSON으로 작성)]

    **위험등급**:  
    - 저위험 / 중간위험 / 고위험 중 하나로 판단

    **증상 해석**:  
    - 상처 종류와 크기, 입력된 증상을 종합해서 상처 상태를 설명해줘.  
    - 염증 반응과 통증, 기능장애가 실제 상태에 어떤 영향을 주는지 자연스럽게 해석해줘.  
    - 어려운 용어는 괄호 병기로 쉽게 풀어줘 (예: 부종(붓기), 발적(붉어짐)).

    **회복 예상 기간**:  
    - 몇 일~몇 주 내 회복될 수 있는지 예측하고, 근거를 간단히 설명해줘.

    **관리 가이드**:  
    - 실생활에서 따라할 수 있는 단계별 상처 관리 방법을 3~5가지로 제시해줘.  
    - 세척, 소독, 드레싱, 연고 사용 등 실용적인 내용을 포함하고, 연고는 성분 위주로 추천해줘 (예: 시카, 판테놀 등).

    **주의사항**:  
    - 감염 예방, 상처 자극 방지, 드레싱 교체 등에 대해 핵심 주의사항 2~4가지를 알려줘.

    **행동 지침**:  
    - 위험도에 따라 병·의원 방문 필요성 여부를 판단해줘.  
    - 고위험 → 병원 또는 응급실 즉시 내원 권장  
    - 중간위험 → 병·의원 진료 권장  
    - 저위험 → 자가 치료 가능, 변화 시 병원 상담

    **경과 분석 결과** *(옵션)*:  
    - history_data가 있을 경우, 이전 기록과 비교하여 상태가 호전형 / 정체형 / 악화형인지 판단하고, 크기 변화율(%)도 포함해줘.

    **계절 및 기후 주의사항** *(옵션)*:  
    - 여름/겨울 및 고온다습/건조 등의 기후가 상처 회복에 어떤 영향을 줄 수 있는지 간단히 설명해줘.

    꼭 JSON 형식으로 반환해줘.
    예시 :
    {
    "risk_level": "고위험",
    "symptom_analysis": "상처는 베인 상처로, 가로 4cm, 세로 2cm로 비교적 크며, 피부가 붉고 부어 있고, 만지면 뜨거우며 통증이 심하게 나타납니다. 이는 염증 반응이 활발하게 진행 중임을 의미합니다. 부종(붓기), 발적(붉어짐), 열감 등은 감염의 위험 신호일 수 있습니다.",
    "recovery_period": "약 2~3주 내 회복될 수 있으나, 감염이 동반될 경우 더 오래 걸릴 수 있습니다. 상처의 크기와 염증 증상이 심한 점을 고려했습니다.",
    "care_guide": "1. 흐르는 물로 상처를 깨끗이 세척하세요.\n2. 소독제를 사용해 감염을 예방하세요.\n3. 멸균 거즈로 상처를 덮고, 하루 1~2회 드레싱을 교체하세요.\n4. 시카, 판테놀 등 진정 성분의 연고를 사용하세요.\n5. 상처 부위를 자극하지 않도록 주의하세요.",
    "caution": "상처 부위가 더 붓거나, 고름이 생기거나, 열이 지속되면 즉시 병원을 방문하세요. 드레싱은 항상 깨끗한 상태로 유지하고, 손을 깨끗이 씻은 후 처치하세요.",
    "action_guide": "감염 및 합병증 우려가 높으므로 즉시 병원이나 응급실 방문을 권장합니다.",
    "progress_analysis": "이전 기록과 비교 시 상처 크기가 20% 증가하여 악화형으로 판단됩니다.",
    "seasonal_caution": "여름철 고온다습한 환경에서는 상처가 쉽게 덧날 수 있으니, 땀과 습기를 잘 관리하고, 통풍이 잘 되도록 주의하세요."
    }

    """

    import json
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "너는 의료 전문가이자 상처 분석 도우미야."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        result_text = response.choices[0].message['content']
    except Exception as api_error:
        # OpenAI API 호출 실패시
        print("OpenAI API Error:", api_error)
        return {"error": "AI 서버와 통신에 실패했습니다.", "detail": str(api_error)}
    try:
        result_json = json.loads(result_text)
    except json.JSONDecodeError:
        import re
        match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if match:
            result_json = json.loads(match.group())
        else:
            return {"error": "LLM 응답에서 JSON을 추출할 수 없습니다.", "raw": result_text}

    return result_json