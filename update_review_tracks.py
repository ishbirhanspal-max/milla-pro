with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Locate the review container
start_token = '<div class="tm-scroll tm-scroll--reviews" id="tm-reviews-template--23901876781272__testimonials_6TEXnH">'
end_token = '</div>\n      </div>\n    </section>\n\n    <!-- 10. FREQUENTLY ASKED QUESTIONS'

s_idx = text.find(start_token)
e_idx = text.find(end_token)

if s_idx == -1 or e_idx == -1:
    print(f"Error finding tokens: s_idx={s_idx}, e_idx={e_idx}")
    exit(1)

inner_reviews = text[s_idx + len(start_token):e_idx]

# Let's extract track 1
t1_start = inner_reviews.find('<div class="tm-track">')
t1_end = inner_reviews.find('</div>', t1_start)
# A track has multiple nested divs, so let's find the closing tag for <div class="tm-track">
# Each track contains 6 <figure class="tm-review">
# Let's find by splitting or regex
tracks = re.findall(r'<div class="tm-track"[^>]*>[\s\S]*?</div>\s*(?=<div class="tm-track"|$)', inner_reviews)
print(f"Found {len(tracks)} tracks in reviews container")

if len(tracks) >= 1:
    track_single = tracks[0]
    # Ensure aria-hidden is on clones
    track_base = re.sub(r'aria-hidden="true"\s*', '', track_single)
    track_clone = track_base.replace('<div class="tm-track">', '<div class="tm-track" aria-hidden="true">')
    
    # 4 tracks total: 2 in Set A, 2 in Set B (total 24 cards = 8256px wide)
    new_inner = f"\n          <!-- Track 1 (Set A) -->\n          {track_base}\n          <!-- Track 2 (Set A) -->\n          {track_clone}\n          <!-- Track 3 (Set B - Clone for Infinite 60fps GPU Marquee) -->\n          {track_clone}\n          <!-- Track 4 (Set B - Clone for Infinite 60fps GPU Marquee) -->\n          {track_clone}\n        "
    
    new_text = text[:s_idx + len(start_token)] + new_inner + text[e_idx:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Successfully updated index.html with 4 robust tracks!")
