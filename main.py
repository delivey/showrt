from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import xlsxwriter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os


# asks for user input
search_term = input("What TV-Series do you want ratings for? \n")
print(f"Searching for {search_term}")

path = os.getcwd()

# turns the website on and makes a search
driver = webdriver.Chrome(f'{path}\chromedriver.exe') 
driver.get("http://www.imdb.com")
make_search = driver.find_element_by_id("suggestion-search")
make_search.click()
make_search.send_keys(search_term)
make_search.send_keys(Keys.RETURN)

# clicks on the first search results
search_result = driver.find_element_by_class_name('primary_photo')
search_result.click()

"""current_url = driver.current_url
new_url = current_url.replace("?ref_=fn_al_tt_1", "episodes?ref_=tt_ov_epl")
driver.get(new_url)
season_element = driver.find_element_by_css_selector("#episode_top")
# season_element = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/h3")
season_number = int(season_element.get_attribute()) # /html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/h3
print(f"previous season: {season_number}")"""

def season_execute(season_number):
    # gets the current url, creates the new url, opening whatever season season_number is
    current_url = driver.current_url
    new_url = current_url.replace("?ref_=fn_al_tt_1", f"episodes?season={season_number}")
    # new_url = current_url.replace("?ref_=fn_al_tt_1", "episodes?ref_=ttep_ql_1")
    driver.get(new_url)

    # finds out how many episodes are in season 1
    element = driver.find_element_by_css_selector('meta[itemprop="numberofEpisodes"]')
    ep_number = int(element.get_attribute('content'))
    ep_list = list(range(1, ep_number + 1))

    # creates a default excel worksheet
    excel_file = xlsxwriter.Workbook(f'{path}\{search_term}.xlsx')
    worksheet = excel_file.add_worksheet()
    worksheet.write('A1', 'Episode')
    worksheet.write('B1', 'Rating')
    print("Excel file created")

    # creates a list of episodes in excel
    for idx, month in enumerate(ep_list):
        worksheet.write(idx + 1, 0, ep_list[idx])

    # gets the rating for each episode and assigns it in excel
    for num in ep_list:
        rating = driver.find_elements_by_css_selector('span[class="ipl-rating-star__rating"]')
        rating_list = []
        for i in rating:
            rating_txt = i.get_attribute('innerHTML')
            if '.' in rating_txt:
                rating_list.append(rating_txt)

    float_list = list(np.float_(rating_list))
            
    for idx, month in enumerate(ep_list):
        worksheet.write(idx + 1, 1, float_list[idx])
    print("Excel file filled")

    excel_file.close()

    lowest_num = min(float_list)
    max_num = max(float_list)
    lowest_rounded = int(round(lowest_num))
    real_low = lowest_rounded
    if lowest_rounded > lowest_num:
        real_low += lowest_rounded-1

    # creates the line chart
    df = pd.read_excel(f'{path}\{search_term}.xlsx')
    default_plot = df.plot(x='Episode', y='Rating', kind='line', color='red', ylim=(real_low, max_num))
    default_plot.xaxis.set_major_locator(MaxNLocator(integer=True))
    default_plot.set_title(f'Each {search_term} Episode Rating')
    default_plot.set_ylabel('Rating')

    # saves the line chart
    plt.savefig(f'{path}\{search_term}_{season_number}_chart.png', dpi=300)
    print("Chart saved")

season_execute(1)
