from bs4 import BeautifulSoup
import minify_html  # type: ignore

minified_links = [
  ["https://docs.google.com/forms/d/e/1FAIpQLSdAL2PzavyrtXgGmtNrZAMyh3hV6g3fU0chxhWFxunQEZtH0g/viewform", "L#1@"],
  ["https://docs.google.com/forms/d/e/1FAIpQLSf9boBe7k5tCwq7LdWgBHHGIPVc4ROO5yjVDo1X5LDAxkmGWQ/viewform", "L#2@"],
  ["https://docs.google.com/forms/d/e/1FAIpQLSfKUBx-icfRCWmhHqUwzX60BVQE21s_NERNfU2VvbjEfE371A/viewform", "L#3@"],
  ["https://docs.google.com/forms/d/e/1FAIpQLSfResxEUiRCyFITWPkzoQ2HhHEvUS5fyg68Rl28hFH6vhHlaA/viewform", "L#4@"],
  ["GoldenDict", "Tipitakapali.org"],
]


def cleanup(html_content, counter):
    # Split HTML at <body> to extract body content
    if "<body>" not in html_content:
        return ""
    parts = html_content.split("<body>", 1)
    if len(parts) != 2:
        print("<body> split not equal 2")

    body_content = html_content.split("<body>", 1)[1]
    # Parse body content with BeautifulSoup
    soup = BeautifulSoup(body_content, "html.parser")

    # change div class from dpd -> deconstructor
    for div in soup.find_all("div", class_="dpd"):
        div["class"] = "dpd deconstructor"

    # Remove title attributes from all elements
    for element in soup.find_all(True):  # Find all tags
        if element.get("title"):
            del element["title"]

    # Find footer paragraph
    footer = soup.find("p", class_="footer")
    if footer:
        # Find the link containing '=Deconstructor'
        deconstructor_link = None
        for link in footer.find_all("a"):
            if link.get("href") and "=Deconstructor" in link.get("href"):
                deconstructor_link = link.get("href")
                break

        # Replace footer with minified version
        if deconstructor_link:
            # new class is dfooter
            new_footer = soup.new_tag("p", attrs={"class": "footer"})
            new_footer.string = "These word breakups are code-generated. "
            new_link = soup.new_tag(
                "a",
                attrs={"class": "link", "href": deconstructor_link, "target": "_blank"},
            )
            new_link.string = "Improve it."
            new_footer.append(new_link)
            footer.replace_with(new_footer)

    
    # Convert to HTML string
    defi = str(soup)

    # Replace links
    for olds, news in minified_links:
        defi = defi.replace(olds, news)

    defi = minify_html.minify(defi)

    return defi.strip()


if __name__ == "__main__":

    # Test with the provided HTML
    aa = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><link href="dpd-css-and-fonts.css" rel="stylesheet"><title>DPD Deconstructor</title><style>:root {/* Background in light mode, text in dark mode */--light: hsl(198, 100%, 95%);--light-shade: hsl(198, 100%, 93%);/* Background in dark mode, text in light mode */--dark: hsl(198, 100%, 5%);--dark-shade: hsl(198, 100%, 7%);/* Primary colour used for logo, buttons, etc */--primary: hsl(198, 100%, 50%);/* Primary alternative used for pressed buttons */--primary-alt: hsl(205, 100%, 40%);/* Primary colour suitable for text in light and dark mode */--primary-text: hsl(205, 79%, 48%);/* Button shadows */--shadow-default: 2px 2px 4px hsla(0, 0%, 20%, 0.4);--shadow-hover: 2px 2px 4px hsla(0, 0%, 20%, 0.5);/* Various grays */--gray: hsl(0, 0%, 50%);--gray-light: hsl(0, 0%, 75%);--gray-dark: hsl(0, 0%, 25%);--gray-transparent: hsla(0, 0%, 50%, 0.25);/* Secondary colour just for help and abbreviations */--secondary: hsl(158, 100%, 35%);/* Frequency heatmap  */--freq0: hsla(198, 90%, 50%, 0.10);--freq1: hsla(200, 90%, 50%, 0.20);--freq2: hsla(202, 90%, 50%, 0.30);--freq3: hsla(204, 90%, 50%, 0.40);--freq4: hsla(206, 90%, 50%, 0.50);--freq5: hsla(208, 90%, 50%, 0.60);--freq6: hsla(210, 90%, 50%, 0.70);--freq7: hsla(212, 90%, 50%, 0.80);--freq8: hsla(214, 90%, 50%, 0.90);--freq9: hsla(216, 90%, 50%, 1.00);--freq10: hsla(218, 90%, 50%, 1.00);}</style></head><body><div class=dpd><p title="abbhānāraha + kāle + api">abbhānāraha + kāle + api<p class=footer>For more information, please <a class=link href=https://digitalpalidictionary.github.io/features/deconstructor/ target=_blank>read the docs</a>. These word breakups are code-generated. Please <a class=link href=https://docs.google.com/forms/d/e/1FAIpQLSf9boBe7k5tCwq7LdWgBHHGIPVc4ROO5yjVDo1X5LDAxkmGWQ/viewform?usp=pp_url&entry.438735500=byābādhissantīti&entry.326955045=Deconstructor&entry.1433863141=GoldenDict%202025-04-13 target=_blank>suggest any improvements here</a>. Mistakes in deconstruction are usually caused by a word missing from the dictionary. <a class=link href=https://docs.google.com/forms/d/e/1FAIpQLSfResxEUiRCyFITWPkzoQ2HhHEvUS5fyg68Rl28hFH6vhHlaA/viewform?usp=pp_url&entry.1433863141=GoldenDict+2025-04-13 target=_blank>Add missing words here</a>.</div>"""

    print(cleanup(aa, 0))
