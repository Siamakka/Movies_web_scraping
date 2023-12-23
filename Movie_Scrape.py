from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
import pandas as pd
import time
import numpy as np

start_time = time.perf_counter()

df_movie_names = pd.read_excel("Movie_names.xlsx")
foreign_movie_names = df_movie_names['foreign_movie_name'].tolist()

# Create empty lists to store data for each item
imdb_search_link = []
imdb_movie_link = []
imdb_search_movie_name = []
sheet_movie_name = []
imdb_movie_year = []
name_diff = []
imdb_id = []
imdb_rating = []
imdb_length = []
imdb_about = []
imdb_mpaa = []
imdb_kind = []
imdb_genre1 = []
imdb_genre2 = []
imdb_genre3 = []
imdb_writers = []
imdb_directors = []
imdb_star1 = []
imdb_star1_role = []
imdb_star2 = []
imdb_star2_role = []
imdb_star3 = []
imdb_star3_role = []
imdb_poster = []
star1_search_url = []
star2_search_url = []
star3_search_url = []
imdb_star1_profile = []
imdb_star2_profile = []
imdb_star3_profile = []


for movie in foreign_movie_names[:10]:

    # Create IMDB search link. movies with no str names, get error in try and use except.
    try:
        movie_original_name = movie.replace(' ', '%20')
    except:
        movie_original_name = str(movie)
    search_link = 'https://www.imdb.com/find/?q=' + movie_original_name + '&s=tt&exact=true&ref_=fn_tt_ex'
    imdb_search_link.append(search_link)


    request = requests.get(search_link, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(request.content, 'html.parser')
    
    sheet_movie_name.append(movie)

    # find movie names
    try:
        movie_link = soup.find('a', class_='ipc-metadata-list-summary-item__t')
        movie_link_text = 'https://www.imdb.com' + movie_link.get_attribute_list('href')[0]
        imdb_movie_link.append(movie_link_text)
    except:
        imdb_movie_link.append('Movie link not found!')

    # find IMDB ID
    try:
        id = movie_link.get_attribute_list('href')[0]
        movie_ids = id[7:16]
        imdb_id.append(movie_ids)
    except:
        imdb_id.append('Movie ID not found!')

    # find movie name
    try:
        movie_name = soup.findChild('div', class_='ipc-metadata-list-summary-item__tc')
        movie_name_text = [n.text for n in movie_name]
        movie_name = movie_name_text[0]
        imdb_search_movie_name.append(movie_name)
    except:
        imdb_search_movie_name.append('IMDB Search link not found!')

    # find if name of the movie is equal to name in the sheet or not
    if str(movie).lower() == str(movie_name).lower():
        name_diff.append('True')
    else:
        name_diff.append('False')


for movie in imdb_movie_link:
    request = requests.get(movie, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(request.content, 'html.parser')

    # find IMDB ratting
    try:
        rating_label = soup.find('span', class_= 'sc-bde20123-1 cMEQkK')
        rating_text = [ra.text for ra in rating_label]
        rating_text = ' '.join([str(elm) for elm in rating_text])
        imdb_rating.append(rating_text)
    except:
        imdb_rating.append('IMDB rating not found!')

    # find movie length
    try:
        length_label = soup.findChild('ul', class_= 'ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt')
        length_text = [l.text for l in length_label]
        length_text = length_text[-1]
        length_split = length_text.split(' ')
        # convert '*h *m' to minutes
        try:
            length_minutes = (int(length_split[0].replace('h', '')) * 60) + int(length_split[1].replace('m', ''))
        except:
            length_minutes = int(length_split[0].replace('m', ''))
        imdb_length.append(length_minutes)
    except:
        imdb_length.append('Movie length not found!')

    # find plot
    try:
        about_label = soup.find_all('span', class_='sc-466bb6c-1 dWufeH')
        about_text = [ab.text for ab in about_label]
        about_text = ' '.join([str(elm1) for elm1 in about_text])
        imdb_about.append(about_text)
    except:
        imdb_about.append('Movie Plot not found!')

    # find mpaa
    try:
        mpaa_label = soup.findChild('ul', class_= 'ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt')
        mpaa_text = [mp.text for mp in mpaa_label]
        mpaa_text = mpaa_text[-2]
        imdb_mpaa.append(mpaa_text)
    except:
        imdb_mpaa.append('MPAA not found!')

    # find movie year
    try:
        movie_year_label = soup.findChild('ul', class_= 'ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt')
        movie_year_text = [y.text for y in movie_year_label]
        movie_year_text = movie_year_text[-3]
        imdb_movie_year.append(movie_year_text)
    except:
        imdb_movie_year.append('Movie year not found!')

    # movie or tv-series?
    try:
        kind_label = soup.findChild('ul', class_= 'ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt')
        kind_text = [k.text for k in kind_label]
        try:
            kind_text = kind_text[-4]
            imdb_kind.append(kind_text)
        except:
            imdb_kind.append('Movie')
    except:
        imdb_kind.append('Movie/Series kind not found!')

    # find genre1
    try:
        genre1_label = soup.find_all('span', 'ipc-chip__text')
        genre1_text = [ge1.text for ge1 in genre1_label]
        imdb_genre1.append(genre1_text[0])
    except:
        imdb_genre1.append('IMDB genre1 not found!')

    # find genre2
    try:
        genre2_label = soup.find_all('span', 'ipc-chip__text')
        genre2_text = [ge2.text for ge2 in genre2_label]
        if genre2_text[1] == 'Back to top':
            imdb_genre2.append('IMDB genre2 not found')
        else:
            imdb_genre2.append(genre2_text[1])
    except:
        imdb_genre2.append('IMDB genre2 not found!')

    # find genre3
    try:
        genre3_label = soup.find_all('span', 'ipc-chip__text')
        genre3_text = [ge3.text for ge3 in genre3_label]
        if genre3_text[2] == 'Back to top':
            imdb_genre3.append('IMDB Genre3 not found')
        else:
            imdb_genre3.append(genre3_text[2])
    except:
        imdb_genre3.append('IMDB genre3 not found!')

    # find writer of writers
    try:
        try:
            writers_label = (soup.find(string='Writers').parent)
            writers_elts = writers_label.next_sibling.find('li')
            writers = [w.text for w in writers_elts]
            writers = ' '.join([str(elm3) for elm3 in writers])
            imdb_writers.append(writers)
        except:
            writers_label = (soup.find(string='Writer').parent)
            writers_elts = writers_label.next_sibling.find('li')
            writers = [w.text for w in writers_elts]
            writers = ' '.join([str(elm3) for elm3 in writers])
            imdb_writers.append(writers)
    except:
        imdb_writers.append('Writers not found!')

    # find director or directors
    try:
        try:
            director_label = (soup.find(string='Director').parent)
            director_elts = director_label.next_sibling.find_all('li')
            directors = [d.text for d in director_elts]
            directors = ' '.join([str(elm2) for elm2 in directors])
            imdb_directors.append(directors)
        except:
            director_label = (soup.find(string='Directors').parent)
            director_elts = director_label.next_sibling.find_all('li')
            directors = [d.text for d in director_elts]
            directors = ' '.join([str(elm2) for elm2 in directors])
            imdb_directors.append(directors)
    except:
        imdb_directors.append('Directors not found!')

    # find star1
    try:
        star1_label = (soup.find(string='Stars').parent)
        star1_elts = star1_label.next_sibling.find_all('li')
        stars = [s1.text for s1 in star1_elts]
        imdb_star1.append(stars[0])
    except:
        imdb_star1.append('Star1 not found!')

    # create star1 search url
    try:
        star1_search = stars[0].replace(' ', '%20')
        star1_imdb_search = 'https://www.imdb.com/find/?q=' + star1_search + '&s=nm&exact=true&ref_=fn_nm_ex'
        star1_search_url.append(star1_imdb_search)
    except:
        star1_search_url.append('Star1 search link not found!')

    # find star2
    try:
        star2_label = (soup.find(string='Stars').parent)
        star2_elts = star1_label.next_sibling.find_all('li')
        stars = [s2.text for s2 in star2_elts]
        imdb_star2.append(stars[1])
    except:
        imdb_star2.append('Star2 not found!')

    # create star2 search url
    try:
        star2_search = stars[1].replace(' ', '%20')
        star2_imdb_search = 'https://www.imdb.com/find/?q=' + star2_search + '&s=nm&exact=true&ref_=fn_nm_ex'
        star2_search_url.append(star2_imdb_search)
    except:
        star2_search_url.append('Star2 search link not found!')

    # find star3
    try:
        star3_label = (soup.find(string='Stars').parent)
        star3_elts = star3_label.next_sibling.find_all('li')
        stars = [s3.text for s3 in star3_elts]
        imdb_star3.append(stars[2])
    except:
        imdb_star3.append('Star3 not found!')

    # create star3 search url
    try:
        star3_search = stars[2].replace(' ', '%20')
        star3_imdb_search = 'https://www.imdb.com/find/?q=' + star3_search + '&s=nm&exact=true&ref_=fn_nm_ex'
        star3_search_url.append(star3_imdb_search)
    except:
        star3_search_url.append('Star3 search link not found!')

    # find star1 role
    try:
        star1_role_label = soup.find_all('span', class_='sc-bfec09a1-4 kvTUwN')
        star1_role_text = [r1.text for r1 in star1_role_label]
        imdb_star1_role.append(star1_role_text[0])
    except:
        imdb_star1_role.append('Star1 role not found!')

    # find star2 role
    try:
        star2_role_label = soup.find_all('span', class_='sc-bfec09a1-4 kvTUwN')
        star2_role_text = [r2.text for r2 in star2_role_label]
        imdb_star2_role.append(star2_role_text[1])
    except:
        imdb_star2_role.append('Star2 role not found!')

    # find star3 role
    try:
        star3_role_label = soup.find_all('span', class_='sc-bfec09a1-4 kvTUwN')
        star3_role_text = [r3.text for r3 in star3_role_label]
        imdb_star3_role.append(star3_role_text[2])
    except:
        imdb_star3_role.append('Star3 role not found!')

    # find cover url
    try:
        poster_link = soup.find('img', class_='ipc-image')
        poster_link_text = poster_link.get_attribute_list('src')
        poster_link_text = ' '.join([str(elm4) for elm4 in poster_link_text])
        poster_link_text = poster_link_text[:-30] + 'jpg'
        imdb_poster.append(poster_link_text)
    except:
        imdb_poster.append('IMDB poster link not found!')

# find img src for star1 avatar
for star in star1_search_url:
    request = requests.get(star, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(request.content, 'html.parser')

    try:
        profile_pic_link = soup.find('img', class_='ipc-image')
        profile_pic_text = profile_pic_link.get_attribute_list('src')
        profile_pic_text = ' '.join([str(elm5) for elm5 in profile_pic_text])
        profile_pic_text = profile_pic_text[:-30] + 'jpg'
        imdb_star1_profile.append(profile_pic_text)
    except:
        imdb_star1_profile.append('Star1 Profile pic link not found!')

# find img src for star2 avatar
for star in star2_search_url:
    request = requests.get(star, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(request.content, 'html.parser')

    try:
        profile_pic_link = soup.find('img', class_='ipc-image')
        profile_pic_text = profile_pic_link.get_attribute_list('src')
        profile_pic_text = ' '.join([str(elm6) for elm6 in profile_pic_text])
        profile_pic_text = profile_pic_text[:-30] + 'jpg'
        imdb_star2_profile.append(profile_pic_text)
    except:
        imdb_star2_profile.append('Star2 Profile pic link not found!')

# find img src for star3 avatar
for star in star3_search_url:
    request = requests.get(star, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(request.content, 'html.parser')

    try:
        profile_pic_link = soup.find('img', class_='ipc-image')
        profile_pic_text = profile_pic_link.get_attribute_list('src')
        profile_pic_text = ' '.join([str(elm6) for elm6 in profile_pic_text])
        profile_pic_text = profile_pic_text[:-30] + 'jpg'
        imdb_star3_profile.append(profile_pic_text)
    except:
        imdb_star3_profile.append('Star3 Profile pic link not found!')

#create dataframe and save the file
dataframe = pd.DataFrame({
    'movie/series': pd.Series(imdb_kind),
    'Sheet_movie_name' : pd.Series(sheet_movie_name),
    'Movie_name': pd.Series(imdb_search_movie_name),
    'diff_to_dataset_name': pd.Series(name_diff),
    'imdb_search_link': pd.Series(imdb_search_link),
    'imdb_movie_link': pd.Series(imdb_movie_link),
    'imdb_movie_id': pd.Series(imdb_id),
    'year': pd.Series(imdb_movie_year),
    'imdb_rating': pd.Series(imdb_rating),
    'duration': pd.Series(imdb_length),
    'imdb_plot': pd.Series(imdb_about),
    'imdb_mpaa': pd.Series(imdb_mpaa),
    'imdb_genre1': pd.Series(imdb_genre1),
    'imdb_genre2': pd.Series(imdb_genre2),
    'imdb_genre3': pd.Series(imdb_genre3),
    'writers': pd.Series(imdb_writers),
    'directors': pd.Series(imdb_directors),
    'star1': pd.Series(imdb_star1),
    'star1_profile_search': pd.Series(star1_search_url),
    'star1_profile_pic_url': pd.Series(imdb_star1_profile),
    'star1_role': pd.Series(imdb_star1_role),
    'star2': pd.Series(imdb_star2),
    'star2_profile_search': pd.Series(star2_search_url),
    'star2_profile_pic_url': pd.Series(imdb_star2_profile),
    'star2_role': pd.Series(imdb_star2_role),
    'star3': pd.Series(imdb_star3),
    'star3_profile_search': pd.Series(star3_search_url),
    'star3_profile_pic_url': pd.Series(imdb_star3_profile),
    'star3_role': pd.Series(imdb_star3_role),
    'imdb_movie_poster_url': pd.Series(imdb_poster),
})
dataframe.to_csv('Movie_data.csv')

# download cover files
for url,id in zip(imdb_poster, imdb_id):
    try:
        response = requests.get(url)
        if response.status_code:
            fp = open(id + '.jpg', 'wb')
            fp.write(response.content)
            fp.close()
    except:
        continue

# download star1 avatars
for url,name in zip(imdb_star1_profile, imdb_star1):
    try:
        response = requests.get(url)
        if response.status_code:
            fp = open(name + '.jpg', 'wb')
            fp.write(response.content)
            fp.close()
    except:
        continue

# download star2 avatars
for url,name in zip(imdb_star2_profile, imdb_star2):
    try:
        response = requests.get(url)
        if response.status_code:
            fp = open(name + '.jpg', 'wb')
            fp.write(response.content)
            fp.close()
    except:
        continue

#download star3 avatars
for url,name in zip(imdb_star3_profile, imdb_star3):
    try:
        response = requests.get(url)
        if response.status_code:
            fp = open(name + '.jpg', 'wb')
            fp.write(response.content)
            fp.close()
    except:
        continue

# get Farsi movie names
df_movie_names = pd.read_excel("Movie_names.xlsx")
farsi_movie_names = df_movie_names['farsi_movie_name'].tolist()
filimo_search_link = []
farsi_sheet_movie_name = []

# create movie search links for filimo.com
for movie in farsi_movie_names[:10]:
    farsi_sheet_movie_name.append(movie)
    try:
        farsi_name = movie.replace(' ', '%20')
    except:
        farsi_name = str(movie)

    search_link = 'https://www.filimo.com/search/' + farsi_name
    filimo_search_link.append(search_link)

# setup webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.page_load_strategy = "none"
chrome_binary = 'D:\Zartosht\Meta Data\IMDB\Binaries2\chrome.exe'
options = webdriver.ChromeOptions()
options.binary_location = chrome_binary
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options= options)

# create empty lists to store data
movie_url_list = []
movie_name_list = []
director_list = []
genre1_list = []
genre2_list = []
plot_list = []
star1_list = []
star2_list = []
star3_list = []
producer_list = []
writer_list = []
star1_pic_list = []
star2_pic_list = []
star3_pic_list = []


for link in filimo_search_link[:50]:
    # open every search urls
    driver.get(link)

    # find movie url
    try:
        movie_profile = driver.find_element(By.CSS_SELECTOR, "div[class*='movie-description'")
        movie_profile.click()
        movie_url = driver.current_url
        movie_url_list.append(movie_url)
    except:
        movie_url_list.append('Movie URL not found')

    # find movie name
    try:
        movie_name = driver.find_element(By.CSS_SELECTOR, "span[class*='d-inline-flex'")
        movie_name = movie_name.text
        movie_name_list.append(movie_name)
    except:
        movie_name_list.append('Movie name not found')

    # use bs4
    request = requests.get(movie_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(request.content, 'html.parser')

    # find director
    try:
        director_title = soup.find_all('th', class_='ui-fw-normal')
        director_text = director_title[1].text
        director_list.append(director_text)
    except:
        director_list.append('Director not found')

    # find genre1 and 2
    try:
        genre1_title = soup.find_all('a', class_='ui-btn ui-btn-force-dark ui-btn-small ui-btn ui-br-24 ui-pr-2x ui-pl-2x ui-pt-x ui-pb-x ui-bg-gray-20 details_poster-description-meta-link <?php echo e($innerClass); ?>')
        genre1_text = genre1_title[0].text
        genre1_list.append(genre1_text)
    except:
        genre1_list.append('Genre1 not found')

    try:
        genre2_title = soup.find_all('a', class_='ui-btn ui-btn-force-dark ui-btn-small ui-btn ui-br-24 ui-pr-2x ui-pl-2x ui-pt-x ui-pb-x ui-bg-gray-20 details_poster-description-meta-link <?php echo e($innerClass); ?>')
        genre2_text = genre2_title[1].text
        genre2_list.append(genre2_text)
    except:
        genre2_list.append('Genre2 not found')

    # find plot
    try:
        plot_title = soup.find('p', class_= 'toTruncate ps-relative short-description')
        plot_text = plot_title.text
        plot_list.append(plot_text)
    except:
        plot_list.append('Plot not found')

    # find stars names
    try:
        star1 = soup.find_all('strong', class_= 'ui-fw-normal')
        star1_text = [s.text for s in star1]
        star1_list.append(star1_text[0])
        star2_list.append(star1_text[1])
        star3_list.append(star1_text[2])
    except:
        star1_list.append('Star1 not found')
        star2_list.append('Star2 not found')
        star3_list.append('Star3 not found')

    # find producer and writer
    try:
        crew = soup.find_all('a', class_= 'crew-name')
        crew_text = [c.text for c in crew]
        producer_list.append(crew_text[1])
        writer_list.append(crew_text[2])
    except:
        producer_list.append('Producer not found')
        writer_list.append('Writer not found')

    # find stars avatars url
    try:
        star_pic = soup.find_all('img', class_= 'actor-avatar')
        star_pic = [pic.get_attribute_list('src') for pic in star_pic]
        star1_pic = str(star_pic[0])[2:-53]
        star1_pic_list.append(star1_pic)
        star2_pic = str(star_pic[1])[2:-53]
        star2_pic_list.append(star2_pic)
        star3_pic = str(star_pic[2])[2:-53]
        star3_pic_list.append(star3_pic)
    except:
        star1_pic_list.append('Star1 pic url not found')
        star2_pic_list.append('Star2 pic url not found')
        star3_pic_list.append('Star3 pic url not found')

# create dataframe
farsi_dataframe = pd.DataFrame({
    'movie_sheet_name': pd.Series(farsi_sheet_movie_name),
    'movie_name': pd.Series(movie_name_list),
    'movie_url': pd.Series(movie_url_list),
    'director': pd.Series(director_list),
    'producer': pd.Series(producer_list),
    'writer': pd.Series(writer_list),
    'genre1': pd.Series(genre1_list),
    'genre2': pd.Series(genre2_list),
    'plot': pd.Series(plot_list),
    'star1': pd.Series(star1_list),
    'star2': pd.Series(star2_list),
    'star3': pd.Series(star3_list),
    'star1 avatar url': pd.Series(star1_pic_list),
    'star2 avatar url': pd.Series(star2_pic_list),
    'star3 avatar url': pd.Series(star3_pic_list)
})
farsi_dataframe.to_csv('Farsi_movie_data.csv', encoding='utf-8-sig')

# download avatars files
for url,name in zip(star1_pic_list, star1_list):
    try:
        response = requests.get(url)
        if response.status_code:
            fp = open(name + '.jpg', 'wb')
            fp.write(response.content)
            fp.close()
    except:
        continue

for url,name in zip(star2_pic_list, star2_list):
    try:
        response = requests.get(url)
        if response.status_code:
            fp = open(name + '.jpg', 'wb')
            fp.write(response.content)
            fp.close()
    except:
        continue

for url,name in zip(star3_pic_list, star3_list):
    try:
        response = requests.get(url)
        if response.status_code:
            fp = open(name + '.jpg', 'wb')
            fp.write(response.content)
            fp.close()
    except:
        continue

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(elapsed_time)