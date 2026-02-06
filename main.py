import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def update_readme(news_text, timestamp):
    header = "# ⚽ 실시간 EPL 뉴스 (15분 주기 업데이트)\n\n"
    footer = f"\n\n---\n*최근 업데이트: {timestamp} (KST) / (하루 100회 제한 준수 중)*"
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(header + news_text + footer)

def get_epl_news():
    kst_now = datetime.utcnow() + timedelta(hours=9)
    timestamp = kst_now.strftime('%Y-%m-%d %H:%M:%S')

    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("에러: NEWS_API_KEY 없음")
        return

    # API 호출
    url = f"https://newsapi.org/v2/everything?q=Premier League&sortBy=publishedAt&pageSize=10&language=en&apiKey={api_key}"

    try:
        response = requests.get(url)
        if response.status_code == 429:
            print("한도 초과")
            return
            
        response.raise_for_status()
        data = response.json()
        articles = data.get('articles', [])
        
        # 여기서 확실하게 10개만 자름
        top_10_articles = articles[:11]

        if not top_10_articles:
            print("기사 없음")
            return

        news_content = ""
        for i, article in enumerate(top_10_articles, 1):
            title = article.get('title')
            source = article.get('source', {}).get('name')
            link = article.get('url')
            news_content += f"{i}. [{title}]({link}) - **{source}**\n"
            
        update_readme(news_content, timestamp)
        print(f"성공: {timestamp} 기준 10개 출력 완료")
            
    except Exception as e:
        print(f"오류: {e}")

if __name__ == "__main__":
    get_epl_news()