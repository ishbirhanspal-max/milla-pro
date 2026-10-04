import os
import re

with open('milld_home.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's extract the styles
styles = re.findall(r'<style[^>]*>(.*?)</style>', text, re.DOTALL)
print(f"Extracted {len(styles)} style tags")

# Save the component styles for reference
component_css = ""
for i, s in enumerate(styles):
    for sec in ['milld-hs', 'pg-section', 'rr-section', 'bc-section', 'ss-section', 'tm-section', 'faq-section']:
        if sec in s:
            component_css += f"/* === {sec.upper()} === */\n" + s + "\n\n"

with open('milld_components.css', 'w', encoding='utf-8') as f:
    f.write(component_css)

print(f"Saved milld_components.css ({len(component_css):,} bytes)")
