import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv
import asyncio

# 환경 변수 로드
load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# 악성 요소를 찾고 분류하는 비동기 함수
async def find_malicious_elements(comment):
    try:
        # OpenAI API 호출
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        You are a malicious comment detector.
                        When you find malicious elements in a sentence entered by the user,
                        Select one or more from the
                        classification = ["기타 혐오", "남성", "단순 악플", "성소수자", "여성/가족", "연령", "인종/국적", "종교", "지역"]
                        and return it. If there are multiple, separate them with commas.
                        If there are no malicious elements in the sentence, return nan.

                        example comment = "똥양좆들 와꾸 키 덩치 재기해서 편하게 사노 배때지를 쑤셔블라"
                        answer = "단순 악플, 인종/국적"
                        """
                    },
                    {
                        "role": "user",
                        "content": comment
                    }
                ],
                temperature=0,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
        )
        
        # 응답 처리
        classification = response.choices[0].message.content
        return classification if classification else 'nan'
    
    except Exception as e:
        print(f'Error: {e}')
        return 'unknown'

# 비동기 함수 실행을 위한 함수
async def main():
    # CSV 파일에서 데이터 읽기
    df = pd.read_csv('test_sentence.csv')
    
    # 각 comment에 대해 악성 요소를 분류하고 결과를 새로운 DataFrame에 저장
    results = []
    tasks = [find_malicious_elements(comment) for comment in df['comment']]
    classifications = await asyncio.gather(*tasks)
    
    for comment, classification in zip(df['comment'], classifications):
        results.append({'comment': comment, 'classification': classification})
    
    # 결과를 DataFrame으로 변환
    results_df = pd.DataFrame(results)
    
    # 결과를 CSV 파일로 저장
    results_df.to_csv('comments_classification_results.csv', encoding='utf-8-sig', index=False)

# 비동기 함수 실행
if __name__ == '__main__':
    asyncio.run(main())
