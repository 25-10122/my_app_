import streamlit as st
from openai import OpenAI

# 1. 웹 페이지 기본 설정 및 타이틀
st.set_page_config(page_title="AI 톤앤매너 답장 작성기", page_icon="📧", layout="centered")

st.title("📧 AI 비즈니스 이메일 & 답장 작성기")
st.write("핵심 내용만 적어주시면, 상황과 말투에 맞는 완벽한 메일을 작성해 드립니다.")
st.markdown("---")

# 2. 사이드바 - API 키 입력 및 옵션 설정
with st.sidebar:
    st.header("⚙️ 설정")
    # API 키를 화면에서 입력받거나, Streamlit Secrets를 사용할 수 있습니다.
    openai_api_key = st.text_input("OpenAI API Key 입력", type="password")
    st.markdown("[OpenAI API 키 발급받기](https://platform.openai.com/api-keys)")
    
    st.markdown("---")
    st.subheader("🤖 메일 스타일 설정")
    # 말투(Tone) 선택
    email_tone = st.selectbox(
        "원하는 말투를 선택하세요:",
        ["정중하고 격식 있는 (비즈니스)", "친근하고 부드러운 (동료/친구)", "단호하고 명확한 (협상/거절)", "사과와 양해를 구하는"]
    )
    
    # 언어 선택
    email_lang = st.radio("작성 언어:", ["한국어", "English"])

# 3. 메인 화면 - 사용자 입력창
st.subheader("📝 내용 입력하기")

# 상황 설명 (예: 회의 연기, 협력 제안 등)
context = st.text_area(
    "어떤 상황인가요? 핵심 내용만 적어주세요.",
    placeholder="예시: 내일 오후 2시 미팅을 갑작스러운 내부 사정으로 인해 다음 주 화요일 오후 3시로 변경하고 싶어. 늦게 연락해서 죄송하다는 말도 포함해줘.",
    height=150
)

# 4. AI 메일 생성 로직
if st.button("✨ AI 메일 초안 생성하기"):
    # 유효성 검사 (API 키와 입력 내용이 있는지 확인)
    if not openai_api_key:
        st.warning("오른쪽 사이드바에 OpenAI API Key를 입력해 주세요!")
    elif not context.strip():
        st.warning("메일에 들어갈 핵심 내용을 입력해 주세요!")
    else:
        # 로딩 애니메이션 시작
        with st.spinner("AI가 톤앤매너를 맞춰 메일을 작성하고 있습니다..."):
            try:
                # OpenAI 클라이언트 초기화
                client = OpenAI(api_key=openai_api_key)
                
                # AI에게 줄 역할과 지시사항(Prompt) 설정
                system_prompt = (
                    "너는 비즈니스 커뮤니케이션 전문가야. 사용자가 제공한 핵심 내용을 바탕으로 "
                    f"적절한 이메일을 작성해야 해. 말투는 반드시 '{email_tone}' 스타일에 맞춰야 하고, "
                    f"작성 언어는 '{email_lang}'이어야 해. "
                    "받는 사람이 읽었을 때 자연스럽고 프로페셔널하도록 이메일 제목([제목])과 본문을 나누어서 작성해줘."
                )
                
                # API 호출
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # 가성비가 가장 좋은 최신 모델
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": context}
                    ],
                    temperature=0.7 # 적당한 창의성
                )
                
                # 결과 추출 및 화면 표시
                generated_email = response.choices[0].message.content
                
                st.markdown("---")
                st.subheader("🎉 완성된 이메일 초안")
                
                # 코드 블록 형태로 출력하여 우측 상단에 자동으로 '복사하기' 버튼이 생기도록 함
                st.code(generated_email, language="markdown")
                st.success("작성이 완료되었습니다! 복사해서 사용해 보세요.")
                
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")
