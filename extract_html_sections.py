import re

with open('milld_home.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's extract the HTML for each section
def extract_section(start_str, end_str):
    pos1 = text.find(start_str)
    if pos1 == -1:
        return ""
    pos2 = text.find(end_str, pos1)
    if pos2 == -1:
        return ""
    return text[pos1:pos2+len(end_str)]

hero_html = extract_section('<div id="shopify-section-sections--23901871505624__header', '<!-- END HERO -->')
if not hero_html:
    # Look for milld-hs
    p1 = text.find('class="milld-hs"')
    if p1 != -1:
        start = text.rfind('<section', 0, p1)
        end = text.find('</section>', p1) + len('</section>')
        hero_html = text[start:end]

print("Hero length:", len(hero_html))

pg_html = extract_section('class="pg-section">', '</section>')
print("PG section length:", len(pg_html))

rr_html = extract_section('class="rr-section">', '</section>')
print("RR section length:", len(rr_html))

bc_html = extract_section('class="bc-section">', '</section>')
print("BC section length:", len(bc_html))

ss_html = extract_section('class="ss-section">', '</section>')
print("SS section length:", len(ss_html))

tm_html = extract_section('class="tm-section"', '</section>')
print("TM section length:", len(tm_html))

faq_html = extract_section('class="faq-section"', '</section>')
print("FAQ section length:", len(faq_html))
