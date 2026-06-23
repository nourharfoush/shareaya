import urllib.request
import re
import ssl
import json
import os

# Ignore SSL certificate verification issues
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# List of URLs to scrape
URLS = {
    # Level 1
    "level1_quran": "https://www.alquranulhakeem.net/Rowaq/Rowaq_Intr_Stage_Level_1_Quran.html",
    "level1_aqidah": "https://www.alquranulhakeem.net/Rowaq/Rowaq_Intr_Stage_Level_1_Aqidah.html",
    "level1_tafseer": "https://www.alquranulhakeem.net/Rowaq/Rowaq_Intr_Stage_Level_1_Tafseer.html",
    "level1_hadith": "https://www.alquranulhakeem.net/Rowaq/Rowaq_Intr_Stage_Level_1_Hadith.html",
    "level1_fiqh_hanafy": "https://www.alquranulhakeem.net/Rowaq/Rowaq_Intr_Stage_Level_1_Fiqh_Hanafy.html",
    "level1_fiqh_maleky": "https://www.alquranulhakeem.net/Rowaq/Rowaq_Intr_Stage_Level_1_Fiqh_Maleky.html",
    "level1_fiqh_shafey": "https://www.alquranulhakeem.net/Rowaq/Rowaq_Intr_Stage_Level_1_Fiqh_Shafey.html",
    "level1_nahw": "https://www.alquranulhakeem.net/Rowaq/Rowaq_Intr_Stage_Level_1_Nahw.html",

    # Level 2
    "level2_quran": "https://www.alquranulhakeem.net/Rowaq/Intro_Level_2/Rowaq_Intr_Stage_Level_2_Quran.html",
    "level2_aqidah": "https://www.alquranulhakeem.net/Rowaq/Intro_Level_2/Rowaq_Intr_Stage_Level_2_Aqidah.html",
    "level2_seerah": "https://www.alquranulhakeem.net/Rowaq/Intro_Level_2/Rowaq_Intr_Stage_Level_2_Seerah.html",
    "level2_hadith": "https://www.alquranulhakeem.net/Rowaq/Intro_Level_2/Rowaq_Intr_Stage_Level_2_Hadith.html",
    "level2_fiqh_hanafy": "https://www.alquranulhakeem.net/Rowaq/Intro_Level_2/Rowaq_Intr_Stage_Level_2_Fiqh_Hanafy.html",
    "level2_fiqh_maleky": "https://www.alquranulhakeem.net/Rowaq/Intro_Level_2/Rowaq_Intr_Stage_Level_2_Fiqh_Maleky.html",
    "level2_fiqh_shafey": "https://www.alquranulhakeem.net/Rowaq/Intro_Level_2/Rowaq_Intr_Stage_Level_2_Fiqh_Shafey.html",
    "level2_nahw": "https://www.alquranulhakeem.net/Rowaq/Intro_Level_2/Rowaq_Intr_Stage_Level_2_Nahw.html",
    "level2_tt": "https://www.alquranulhakeem.net/Rowaq/Intro_Level_2/Rowaq_Intr_Stage_Level_2_T_T.html",

    # MSL 1
    "msl1_quran": "https://www.alquranulhakeem.net/Rowaq/MSL_1/MSL_1_Quran.html",
    "msl1_aqidah": "https://www.alquranulhakeem.net/Rowaq/MSL_1/MSL_1_Aqidah.html",
    "msl1_tafseer": "https://www.alquranulhakeem.net/Rowaq/MSL_1/MSL_1_Tafseer.html",
    "msl1_hadith": "https://www.alquranulhakeem.net/Rowaq/MSL_1/MSL_1_Hadith.html",
    "msl1_fiqh_hanafy": "https://www.alquranulhakeem.net/Rowaq/MSL_1/MSL_1_Fiqh_Hanafy.html",
    "msl1_fiqh_maleky": "https://www.alquranulhakeem.net/Rowaq/MSL_1/MSL_1_Fiqh_Maleky.html",
    "msl1_fiqh_shafey": "https://www.alquranulhakeem.net/Rowaq/MSL_1/MSL_1_Fiqh_Shafey.html",
    "msl1_adab": "https://www.alquranulhakeem.net/Rowaq/MSL_1/MSL_1_Adab.html",

    # MSL 2
    "msl2_tar": "https://www.alquranulhakeem.net/Rowaq/MSL_2/MSL_2_Tar.html",
    "msl2_tasawof": "https://www.alquranulhakeem.net/Rowaq/MSL_2/MSL_2_Tasawof.html",
    "msl2_feraq": "https://www.alquranulhakeem.net/Rowaq/MSL_2/MSL_2_Feraq.html",
    "msl2_qadaya": "https://www.alquranulhakeem.net/Rowaq/MSL_2/MSL_2_Qadaya.html",
    "msl2_osool": "https://www.alquranulhakeem.net/Rowaq/MSL_2/MSL_2_Osool_Fiqh.html",
    "msl2_fiqh_hanafy": "https://www.alquranulhakeem.net/Rowaq/MSL_2/MSL_1_Fiqh_Hanafy.html",
    "msl2_fiqh_maleky": "https://www.alquranulhakeem.net/Rowaq/MSL_2/MSL_1_Fiqh_Maleky.html",
    "msl2_fiqh_shafey": "https://www.alquranulhakeem.net/Rowaq/MSL_2/MSL_1_Fiqh_Shafey.html",
    "msl2_fiqh_hanbaly": "https://www.alquranulhakeem.net/Rowaq/MSL_2/MSL_1_Fiqh_Hanbaly.html",
    "msl2_balagha": "https://www.alquranulhakeem.net/Rowaq/MSL_2/MSL_2_Balagha.html",

    # Advanced Stage - Tafseer Level 1 subjects
    "asl1_quran": "https://www.alquranulhakeem.net/Rowaq/ASL/Tafseer/Tafseer_1/ASL_Tafseer_1_Quran.html",
    "asl1_oloom": "https://www.alquranulhakeem.net/Rowaq/ASL/Tafseer/Tafseer_1/ASL_Tafseer_1_Oloom_Quraan.html",
    "asl1_aqidah": "https://www.alquranulhakeem.net/Rowaq/ASL/Tafseer/Tafseer_1/ASL_Tafseer_1_Aqidah.html",
    "asl1_tafseer_ta": "https://www.alquranulhakeem.net/Rowaq/ASL/Tafseer/Tafseer_1/ASL_Tafseer_1_Tafseer_Ta.html",
    "asl1_tafseer_ma": "https://www.alquranulhakeem.net/Rowaq/ASL/Tafseer/Tafseer_1/ASL_Tafseer_1_Tafseer_Ma.html",
    "asl1_hadith": "https://www.alquranulhakeem.net/Rowaq/ASL/Tafseer/Tafseer_1/ASL_Tafseer_1_Hadith.html",
    "asl1_fiqh": "https://www.alquranulhakeem.net/Rowaq/ASL/Tafseer/Tafseer_1/ASL_Tafseer_1_Fiqh_Moqaran.html",
    "asl1_manahej": "https://www.alquranulhakeem.net/Rowaq/ASL/Tafseer/Tafseer_1/ASL_Tafseer_1_Manahej.html",
}

