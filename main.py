import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def update_readme(news_text):
    header = "# ⚽ 실시간 EPL 뉴스 (15분 주기 업데이트)\n\n"
    # 한국 시간(KST) 계산
    kst_now = datetime.utcnow() + timedelta(hours=9)
    timestamp = kst_now.strftime('%Y-%m-%d %H:%M:%S')
    
    footer = f"\n\n---\n*최지막 업데이트: {timestamp} (KST) / (하루 100회 제한 준수 중)*"
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(header + news_text + footer)

def get_epl_news():
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("에러: NEWS_API_KEY가 설정되지 않았습니다.")
        return

    # NewsAPI 호출 (최신순 10개)
    url = f"https://newsapi.org/v2/everything?q=Premier League&sortBy=publishedAt&pageSize=10&language=en&apiKey={api_key}"

    try:
        response = requests.get(url)
        
        if response.status_code == 429:
            print("에러: NewsAPI 호출 한도 초과입니다.")
            return
            
        response.raise_for_status()
        articles = response.json().get('articles', [])
        
        if not articles:
            print("알림: 새로운 기사가 없습니다.")
            return

        news_content = ""
        for i, article in enumerate(articles, 1):
            title = article.get('title')
            source = article.get('source', {}).get('name')
            link = article.get('url')
            news_content += f"{i}. [{title}]({link}) - **{source}**\n"
            
        update_readme(news_content)
        print(f"성공: {timestamp} 기준 README 업데이트 완료")
            
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    get_epl_news()