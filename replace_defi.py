import re


# Do not change this manual remove/replace order
remove_str_1 = (
    """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta data_key="""
)

remove_str_2 = """<title>Digital Pāḷi Dictionary</title><link href="dpd.css" rel="stylesheet"><link href="family_compound_json.js" class="load_js" rel="preload" as="script"><link href="family_compound_template.js" class="load_js" rel="preload" as="script"><link href="family_idiom_json.js" class="load_js" rel="preload" as="script"><link href="family_idiom_template.js" class="load_js" rel="preload" as="script"><link href="family_root_json.js" class="load_js" rel="preload" as="script"><link href="family_root_template.js" class="load_js" rel="preload" as="script"><link href="family_set_json.js" class="load_js" rel="preload" as="script"><link href="family_set_template.js" class="load_js" rel="preload" as="script"><link href="family_word_json.js" class="load_js" rel="preload" as="script"><link href="family_word_template.js" class="load_js" rel="preload" as="script"><link href="feedback_template.js" class="load_js" rel="preload" as="script"><link href="main.js" class="load_js" rel="preload" as="script" as="script">"""

remove_str_3 = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><link href="dpd.css" rel="stylesheet"><title>Digital Pāḷi Dictionary</title></head><body>"""

remove_str_4 = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><link href="dpd.css" rel="stylesheet"><title>Digital Pāḷi Dictionary</title></head><body>'

remove_str_5 = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><link href="deconstructor.css" rel="stylesheet"><title>DPD Deconstructor</title></head><body>"""


remove_list = [remove_str_2, remove_str_3, remove_str_4, remove_str_5]

replace_list = [
    ['var progName = "GoldenDict"', 'var progName = "Tipitakapali.org"'],
    ["=GoldenDict", "=Tipitakapali.org"],
    [
        '<a onclick="button_click(this)" class="button" data-target',
        '<a class="button" data-target',
    ],
    [
        "<p class=deconstructor_footer>These word breakups",
        "<p class=deconstructor_footer>These word breakups",
    ],
    [
        "https://docs.google.com/forms/d/1iMD9sCSWFfJAFCFYuG9HRIyrr9KFRy0nAOVApM998wM/viewform",
        "L#1@",
    ],
    [
        "https://docs.google.com/forms/d/e/1FAIpQLScNC5v2gQbBCM3giXfYIib9zrp-WMzwJuf_iVXEMX2re4BFFw/viewform",
        "L#2@",
    ],
    [
        "https://docs.google.com/forms/d/e/1FAIpQLSdAL2PzavyrtXgGmtNrZAMyh3hV6g3fU0chxhWFxunQEZtH0g/viewform",
        "L#3@",
    ],
    [
        "https://docs.google.com/forms/d/e/1FAIpQLSf9boBe7k5tCwq7LdWgBHHGIPVc4ROO5yjVDo1X5LDAxkmGWQ/viewform",
        "L#4@",
    ],
    [
        "https://docs.google.com/forms/d/e/1FAIpQLSfKUBx-icfRCWmhHqUwzX60BVQE21s_NERNfU2VvbjEfE371A/viewform",
        "L#5@",
    ],
    [
        "https://docs.google.com/forms/d/e/1FAIpQLSfResxEUiRCyFITWPkzoQ2HhHEvUS5fyg68Rl28hFH6vhHlaA/viewform",
        "L#6@",
    ],
]


def replace_defi(defi, counter):
    pattern = r"Please suggest any improvements here\.\</a> <br>Mistakes in deconstruction are usually caused by a word missing from the dictionary\.\ <a class=link href=https://docs\.google\.com/forms/d/e/1FAIpQLSfResxEUiRCyFITWPkzoQ2HhHEvUS5fyg68Rl28hFH6vhHlaA/viewform\?usp=pp_url&entry\.1433863141=.*?target=_blank>Add missing words here</a>\."

    replacement = "Improve it.</a></p>"
    defi = re.sub(pattern, replacement, defi)

    for rm in remove_list:
        defi = defi.replace(rm, "")
    for k, v in replace_list:
        defi = defi.replace(k, v)
    return defi.strip()