# Mapping key to descriptive metadata
METADATA_DEFAULTS = {
    # Level 1
    "level1_quran": {"title": "تجويد", "stage": "المرحلة التمهيدية - المستوى الأول"},
    "level1_aqidah": {"title": "عقيدة", "stage": "المرحلة التمهيدية - المستوى الأول"},
    "level1_tafseer": {"title": "تفسير تحليلي", "stage": "المرحلة التمهيدية - المستوى الأول"},
    "level1_hadith": {"title": "حديث تحليلي", "stage": "المرحلة التمهيدية - المستوى الأول"},
    "level1_fiqh_hanafy": {"title": "فقه حنفي", "stage": "المرحلة التمهيدية - المستوى الأول"},
    "level1_fiqh_maleky": {"title": "فقه مالكي", "stage": "المرحلة التمهيدية - المستوى الأول"},
    "level1_fiqh_shafey": {"title": "فقه شافعي", "stage": "المرحلة التمهيدية - المستوى الأول"},
    "level1_nahw": {"title": "نحو و صرف", "stage": "المرحلة التمهيدية - المستوى الأول"},

    # Level 2
    "level2_quran": {"title": "علوم القرآن", "stage": "المرحلة التمهيدية - المستوى الثاني"},
    "level2_aqidah": {"title": "عقيدة و تصوف", "stage": "المرحلة التمهيدية - المستوى الثاني"},
    "level2_seerah": {"title": "السيرة النبوية", "stage": "المرحلة التمهيدية - المستوى الثاني"},
    "level2_hadith": {"title": "مصطلح الحديث", "stage": "المرحلة التمهيدية - المستوى الثاني"},
    "level2_fiqh_hanafy": {"title": "فقه حنفي", "stage": "المرحلة التمهيدية - المستوى الثاني"},
    "level2_fiqh_maleky": {"title": "فقه مالكي", "stage": "المرحلة التمهيدية - المستوى الثاني"},
    "level2_fiqh_shafey": {"title": "فقه شافعي", "stage": "المرحلة التمهيدية - المستوى الثاني"},
    "level2_nahw": {"title": "نحو و صرف", "stage": "المرحلة التمهيدية - المستوى الثاني"},
    "level2_tt": {"title": "تاريخ التشريع", "stage": "المرحلة التمهيدية - المستوى الثاني"},

    # MSL 1
    "msl1_quran": {"title": "قرآن كريم و تجويد", "stage": "المرحلة المتوسطة - المستوى الأول"},
    "msl1_aqidah": {"title": "عقيدة", "stage": "المرحلة المتوسطة - المستوى الأول"},
    "msl1_tafseer": {"title": "تفسير", "stage": "المرحلة المتوسطة - المستوى الأول"},
    "msl1_hadith": {"title": "حديث", "stage": "المرحلة المتوسطة - المستوى الأول"},
    "msl1_fiqh_hanafy": {"title": "فقه حنفي", "stage": "المرحلة المتوسطة - المستوى الأول"},
    "msl1_fiqh_maleky": {"title": "فقه مالكي", "stage": "المرحلة المتوسطة - المستوى الأول"},
    "msl1_fiqh_shafey": {"title": "فقه شافعي", "stage": "المرحلة المتوسطة - المستوى الأول"},
    "msl1_adab": {"title": "أدب", "stage": "المرحلة المتوسطة - المستوى الأول"},

    # MSL 2
    "msl2_tar": {"title": "تاريخ الحضارة الإسلامية", "stage": "المرحلة المتوسطة - المستوى الثاني"},
    "msl2_tasawof": {"title": "تصوف", "stage": "المرحلة المتوسطة - المستوى الثاني"},
    "msl2_feraq": {"title": "فرق إسلامية", "stage": "المرحلة المتوسطة - المستوى الثاني"},
    "msl2_qadaya": {"title": "قضايا معاصرة", "stage": "المرحلة المتوسطة - المستوى الثاني"},
    "msl2_osool": {"title": "أصول الفقه", "stage": "المرحلة المتوسطة - المستوى الثاني"},
    "msl2_fiqh_hanafy": {"title": "فقه حنفي", "stage": "المرحلة المتوسطة - المستوى الثاني"},
    "msl2_fiqh_maleky": {"title": "فقه مالكي", "stage": "المرحلة المتوسطة - المستوى الثاني"},
    "msl2_fiqh_shafey": {"title": "فقه شافعي", "stage": "المرحلة المتوسطة - المستوى الثاني"},
    "msl2_fiqh_hanbaly": {"title": "فقه حنبلي", "stage": "المرحلة المتوسطة - المستوى الثاني"},
    "msl2_balagha": {"title": "لغة عربية (بلاغة)", "stage": "المرحلة المتوسطة - المستوى الثاني"},

    # Advanced Stage - Tafseer Level 1 subjects
    "asl1_quran": {"title": "القرآن الكريم و التجويد", "stage": "المرحلة المتقدمة - شعبة التفسير والحديث"},
    "asl1_oloom": {"title": "علوم قرآن", "stage": "المرحلة المتقدمة - شعبة التفسير والحديث"},
    "asl1_aqidah": {"title": "عقيدة", "stage": "المرحلة المتقدمة - شعبة التفسير والحديث"},
    "asl1_tafseer_ta": {"title": "تفسير تحليلي", "stage": "المرحلة المتقدمة - شعبة التفسير والحديث"},
    "asl1_tafseer_ma": {"title": "تفسير موضوعي", "stage": "المرحلة المتقدمة - شعبة التفسير والحديث"},
    "asl1_hadith": {"title": "حديث تحليلي", "stage": "المرحلة المتقدمة - شعبة التفسير والحديث"},
    "asl1_fiqh": {"title": "فقه مقارن", "stage": "المرحلة المتقدمة - شعبة التفسير والحديث"},
    "asl1_manahej": {"title": "مناهج مفسرين", "stage": "المرحلة المتقدمة - شعبة التفسير والحديث"},
}

