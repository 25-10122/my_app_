import streamlit as st
import google.generativeai as genai  # 👈 구글 AI 라이브러리로 변경되었습니다.

# 웹 페이지 기본 설정
st.set_page_config(page_title="AI 톤앤매너 답장 작성기", page_icon="📧", layout="centered")

st.title("📧 [무료버전] AI 비즈니스 이메일 & 답장 작성기")
st.write("핵심 내용만 적어주시면, 상황과 말투에 맞는 완벽한 메일을 작성해 드립니다. (구글 Gemini 탑재)")
st.markdown("---")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정")
    # 이제 구글 API 키를 입력받습니다.
    google_api_key = st.text_input("Google Gemini API Key 입력", type="password")
    st.markdown("[구글 API 키 무료로 발급받기](https://aistudio.google.com/)")
    
    st.markdown("---")
    st.subheader("🤖 메일 스타일 설정")
    
    email_tone = st.selectbox(
        "원하는 말투를 선택하세요:",
        ["정중하고 격식 있는 (비즈니스)", "친근하고 부드러운 (동료/친구)", "단호하고 명확한 (협상/거절)", "사과와 양해를 구하는"]
    )
    
    email_lang = st.radio("작성 언어:", ["한국어", "English"])

# 메인 화면 입력창
st.subheader("📝 내용 입력하기")

context = st.text_area(
    "어떤 상황인가요? 핵심 내용만 적어주세요.",
    placeholder="예시: 내일 오후 2시 미팅을 갑작스러운 내부 사정으로 인해 다음 주 화요일 오후 3시로 변경하고 싶어. 늦게 연락해서 죄송하다는 말도 포함해줘.",
    height=150
)

# 버튼 클릭 시 구글 AI 작동
if st.button("✨ AI 메일 초안 생성하기"):
    if not google_api_key:
        st.warning("오른쪽 사이드바에 Google Gemini API Key를 입력해 주세요!")
    elif not context.strip():
        st.warning("메일에 들어갈 핵심 내용을 입력해 주세요!")
    else:
        with st.spinner("구글 AI가 톤앤매너를 맞춰 메일을 작성하고 있습니다..."):
            try:
                # 구글 API 키 인증
                genai.configure(api_key=google_api_key)
                
                # 가장 똑똑하고 가벼운 최신 모델(Gemini 1.5 Flash) 사용
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # 프롬프트(명령어) 조합
                prompt = (
                    f"너는 비즈니스 커뮤니케이션 전문가야. 다음 [핵심 내용]을 바탕으로 이메일을 작성해줘.\n"
                    f"1. 말투 스타일: {email_tone}\n"
                    f"2. 작성 언어: {email_lang}\n"
                    f"3. 요구사항: 받는 사람이 읽었을 때 자연스럽고 프로페셔널하도록 이메일 제목([제목])과 본문을 명확히 나누어서 작성해줘.\n\n"
                    f"[핵심 내용]: {context}"
                )
                
                # AI 답변 생성
                response = model.generate_content(prompt)
                generated_email = response.text
                
                # 결과 출력
                st.markdown("---")
                st.subheader("🎉 완성된 이메일 초안")
                st.code(generated_email, language="markdown")
                st.success("작성이 완료되었습니다! 무료로 마음껏 사용해 보세요.")
                
            except Exception as e:
                st.error(f"에러가 발생했습니다. API 키가 올바른지 확인해 주세요. (상세 에러: {e})")
