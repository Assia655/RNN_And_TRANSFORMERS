import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from datetime import datetime
from urllib.parse import urljoin

def calculate_relevance_score(text):
    """
    Calculate relevance score (0-10) based on content quality and sports keywords
    """
    if not text or len(text) < 20:
        return 0
    
    text_lower = text.lower()
    
    # Arabic sports keywords
    keywords = [
        'كرة القدم', 'كرة', 'فريق', 'لاعب', 'مباراة', 'هدف', 'رياضة', 'دوري',
        'بطولة', 'كأس', 'نهائي', 'فوز', 'هزيمة', 'تعادل', 'ملعب', 'مدرب',
        'لاعبين', 'منتخب', 'دولي', 'عالمي', 'محلي', 'بطل', 'بطالة', 'رياضي'
    ]
    
    # Count keyword occurrences
    keyword_count = sum(text_lower.count(keyword) for keyword in keywords)
    text_length = len(text.split())
    
    # Calculate score
    if text_length == 0:
        return 0
    
    keyword_density = (keyword_count / text_length) * 100
    score = min(10, max(1, keyword_density * 3))
    
    # Bonus for minimum length
    if text_length >= 50:
        score = min(10, score + 1)
    if text_length >= 100:
        score = min(10, score + 0.5)
    
    return round(score, 1)

def scrape_wikipedia_ar(topic_url):
    """
    Scrape paragraphs from Arabic Wikipedia
    """
    texts = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(topic_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"Error accessing {topic_url}: Status {response.status_code}")
            return texts
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all paragraphs
        paragraphs = soup.find_all('p')
        
        for para in paragraphs:
            text = para.get_text(strip=True)
            
            # Clean text
            text = re.sub(r'\[\d+\]', '', text)  # Remove reference markers [1], [2], etc
            text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
            
            # Keep substantial paragraphs
            if len(text) > 80 and len(text) < 1000:
                texts.append(text)
        
        print(f"✓ Scraped {len(texts)} paragraphs from {topic_url}")
        
    except Exception as e:
        print(f"Error scraping {topic_url}: {e}")
    
    return texts

def main():
    """Main function to scrape Wikipedia and create dataset"""
    
    print("جاري جمع البيانات من ويكيبيديا العربية...")
    print("=" * 80)
    
    # Arabic Wikipedia sports pages
    wikipedia_urls = [
        # Football/Soccer
        'https://ar.wikipedia.org/wiki/كرة_القدم',
        'https://ar.wikipedia.org/wiki/كأس_العالم_لكرة_القدم',
        'https://ar.wikipedia.org/wiki/دوري_أبطال_أوروبا',
        'https://ar.wikipedia.org/wiki/رونالدو',
        'https://ar.wikipedia.org/wiki/ميسي',
        
        # Basketball
        'https://ar.wikipedia.org/wiki/كرة_السلة',
        'https://ar.wikipedia.org/wiki/NBA',
        
        # Volleyball
        'https://ar.wikipedia.org/wiki/كرة_الطائرة',
        
        # Tennis
        'https://ar.wikipedia.org/wiki/كرة_المضرب',
        
        # Swimming
        'https://ar.wikipedia.org/wiki/السباحة',
        
        # Track and Field
        'https://ar.wikipedia.org/wiki/ألعاب_القوى',
        
        # Olympic Games
        'https://ar.wikipedia.org/wiki/الألعاب_الأولمبية',
        
        # More Football topics
        'https://ar.wikipedia.org/wiki/الدوري_الإسباني',
        'https://ar.wikipedia.org/wiki/الدوري_الإيطالي',
        'https://ar.wikipedia.org/wiki/الدوري_الإنجليزي_الممتاز',
    ]
    
    all_texts = []
    
    # Scrape each Wikipedia page
    for url in wikipedia_urls:
        print(f"جاري الكشط من: {url}")
        texts = scrape_wikipedia_ar(url)
        all_texts.extend(texts)
        time.sleep(1)  # Respectful delay between requests
    
    print("\n" + "=" * 80)
    print(f"تم جمع {len(all_texts)} نص من ويكيبيديا")
    
    # Create dataset with relevance scores
    dataset = []
    for text in all_texts:
        score = calculate_relevance_score(text)
        dataset.append({
            'Text': text,
            'Score': score
        })
    
    # Create DataFrame
    df = pd.DataFrame(dataset)
    
    # Sort by score (descending)
    df = df.sort_values('Score', ascending=False).reset_index(drop=True)
    
    # Display preview
    print("\n" + "=" * 80)
    print("عينة من البيانات المجمعة | Dataset Preview")
    print("=" * 80)
    
    for idx in range(min(10, len(df))):
        print(f"\nText {idx + 1} | Score: {df.iloc[idx]['Score']}")
        print(f"{df.iloc[idx]['Text'][:250]}...")
        print("-" * 80)
    
    # Save to CSV
    csv_filename = f"wikipedia_sports_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    
    print(f"\n✓ تم حفظ البيانات | Dataset saved to: {csv_filename}")
    print(f"\nإحصائيات البيانات | Dataset Statistics:")
    print(f"إجمالي النصوص | Total texts: {len(df)}")
    print(f"متوسط النقاط | Average score: {df['Score'].mean():.2f}")
    print(f"أقل نقاط | Min score: {df['Score'].min()}")
    print(f"أعلى نقاط | Max score: {df['Score'].max()}")
    
    # Display score distribution
    print(f"\nتوزيع النقاط | Score Distribution:")
    score_ranges = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
    for min_s, max_s in score_ranges:
        count = len(df[(df['Score'] >= min_s) & (df['Score'] < max_s)])
        print(f"  {min_s}-{max_s}: {count} texts")
    
    return df

if __name__ == "__main__":
    df = main()