# import packages
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BS

# ====================== SCRAPE SECTION ========================================
# this request to navigate to [all watches page] using selenium
all_watches_url = 'https://www.rogerdubuis.com/sa-en/selection/all-watches'
browser = webdriver.Chrome()
browser.get(all_watches_url)
# to store [all watches page] as [HTML] format
all_watches_html = browser.page_source
browser.quit()

# to parse content of [all_watches_html] using BeautifulSoup
soup = BS(all_watches_html, 'html.parser')

'''
Comprehensive loop to get [href] from [<a href= 'specific watch link'></a>] of all watches
and append it to [all_watches_links].

So now we have all watches links in a LIST
'''
all_watches_links = [a_tag['href'].replace('/sa-en', '') for a_tag in soup.find_all(
    'a', class_='h5 text-base expand-target flex-grow', href=True)]
# ------Print output------
print(len(all_watches_links))  # check how many watches do we have


# this snippet to set up options to run [Chrome] in headless mode
options = Options()
options.add_argument("--headless=new")

# this function to get all HTML contents for each watch using selenium and store it in a LIST


def get_html_for_each_watch(watches_URLs_lst):
    html_format_for_all_watches = []
    for link in watches_URLs_lst:
        browser = webdriver.Chrome(options=options)
        browser.get(link)
        raw_html = browser.page_source
        browser.quit()
        html_format_for_all_watches.append(raw_html)
        time.sleep(2)
    return html_format_for_all_watches


html_format_for_all_watches = get_html_for_each_watch(all_watches_links)
# ------Print output------
print(html_format_for_all_watches)

# this function to parse all HTML contents for each watch using selenium and store it in a LIST


def parse_watches_data(watches_format_lst):
    contents_of_watches_pages = [
        BS(html_format, 'html.parser') for html_format in watches_format_lst]
    return contents_of_watches_pages


contents_of_watches_pages = parse_watches_data(html_format_for_all_watches)
# ------Print output------
print(contents_of_watches_pages)

watches_dict = {
    'reference_number': [],
    'watch_URL': [],
    'type': [],  # Blank values
    'brand': [],
    'year_introduced': [],  # Blank values
    'parent_model': [],
    'specific_model': [],
    'nickname': [],
    'marketing_name': [],
    'style': [],  # Blank values
    'currency': [],
    'price': [],
    'image_URL': [],
    'made_in': [],
    'case_shape': [],  # Blank values
    'case_material': [],
    'case_finish': [],  # Blank values
    'case_back': [],
    'diameter': [],
    'between_lugs': [],  # Blank values
    'lug_to_lug': [],  # Blank values
    'case_thickness': [],  # Blank values
    'bezel_material': [],
    'bezel_color': [],
    'crystal': [],
    'water_resistance': [],
    'weight': [],  # Blank values
    'dial_color': [],
    'numerals': [],
    'bracelet_material': [],
    'bracelet_color': [],
    'clasp_type': [],
    'movement': [],
    'caliber': [],
    'power_reserve': [],
    'frequency': [],
    'jewels': [],
    'features': [],
    'description': [],
    'short_description': []  # Blank values
}

# ------Print output------
# watches_dict

# field_02 = watches_dict['watch_URL']
[watches_dict['watch_URL'].append(watch_link)
 for watch_link in all_watches_links]

