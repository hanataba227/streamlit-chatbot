# 필요한 라이브러리 가져오기
import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="Chat", page_icon="💬")

# 환경변수에서 API 키 가져오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# API 키가 없으면 에러 표시하고 중단
if not api_key:
    st.error("OPENAI_API_KEY가 .env 파일에 없습니다.")
    st.stop()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)

def get_llm_response(messages, placeholder):
    """AI로부터 스트리밍 응답을 받아오는 함수"""
    response = ""  # 전체 응답을 저장할 변수
    
    # OpenAI API 호출 (스트리밍 모드)
    stream = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=messages, 
        stream=True
    )
    
    # 스트림에서 각 청크를 받아서 실시간으로 화면에 표시
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:  # 내용이 있으면
            response += content
            placeholder.markdown(response)  # 화면에 실시간 업데이트
    
    return response

# 세션 상태에 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "당신은 간결하고 도움이 되는 AI 어시스턴트입니다."}
    ]

# 사용자 입력 받기
user_input = st.chat_input("메시지를 입력하세요")

if user_input:  # 사용자가 메시지를 입력했으면
    # 사용자 메시지를 대화 기록에 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 사용자 메시지 화면에 표시
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성 및 표시
    with st.chat_message("assistant"):
        response_placeholder = st.empty()  # 실시간 업데이트를 위한 빈 공간
        ai_response = get_llm_response(st.session_state.messages, response_placeholder)
