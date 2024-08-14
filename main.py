
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

# client 객체 생성하기
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY")) # 발급받은 API 키 값을 넣어주세요

#응답 받기
response = client.chat.completions.create(
    model = "gpt-4-turbo-preview",
    messages =[
        {
            "role":"system",
            "content":"""
            너는 악성 댓글 탐지기이자 순화어 추천기야.
            사용자가 입력한 문장 안에 악성 요소(저주나 협박, 비방, 성적 욕설)와 주의 요소를 해당 부분만 추출해.
            그리고 대체 가능한 순화어를 추천해줘. 대체 가능한 표현이 없는 경우에는 ""을 반환해줘.
            json format으로 추출해줘.
            {
            "악성 요소": [{"표현1":["순화어1", "순화어2", ...]}, {"표현2": ["순화어1", ...]}],
            "주의 요소": [{"표현1":["순화어1", "순화어2", ...]}, {"표현2": ["순화어1", ...]}]
            }
            """
        },
        {
            "role":"user",
            "content":"야 이 멍청한 새끼야"
        }
    ],
    temperature=0,
    max_tokens = 1000,
    top_p = 1,
    frequency_penalty = 0,
    presence_penalty = 0,
    
    # response_format 지정하기
    response_format = {"type":"json_object"}
)

print(response.choices[0].message.content)