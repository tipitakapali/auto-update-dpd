# Changing remove/replace order = not working !
rm1 = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta data_key="""

rm2 = """<title>Digital Pāḷi Dictionary</title><link href="dpd.css" rel="stylesheet"><link href="family_compound_json.js" class="load_js" rel="preload" as="script"><link href="family_compound_template.js" class="load_js" rel="preload" as="script"><link href="family_idiom_json.js" class="load_js" rel="preload" as="script"><link href="family_idiom_template.js" class="load_js" rel="preload" as="script"><link href="family_root_json.js" class="load_js" rel="preload" as="script"><link href="family_root_template.js" class="load_js" rel="preload" as="script"><link href="family_set_json.js" class="load_js" rel="preload" as="script"><link href="family_set_template.js" class="load_js" rel="preload" as="script"><link href="family_word_json.js" class="load_js" rel="preload" as="script"><link href="family_word_template.js" class="load_js" rel="preload" as="script"><link href="feedback_template.js" class="load_js" rel="preload" as="script"><link href="main.js" class="load_js" rel="preload" as="script" as="script">"""


rm3 = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><link href="dpd.css" rel="stylesheet"><title>Digital Pāḷi Dictionary</title></head><body>"""

rm4 = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><link href="dpd.css" rel="stylesheet"><title>Digital Pāḷi Dictionary</title></head><body>'


s0 = """https://docs.google.com/forms/d/e/1FAIpQLSfResxEUiRCyFITWPkzoQ2HhHEvUS5fyg68Rl28hFH6vhHlaA/viewform?usp=pp_url"""
s0r = "@#@@@"

s1 = r"https://docs.google.com/forms/d/e/1FAIpQLSf9boBe7k5tCwq7LdWgBHHGIPVc4ROO5yjVDo1X5LDAxkmGWQ/viewform?usp=pp_url"
s1r = r"@@@##"


s2 = r"https://docs.google.com/forms/d/e/1FAIpQLSdAL2PzavyrtXgGmtNrZAMyh3hV6g3fU0chxhWFxunQEZtH0g/viewform?usp=pp_url"
s2r = r"@#@#@"

s3 = r"https://docs.google.com/forms/d/e/1FAIpQLSdAL2PzavyrtXgGmtNrZAMyh3hV6g3fU0chxhWFxunQEZtH0g/viewform?usp=pp_url"
s3r = r"@###@###@"

s4 = 'var progName = "GoldenDict"'
s4r = 'var progName = "tipitakapali.org"'

s5 = r"""Inflections not found in the Chaṭṭha Saṅgāyana corpus, or within processed sandhi compounds are <span class="gray">grayed out</span>. They might still occur elsewhere, within compounds or in other versions of the Pāḷi texts.</p><p class="footer">Did you spot a mistake in the declension table? Something missing? <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSfKUBx-icfRCWmhHqUwzX60BVQE21s_NERNfU2VvbjEfE371A/viewform?usp=pp_url"""

s5r = r"$#$@$"

s6 = "=GoldenDict"
s6r = "=tipitakapali.org"

s7 = '<a onclick="button_click(this)" class="button" data-target'
s7r = '<a class="button" data-target'


# rm1?
removes = [rm2, rm3, rm4]
replaces = {s0: s0r, s1: s1r, s2: s2r, s3: s3r, s4: s4r, s5: s5r, s6: s6r, s7: s7r}


def replace_defi(defi, counter):
    for rm in removes:
        defi = defi.replace(rm, "")
    for k, v in replaces.items():
        defi = defi.replace(k, v)
    return defi.strip()
