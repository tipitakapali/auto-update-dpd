import re
from extract_feedback_word_id import extract_feedback_word_id



find_freq = r'<a class="button" data-target="frequency_[^"]*" href="#">frequency</a>'
fb_button = r'<a class="button" data-target="feedback_[^"]*" href="#">feedback</a>'


find_freq_div = (
    r'<div class="content hidden" id="frequency_[^"]*">.*?log it here.*?</div>'
)
find_feedback_div = r'<div class="content hidden" id="feedback_[^"]*">.*?</div>'
find_feedback_div_gettext = r'<div class="content hidden" id="feedback_[^"]*">(.*?)</div>'

find_declension_id = r'<a class="button" data-target="declension_([^"]*)" href="#">declension</a>'
find_declension_div_gettext = r'<div class="content hidden" id="declension_[^"]*">(.*?)</div>'
 
find_conjugation_id = r'<a class="button" data-target="conjugation_([^"]*)" href="#">conjugation</a>'
find_conjugation_div_gettext = r'<div class="content hidden" id="conjugation_[^"]*">(.*?)</div>'
 

def min_defi(defi, kk):
    """Replaces specific patterns in the definition text."""
    if defi:
        # remove frequency elements
        defi = re.sub(find_freq, "", defi)
        defi = re.sub(find_freq_div, "", defi, flags=re.DOTALL)

        real_feedback_word_url = extract_feedback_word_id(defi, find_feedback_div_gettext, start_pattern="entry.438735500=", end_pattern="&entry")

        # Replace <a> tags with the specified pattern and unique counter
        re_fb_button = f'<a class="button" data-target="fb{kk}" href="#">fb</a>'
        defi = re.sub(fb_button, re_fb_button, defi)

        # Replace <div> tags with the specified pattern and unique counter
        re_fback_div = (
            f'<div class="content hidden" id="fb{kk}">fe33db3k_{real_feedback_word_url}_h3r3</div>'
        )
        defi = re.sub(
            find_feedback_div, re_fback_div, defi, flags=re.DOTALL
        )

        # extract declention, conjugation id and delete its content (heavy, rarely use, click on it to fetch separately)
        declension_id = ""
        declension_text = ""
        conjugation_id = ""
        conjugation_text = ""
        
        de_match = re.search(find_declension_id, defi)
        if de_match:
            declension_id = de_match.group(1)
        con_match = re.search(find_conjugation_id, defi)
        if con_match:
            conjugation_id = con_match.group(1)
        
        if declension_id:
            match_divcont = re.search(find_declension_div_gettext, defi)
            if match_divcont:
                declension_text = match_divcont.group(1)
            decl_holder = f'<div class="content hidden" id="declension_{declension_id}"></div>'
            defi = re.sub(
                find_declension_div_gettext, decl_holder, defi, flags=re.DOTALL
            )
            
        if conjugation_id:
            matchc = re.search(find_conjugation_div_gettext, defi)
            if matchc:
                conjugation_text = matchc.group(1)
            conju_holder = f'<div class="content hidden" id="conjugation_{conjugation_id}"></div>'
            defi = re.sub(
                find_conjugation_div_gettext, conju_holder, defi, flags=re.DOTALL
            )

    return defi, (declension_id, declension_text), (conjugation_id, conjugation_text)
