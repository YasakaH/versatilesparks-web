"""Fetch YouTube transcripts with delays to avoid IP block"""
import time, os
from youtube_transcript_api import YouTubeTranscriptApi

OUT = r'C:\Users\varas\personalities'
videos = {
    'semrush_ai_visibility': '5dZSJwaCj_Y',
    'ai_search_marketing': '73_APaOtvIw',
    'brand_strategy_ai': 'TX-voD3F_Bk',
    'seo_ai_future': '0hgmb5u6Rh0',
    'competitor_intelligence': '1x3qiGtbhtE',
    'digital_pr_strategy': 'y0DGEa_84Mo',
}

for name, vid in videos.items():
    path = os.path.join(OUT, f'transcript_{name}.txt')
    if os.path.exists(path):
        print(f'⏭️ {name} already exists, skipping')
        continue
    
    for attempt in range(3):
        try:
            result = YouTubeTranscriptApi().fetch(vid, languages=['en'])
            text = ' '.join([s.text for s in result.snippets])
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f'✅ {name}: {len(text)} chars saved')
            time.sleep(5)  # Delay between requests
            break
        except Exception as e:
            print(f'⚠️ {name} attempt {attempt+1}: {str(e)[:60]}')
            if attempt < 2:
                print(f'   Waiting {30*(attempt+1)}s before retry...')
                time.sleep(30*(attempt+1))
            else:
                print(f'❌ {name} failed after 3 attempts')
