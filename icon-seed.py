from selenium import webdriver
import time

driver = webdriver.Chrome('C://Users/lucas/chromedriver.exe')
link = 'https://thenounproject.com/search/?q='
icons = {}


def get_product_names(link):
    """Get product names from file
    Parse for search terms
    Use selenium to get icons"""



    with open('products.txt') as filename:
        for line in filename:
            print(line)
            line = line.rstrip().lower().split("|")
            product_id, term = line
            term = term.split()
            term = term[::-1]
            icon_exists = False

            for word in term:
                if word in list(icons.keys()):
                    icons[word]['products'].append(product_id)
                    icon_exists = True
                    print("exists!")
                elif word[:-1] in icons.keys():
                    icons[word[:-1]]['products'].append(product_id)
                    icon_exists = True
                    print("exists!")

            if not icon_exists:
                use_term = False
                if ')' in term[0]:
                    for word in term:
                        if use_term:
                            term = word
                            break
                        elif '(' in word:
                            use_term = True
                else:
                    term = term[0]

                print(term)
                driver.get(link + term)
                time.sleep(3)
                try:
                    icon = driver.find_element_by_css_selector("div.Grid-cell.loaded")  # div
                except:
                    continue
                image = icon.find_element_by_tag_name('img').get_attribute("src")
                driver.get(icon.find_element_by_tag_name('a').get_attribute("href"))
                time.sleep(3)
                try:
                    name = driver.find_element_by_css_selector("h1.main-term").text  # h1
                except:
                    name = 'not found'
                try:
                    designer = driver.find_element_by_css_selector("span.designer").text  # span
                except:
                    designer = 'not found'
                icons[term] = {"products": [product_id]}
                icons[term]["link"] = image
                icons[term]["credit"] = name + " " + designer
                print("Success!")


def write_to_file(icons):
    """Writes info from Selenium to file for use in pSQL later"""

    with open('icons.txt', 'w') as file1:
        for icon in icons:

            try:
                credit = icons[icon]["credit"].decode('utf8')
            except:
                credit = "Uncredited"
            file1.write('{} | {} | {}\n'.format(icon, credit, icons[icon]["link"]))

    with open('product_icons.txt', 'w') as file2:
        for icon in icons:
            for product in icons[icon]["products"]:
                file2.write('{} | {}\n'.format(icon, product))


get_product_names(link)
driver.close()
write_to_file(icons)
print(icons)
