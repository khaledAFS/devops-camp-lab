from selenium import webdriver
import time

driver = webdriver.Chrome('C://Users/lucas/chromedriver.exe')
link = 'https://thenounproject.com/search/?q='
icons = {}


def get_product_names(link):
    """Get product names from file
    Parse for search terms
    Use selenium to get icons"""

    # icons = {"apple": {"products": [], "link": url, "credit": credit}}

    with open('products.txt') as filename:
        for line in filename:
            print(line)
            line = line.rstrip().lower().split("|")
            product_id, term = line
            term = term.split()
            term = term[::-1]
            icon_exists = False

            for word in term:
                if word in icons:
                    icons[word]['products'].append(product_id)
                    icon_exists = True
                    print("exists!")
                    continue
                elif word[:-1] in icons:
                    icons[word[:-1]]['products'].append(product_id)
                    icon_exists = True
                    print("exists!")
                    continue

            if not icon_exists:
                term = term[0]
                print(term)
                driver.get(link + term)
                time.sleep(4)
                try:
                    icon = driver.find_element_by_css_selector("div.Grid-cell.loaded")  # div
                except Exception:
                    continue
                image = icon.find_element_by_tag_name('img').get_attribute("src")
                driver.get(icon.find_element_by_tag_name('a').get_attribute("href"))
                time.sleep(4)
                try:
                    name = driver.find_element_by_css_selector("h1.main-term").text  # h1
                    designer = driver.find_element_by_css_selector("span.designer").text  # span
                except Exception:
                    continue
                icons[term] = {"products": [product_id]}
                icons[term]["link"] = image
                icons[term]["credit"] = name + " " + designer
                print("Success!")


def write_to_file(icons):
    """Writes info from Selenium to file for use in pSQL later"""

    with open('icons.txt', 'a') as file1:
        for icon in icons:
            file1.write(icon)
            file1.write("|")
            try:
                file1.write(icons[icon]["credit"].decode('utf8'))
            except Exception:
                file1.write("Uncredited")
            file1.write("|")
            file1.write(icons[icon]["link"])
            file1.write("\n")

    with open('product_icons.txt', 'a') as file2:
        for icon in icons:
            for product in icons[icon]["products"]:
                file2.write(icon)
                file2.write("|")
                file2.write(product)
                file2.write("\n")


get_product_names(link)
driver.close()
write_to_file(icons)
print(icons)