for page_content in contents_of_watches_pages:
    for field_value in page_content:
        # field_01 = watches_dict['reference_number']
        try:
            reference_number = field_value.find(
                'div', class_='sgphx-product-banner__title').text.split('\n')[3].split(' ')[12]
        except TypeError:
            reference_number = ''
        watches_dict['reference_number'].append(reference_number)

        # field_03 = watches_dict['type'] >> Blank values
        watch_type = ''
        watches_dict['type'].append(watch_type)

        # field_04 = watches_dict['brand']
        brand = 'Roger Dubuis'
        watches_dict['brand'].append(brand)

        # field_05 = watches_dict['year_introduced']
        year_introduced = ''
        watches_dict['year_introduced'].append(year_introduced)

        # field_06 = watches_dict['parent_model']
        parent_model = field_value.find('div', class_='sgphx-h4').text
        watches_dict['parent_model'].append(parent_model)

        # field_07 = watches_dict['specific_model']
        specific_model = field_value.find('h1', class_='sgphx-h2').text
        specific_model = parent_model + ' ' + specific_model
        watches_dict['specific_model'].append(specific_model)

        # field_08 = watches_dict['nickname']
        nickname = field_value.find('span', class_='sgphx-text-muted').text
        watches_dict['nickname'].append(nickname)

        # field_09 = watches_dict['marketing_name']
        '''
        I try to target class name (sgphx-tag), but it show me more things that not to deal with 
        tags that i am looking for, so i notice that every tag i'm looking for has an attribute
        name (data-cy), so i target this attribute, and i initialize a [marketing_name_tag] LIST
        to append just HTML tags that has only (data-cy) attribute, and before append it i convert it 
        to string preparing to clean it after that as the client want to look.
        '''
        cleaning_marketing_name_tag = []
        tags = field_value.find_all('span', attrs={'data-cy': True})
        for t in tags:
            clean_tag = str(t).split('<')[1].split('>')[-1]
            cleaning_marketing_name_tag.append(clean_tag)
        watch_tags = cleaning_marketing_name_tag[1:]
        # to grouping tags in the list in string syntax
        if len(watch_tags) == 0:
            watch_tags = ''
        elif len(watch_tags) == 1:
            watch_tags = watch_tags[0]
        else:
            watch_tags = ', '.join(watch_tags)
        watches_dict['marketing_name'].append(watch_tags)
        cleaning_marketing_name_tag.clear()

        # field_10 = watches_dict['style']
        style = ''
        watches_dict['style'].append(style)

        # field_11 = watches_dict['currency']
        currency = 'USD'
        watches_dict['currency'].append(currency)

        # field_12 = watches_dict['price']
        '''
        In the website we have a tow categories of price:
        - 'Price upon request' string value
        - string value containing numerical syntax such as '59,000' 
        
        in this snippet i used `if statement` to clean a price values and separate it to
        - (String) for 'Price upon request' value
        - (int) for numerical values by convert it from string syntax
        '''
        price = field_value.find(
            'span', class_='price-from--prices').span.text.split('\n')
        try:
            if price is not None:
                if price[0] == 'Price upon request':
                    price = price[0]
                else:
                    price = price[0][2:].split(',')
                    price = ''.join(price)
                    # Convert the input string containing numerical syntax into an integer value
                    price = int(price)
        except TypeError:
            price = ''
        watches_dict['price'].append(price)

        # field_13 = watches_dict['image_URL']
        image_URL = field_value.find_all(
            'button', class_='sgphx-picture sgphx-picture--actionable sgphx-light-box-trigger')[0].img['data-src']
        watches_dict['image_URL'].append(image_URL)

        # field_14 = watches_dict['made_in']
        made_in = 'Switzerland'
        watches_dict['made_in'].append(made_in)

        # field_15 = watches_dict['case_shape']
        case_shape = ''
        watches_dict['case_shape'].append(case_shape)

        # field_16 = watches_dict['case_material']
        case_material = field_value.find_all(
            'ul', class_='sgphx-tech-details__list')[0].p.text.replace('\n', ' ')
        watches_dict['case_material'].append(case_material)

        # field_17 = watches_dict['case_finish']
        case_finish = ''
        watches_dict['case_finish'].append(case_finish)

        # field_18 = watches_dict['case_back']
        case_back = field_value.find_all(
            'ul', class_='sgphx-tech-details__list')[0].p.text.replace('\n', ' ')
        watches_dict['case_back'].append(case_back)

        # field_19 = watches_dict['diameter']
        diameter = field_value.find_all(
            'div', class_='sgphx-rich-text')[1].ul.li.text.split(':')[-1][1:]
        watches_dict['diameter'].append(diameter)

        # field_20 = watches_dict['between_lugs']
        between_lugs = ''
        watches_dict['between_lugs'].append(between_lugs)

        # field_21 = watches_dict['lug_to_lug']
        lug_to_lug = ''
        watches_dict['lug_to_lug'].append(lug_to_lug)

        # field_22 = watches_dict['case_thickness']
        case_thickness = ''
        watches_dict['case_thickness'].append(case_thickness)

        # field_23 = watches_dict['bezel_material']
        bezel_material = field_value.find_all(
            'ul', class_='sgphx-tech-details__list')[0].p.text.replace('\n', ' ')
        watches_dict['bezel_material'].append(bezel_material)

        # field_24 = watches_dict['bezel_color']
        bezel_color = field_value.find_all(
            'ul', class_='sgphx-tech-details__list')[0].p.text.replace('\n', ' ')
        watches_dict['bezel_color'].append(bezel_color)

        # field_25 = watches_dict['crystal']
        crystal = field_value.find_all(
            'ul', class_='sgphx-tech-details__list')[0].p.text.replace('\n', ' ')
        watches_dict['crystal'].append(crystal)

        # field_26 = watches_dict['water_resistance']
        '''
        In this snippet i target a (div) tag has a class named as (sgphx-rich-text)
        this class has a (ul) tag:
        <ul>
            <li> size: (value) </li>
            <li> water resistance: (value) </li>
        </ul>
        -------------
        Some times this (ul) has tow (li) some times has one, and i'm just targeting the value
        of water resistance.
        '''
        case_section = field_value.find_all(
            'div', class_='sgphx-rich-text')[1].ul.find_all('li')
        for ele in case_section:
            ele = ele.text.split(':')
            if ele[0] == 'Water Resistance':
                water_resistance = ele[-1][1:]
            else:
                water_resistance = ''
        watches_dict['water_resistance'].append(water_resistance)

        # field_27 = watches_dict['weight']
        weight = ''
        watches_dict['weight'].append(weight)

        # field_28 = watches_dict['dial_color']
        dial_color = field_value.find_all(
            'div', class_='sgphx-rich-text')[2].text.replace('\n', ' ')
        watches_dict['dial_color'].append(dial_color)

        # field_29 = watches_dict['numerals']
        numerals = field_value.find_all(
            'div', class_='sgphx-rich-text')[2].text.replace('\n', ' ')
        watches_dict['numerals'].append(numerals)

        # field_30 = watches_dict['bracelet_material']
        strap_type_info_lst = []
        bracelet_material = field_value.find_all(
            'div', class_='sgphx-rich-text')
        for find_li in bracelet_material:
            strap_type_info_lst.append(str(find_li.li))

        strap_type = strap_type_info_lst[3].split(
            '</li>')[0].split('<li>')[-1].split(':')[-1]
        watches_dict['bracelet_material'].append(strap_type)
        strap_type_info_lst.clear()

        # field_31 = watches_dict['bracelet_color']
        '''
        The problem i faced here that a view pages in the website have a different structure in 
        the (strap) section, so the length of (strap) section has a (div) with a class name (sgphx-rich-text).
        the length of the (div) look different from page to page, and with `if statement` i handled this
        issue to catch 'Color' values only.
        '''
        bracelet_color = field_value.find_all(
            'div', class_='sgphx-rich-text')[3].find_all('li')
        try:
            if len(bracelet_color) > 0:
                bracelet_color = field_value.find_all(
                    'div', class_='sgphx-rich-text')[3].find_all('li')
                for bracelet_color_value in bracelet_color:
                    bracelet_color = bracelet_color_value.text.split(':')
                    if bracelet_color[0] == 'Color':
                        bracelet_color = bracelet_color[-1][1:]
                    else:
                        bracelet_color = ''
            else:
                bracelet_color = ''
        except TypeError:
            bracelet_color = ''
        watches_dict['bracelet_color'].append(bracelet_color)

        # field_32 = watches_dict['clasp_type']
        try:
            clasp_type = field_value.find_all(
                'div', class_='sgphx-rich-text')[4].p.text
        except AttributeError:
            clasp_type = ''
        watches_dict['clasp_type'].append(clasp_type)

        # field_33 = watches_dict['movement']
        '''
        In this snippet i used try and except to handle changing of page structure form page to page
        '''
        try:
            movement = field_value.find_all(
                'div', class_='sgphx-rich-text')[6].ul.find_all('li')[0].text.split(':')[-1][1:]
        except AttributeError:
            try:
                movement = field_value.find_all(
                    'div', class_='sgphx-rich-text')[5].ul.find_all('li')[0].text.split(':')[-1][1:]
            except AttributeError:
                movement = ''
        watches_dict['movement'].append(movement)

        # field_34 = watches_dict['caliber']
        caliber = field_value.find_all(
            'h3', class_='sgphx-headings__subtitle sgphx-h4')[-1].text
        watches_dict['caliber'].append(caliber)

        # field_35 = watches_dict['power_reserve']
        '''
        in this snippet i face different structures from page to page
        <ul>
        <li>Energy: value</li>
        <li>Indications: value</li>
        <li>Power reserve: value</li>
        </ul>
        i'm targeting [power reserve] value, some pages have different numbers of <li> tag, and i have
        some values have Nonetype value, in this snippet i handle these problems.
        '''
        movement_Section = field_value.find_all(
            'div', class_='sgphx-rich-text')[6].ul
        if movement_Section is not None:
            movement_Section = field_value.find_all(
                'div', class_='sgphx-rich-text')[6].ul.find_all('li')
            for ele in movement_Section:
                ele = ele.text.split(':')
                if ele[0] == 'Power reserve':
                    power_reserve = ele[1][1:]
                else:
                    power_reserve = ''
        watches_dict['power_reserve'].append(power_reserve)

        # field_36 = watches_dict['frequency']
        '''
        in this snippet i face different structures from page to page
        <ul>
        <li>Number of pieces: value</li>
        <li>Number of rubis: value</li>
        <li>Diameter: value</li>
        <li>Thickness: value</li>
        <li>Frequency: value</li>
        </ul>
        i'm targeting [Frequency] value, some pages have different numbers of <li> tag, and i have
        some values have Nonetype value, in this snippet i handle these problems.
        '''
        movement_in_technical_section = field_value.find_all(
            'div', class_='sgphx-rich-text')[8].ul
        try:
            if movement_in_technical_section is not None:
                for ele in movement_in_technical_section:
                    ele = ele.text.split(':')
                    if ele[0] == 'Frequency':
                        frequency = ele[1][1:]
        except TypeError:
            frequency = ''
        watches_dict['frequency'].append(frequency)

        # field_37 = watches_dict['jewels']
        '''
        in this snippet i face different structures from page to page
        <ul>
        <li>Number of pieces: value</li>
        <li>Number of rubis: value</li>
        <li>Diameter: value</li>
        <li>Thickness: value</li>
        <li>Frequency: value</li>
        </ul>
        i'm targeting [Number of rubis] value, some pages have different numbers of <li> tag, and i have
        some values have Nonetype value, in this snippet i handle these problems.
        '''
        movement_in_technical_section = field_value.find_all(
            'div', class_='sgphx-rich-text')[8].ul
        try:
            if movement_in_technical_section is not None:
                for ele in movement_in_technical_section:
                    ele = ele.text.split(':')
                    if ele[0] == 'Number of rubis':
                        jewels = ele[1][1:]
                        # clean it to be an integer value
                        jewels = int(jewels)
        except TypeError:
            jewels = ''
        watches_dict['jewels'].append(jewels)

        # field_38 = watches_dict['features']
        top_paragraph_in_the_movement_section = field_value.find_all(
            'div', class_='sgphx-rich-text')[5].p
        if top_paragraph_in_the_movement_section is not None:
            try:
                features = top_paragraph_in_the_movement_section.text
            except TabError:
                features = ''
        watches_dict['features'].append(features)

        # field_39 = watches_dict['description']
        description = field_value.find_all('div', class_='sgphx-rich-text')[0].text.split(
            '\n')[1].replace('            ', 'cut_long_space').split('cut_long_space')[-1]
        watches_dict['description'].append(description)

        # field_40 = watches_dict['short_description']
        short_description = ''
        watches_dict['short_description'].append(short_description)


length_of_watches_dict_keys = {
    key: len(values) for key, values in watches_dict.items()}
# ------show the keys length------
print(length_of_watches_dict_keys)  # FOR TESTING THE LENGTH OF EACH KEY


def make_watch_dict_empty(dictionary):
    for key in dictionary:
        dictionary[key] = []


'''
        COMMENT THE NEXT LINE BEFORE EXECUTE ALL CELLS
########## THIS CELL IS FOR TESTING PURPOSES ONLY ##########
'''
# ------execute the function------
# make_watch_dict_empty(watches_dict) # THIS LINE FOR TESTING PURPOSES ONLY

# ==================== PANDAS SECTION =======================================
watch_dict_df = pd.DataFrame(watches_dict)
# set [reference_number] as id index
roger_dubuis_df = watch_dict_df.set_index('reference_number')
# to convert data i extracted to csv file
roger_dubuis_df.to_csv('roger_dubuis_dataset.csv', mode='w', encoding='utf-8-sig')