result_data = {}

for key, url in URLS.items():
    print(f"Scraping {key}: {url} ...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            html = response.read().decode('utf-8')
            
            # Find subject title
            # Let's check defaults first, and override if we find a header
            default_meta = METADATA_DEFAULTS.get(key, {"title": "مادة دراسية", "stage": "رواق الأزهر"})
            title = default_meta["title"]
            stage = default_meta["stage"]
            
            # Find all h1 tags (some pages have headings for lecture num and title)
            # Find text inside h1 tags with class mydiv_1
            headings = re.findall(r'<h1[^>]*class="mydiv_1"[^>]*>([^<]+)</h1>', html, re.IGNORECASE)
            
            # Find all youtube embeds
            youtube_ids = re.findall(r'youtube\.com/embed/([a-zA-Z0-9_-]+)', html, re.IGNORECASE)
            
            # Find all Google Drive/external notes URLs in buttons in the bottom
            # Typically looks like: onclick=" window.open('https://drive.google.com/file/d/...' or similar
            drive_links = re.findall(r"window\.open\(\s*'([^']+)'", html)
            pdf_link = ""
            for link in drive_links:
                if "drive.google.com" in link or "Al_Kotob" in link or "kotob" in link:
                    # Let's keep the drive link which is for the lectures notes
                    if "sharing" in link or "/view" in link:
                        pdf_link = link
                        break
            if not pdf_link and drive_links:
                # Fallback to the last opened link if it is drive
                for link in reversed(drive_links):
                    if "drive.google.com" in link:
                        pdf_link = link
                        break
            
            # Match logo image
            # Usually: <img src="([^"]+)" alt="Logo" class="center" ...
            logos = re.findall(r'<img[^>]*src="([^"]+)"', html, re.IGNORECASE)
            logo = "https://www.alquranulhakeem.net/Rowaq/Al_Azhar_Logo_1.jpeg" # Default
            for img in logos:
                if "Logo" in img or "logo" in img or "Rowaq" in img or "Azhar" in img or "Rowaq_0" in img:
                    logo = img
                    if not logo.startswith("http"):
                        # Resolve relative logo urls
                        logo = "https://www.alquranulhakeem.net/Rowaq/" + logo.lstrip("/")
                    break
            if logo == "https://www.alquranulhakeem.net/Rowaq/Al_Azhar_Logo_1.jpeg" and len(logos) > 0:
                logo = logos[0]
                if not logo.startswith("http"):
                    logo = "https://www.alquranulhakeem.net/Rowaq/" + logo.lstrip("/")

            # Clean headings: remove trailing space and comments
            clean_headings = []
            for h in headings:
                h_clean = re.sub(r'<!--.*?-->', '', h).strip()
                if h_clean and h_clean != "المواد المقررة" and "شعبة" not in h_clean:
                    clean_headings.append(h_clean)

            # Pair up headings with YouTube IDs
            # Rowaq pages typically have:
            # - heading 1: "- المحاضرة الأولى -"
            # - heading 2: "عنوان المحاضرة"
            # and then one youtube video.
            # So every video has 2 headings preceding it.
            lectures = []
            
            # Let's find headings and iframes in the order they appear to pair them correctly
            # We can do this by regex search in the entire html text
            items = [] # Will contain tuples of ('heading', text) or ('video', id)
            
            # Simple parser to find order
            pos = 0
            while True:
                h_match = re.search(r'<h1[^>]*class="mydiv_1"[^>]*>(.*?)</h1>', html[pos:], re.DOTALL | re.IGNORECASE)
                v_match = re.search(r'youtube\.com/embed/([a-zA-Z0-9_-]+)', html[pos:], re.IGNORECASE)
                
                if not h_match and not v_match:
                    break
                    
                h_idx = h_match.start() + pos if h_match else float('inf')
                v_idx = v_match.start() + pos if v_match else float('inf')
                
                if h_idx < v_idx:
                    h_text = re.sub(r'<[^>]+>', '', h_match.group(1)) # strip any inner html
                    h_text = re.sub(r'<!--.*?-->', '', h_text).strip()
                    if h_text and h_text != "المواد المقررة" and "شعبة" not in h_text and "المحاضرة" not in h_text:
                        items.append(('title', h_text))
                    elif h_text and "المحاضرة" in h_text:
                        items.append(('num', h_text))
                    pos = h_idx + len(h_match.group(0))
                else:
                    items.append(('video', v_match.group(1)))
                    pos = v_idx + len(v_match.group(0))
            
            # Now build the lectures list by matching videos with their preceding titles
            current_num = ""
            current_title = ""
            for item_type, val in items:
                if item_type == 'num':
                    current_num = val
                elif item_type == 'title':
                    current_title = val
                elif item_type == 'video':
                    full_title = ""
                    if current_num and current_title:
                        full_title = f"{current_num} - {current_title}"
                    elif current_num:
                        full_title = current_num
                    elif current_title:
                        full_title = current_title
                    else:
                        full_title = f"المحاضرة {len(lectures)+1}"
                    
                    # Clean up double dashes or spaces
                    full_title = re.sub(r'\s+', ' ', full_title).replace(" - - ", " - ").strip()
                    
                    lectures.append({
                        "title": full_title,
                        "youtube_id": val
                    })
                    # Reset for next
                    current_num = ""
                    current_title = ""
            
            # Fallback if pairing failed or mismatch: just map youtube_ids with clean headings
            if not lectures and youtube_ids:
                for idx, yid in enumerate(youtube_ids):
                    lbl = f"المحاضرة {idx+1}"
                    # Try to use heading pairs
                    if idx * 2 + 1 < len(clean_headings):
                        lbl = f"{clean_headings[idx*2]} - {clean_headings[idx*2+1]}"
                    elif idx < len(clean_headings):
                        lbl = clean_headings[idx]
                    lectures.append({
                        "title": lbl,
                        "youtube_id": yid
                    })

            result_data[key] = {
                "title": title,
                "stage": stage,
                "logo": logo,
                "pdf_link": pdf_link,
                "lectures": lectures
            }
            print(f"Successfully scraped {len(lectures)} lectures for {key}.")
    except Exception as e:
        print(f"ERROR scraping {key} ({url}): {e}")

# Write to file
output_path = "lectures_data.js"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("// قاعدة بيانات محاضرات رواق العلوم الشرعية والعربية - مولدة تلقائياً\n")
    f.write("const LECTURES_DATA = ")
    f.write(json.dumps(result_data, ensure_ascii=False, indent=2))
    f.write(";\n")

print(f"Extraction completed. Data saved to {output_path}")
