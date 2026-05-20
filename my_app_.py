import streamlit as st  # 👈 필수 라이브러리를 가장 먼저 가져옵니다.
from openai import OpenAI

# [중요] st.set_page_config는 import 문 바로 다음에, 다른 모든 st 함수보다 먼저 와야 합니다.
st.set_page_config(page_title="AI 톤앤매너 답장 작성기", page_icon="📧", layout="centered")

# 1. 메인 화면 타이틀 및 설명
st.title("📧 AI 비즈니스 이메일 & 답장 작성기")
st.write("핵심 내용만 적어주시면, 상황과 말투에 맞는 완벽한 메일을 작성해 드립니다.")
st.markdown("---")

# 2. 사이드바 설정 (옵션 및 API 키 입력)
with st.sidebar:
    st.header("⚙️ 설정")
    # API 키를 화면에서 안전하게 입력받는 창 (비밀번호 마스킹 처리)
    openai_api_key = st.text_input("OpenAI API Key 입력", type="password")
    st.markdown("[OpenAI API 키 발급받기](https://platform.openai.com/api-keys)")
    
    st.markdown("---")
    st.subheader("🤖 메일 스타일 설정")
    
    # 사용자가 선택할 말투(Tone) 옵션
    email_tone = st.selectbox(
        "원하는 말투를 선택하세요:",
        ["정중하고 격식 있는 (비즈니스)", "친근하고 부드러운 (동료/친구)", "단호하고 명확한 (협상/거절)", "사과와 양해를 구하는"]
    )
    
    # 결과물 언어 선택
    email_lang = st.radio("작성 언어:", ["한국어", "English"])

# 3. 메인 화면 - 텍스트 입력창
st.subheader("📝 내용 입력하기")

context = st.text_area(
    "어떤 상황인가요? 핵심 내용만 적어주세요.",
    placeholder="예시: 내일 오후 2시 미팅을 갑작스러운 내부 사정으로 인해 다음 주 화요일 오후 3시로 변경하고 싶어. 늦게 연락해서 죄송하다는 말도 포함해줘.",
    height=150
)

# 4. 버튼 클릭 시 AI 메일 생성 로직 작동
if st.button("✨ AI 메일 초안 생성하기"):
    # 필수 입력 항목 검증 (Validation)
    if not openai_api_key:
        st.warning("오른쪽 사이드바에 OpenAI API Key를 입력해 주세요!")
    elif not context.strip():
        st.warning("메일에 들어갈 핵심 내용을 입력해 주세요!")
    else:
        # AI 응답 대기 중 로딩 애니메이션 띄우기
        with st.spinner("AI가 톤앤매너를 맞춰 메일을 작성하고 있습니다..."):
            try:
                # OpenAI 클라이언트 초기화
                client = OpenAI(api_key=openai_api_key)
                
                # 프롬프트 구성 (AI에게 명확한 가이드라인 제공)
                system_prompt = (
                    "너는 비즈니스 커뮤니케이션 전문가야. 사용자가 제공한 핵심 내용을 바탕으로 "
                    f"적절한 이메일을 작성해야 해. 말투는 반드시 '{email_tone}' 스타일에 맞춰야 하고, "
                    f"작성 언어는 '{email_lang}'이어야 해. "
                    "받는 사람이 읽었을 때 자연스럽고 프로페셔널하도록 이메일 제목([제목])과 본문을 나누어서 작성해줘."
                )
                
                # API 호출 (비용 효율적이고 빠른 gpt-4o-mini 모델 활용)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": context}
                    ],
                    temperature=0.7
                )
                
                # 생성된 텍스트 결과 가져오기
                generated_email = response.choices[0].message.content
                
                # 결과 화면에 출력
                st.markdown("---")
                st.subheader("🎉 완성된 이메일 초안")
                
                # 사용자가 편하게 복사할 수 있도록 st.code 사용 (우측 상단 복사 버튼 자동 생성)
                st.code(generated_email, language="markdown")
                st.success("작성이 완료되었습니다! 복사해서 사용해 보세요.")
                
            except Exception as e:
                # API 연동 과정에서 에러 발생 시 사용자에게 친절하게 메시지 표시
                st.error(f"에러가 발생했습니다. API 키가 올바른지 확인해 주세요. (상세 에러: {e})")
