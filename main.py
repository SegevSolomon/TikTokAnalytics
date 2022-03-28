import gspread
from datetime import datetime
from bs4 import BeautifulSoup
from functions import convert_number
from functions import check_date
from functions import video_array
from functions import view_array
from functions import check_if_tiktok_url
from functions import check_if_private_account
from functions import get_tiktok_followers
from functions import check_if_video_load
from functions import get_publish_date
from functions import check_if_username_correct
from functions import human_format
from TikTokApi import TikTokApi
from selenium import webdriver
import time

gc = gspread.service_account(filename='creds.json')
sh = gc.open_by_key('XXXkeyXXX')
sheet = sh.sheet1

# Getting data from the sheet
data = sheet.get_all_records()
print(data)
col = sheet.col_values(1)

for counter in range(1, len(col)):
    tiktok_account_name = col[counter]
    tiktok_account_link = "https://www.tiktok.com/@" + tiktok_account_name
    if check_if_tiktok_url(tiktok_account_link):
        # Define selenium
        PATH = 'D:\selenium webdriver\chromedriver.exe'
        driver = webdriver.Chrome(PATH)

        # open selenium
        driver.get(tiktok_account_link)
        driver.maximize_window()

        # get the source page of the tiktok account
        html = driver.page_source

        api = TikTokApi(custom_verify_fp="")
        data = api.user(username=tiktok_account_name).info_full()

        # check if the username is correct
        if check_if_username_correct(data):
            sheet.update_cell(counter + 1, 2, "Not Found")
            sheet.update_cell(counter + 1, 3, "Not Found")
            sheet.update_cell(counter + 1, 4, "Not Found")
            sheet.update_cell(counter + 1, 5, "Not Found")
            sheet.update_cell(counter + 1, 6, "Not Found")
            sheet.update_cell(counter + 1, 7, "Not Found")
            today = datetime.now()
            date = str(today.strftime("%d/%m/%Y %H:%M:%S"))
            sheet.update_cell(counter + 1, 8, date)
        else:
            # check if the account is private
            if check_if_private_account(html, data):
                sheet.update_cell(counter + 1, 2, "Private Account")
                sheet.update_cell(counter + 1, 3, "Private Account")
                sheet.update_cell(counter + 1, 4, "Private Account")
                sheet.update_cell(counter + 1, 5, "Private Account")
                sheet.update_cell(counter + 1, 6, "Private Account")
                sheet.update_cell(counter + 1, 7, "Private Account")
                today = datetime.now()
                date = str(today.strftime("%d/%m/%Y %H:%M:%S"))
                sheet.update_cell(counter + 1, 8, date)

            # if the account is not private continue to "else"
            else:
                # get full html page with all the videos - infinity roll
                previous_height = driver.execute_script('return document.body.scrollHeight')
                while True:
                    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    time.sleep(1)
                    new_height = driver.execute_script('return document.body.scrollHeight')
                    if new_height == previous_height:
                        break

                    previous_height = new_height
                    print("scroll")


                html = driver.page_source
                # convert the source page from Selenium to BeautifulSoup
                soup = BeautifulSoup(html, "html.parser")

                # get the tiktok username
                #tiktok_username = get_tiktok_username(soup)
                # get the tiktok followers
                tiktok_followers = get_tiktok_followers(data)

                # get the views counter from every video
                views = soup.find_all(class_="video-count tiktok-1p23b18-StrongVideoCount eor0hs42")
                viewsArray = view_array(views)

                # get all the video links of the tiktok account
                videos = soup.find_all(class_="tiktok-yz6ijl-DivWrapper e1u9v4ua1")
                videosArray = video_array(videos)


                # create a int for save the total likes, comments, shares and relevent videos
                totalLikes = 0
                totalComments = 0
                totalShare = 0
                totalViews = 0
                releventVideo = 0
                for index in range(len(videosArray)):
                    # load selenium
                    driver.get(videosArray[index])
                    driver.maximize_window()

                    # get the source page
                    html = driver.page_source

                    # check if the video load
                    if check_if_video_load(html):
                        print("video don't work!")
                    # if the video load continue to "else"
                    else:
                        soup = BeautifulSoup(html, "html.parser")
                        # get the publish date of the video
                        publishDate = get_publish_date(soup)
                        print(publishDate)
                        if check_date(publishDate):
                            # get the likes, comments and shares buttons
                            buttons = soup.find_all(class_="tiktok-1xiuanb-ButtonActionItem e1bs7gq20")
                            # check if there is a 3 buttons
                            if len(buttons) == 3:
                                likes = buttons[0]
                                comments = buttons[1]
                                shares = buttons[2]

                                likes = str(likes)
                                comments = str(comments)
                                shares = str(shares)

                                # split the buttons and the text
                                likes = likes.split("<strong")[1].split('">')[1].split('</strong')[0]
                                comments = comments.split("<strong")[1].split('">')[1].split('</strong')[0]
                                shares = shares.split("<strong")[1].split('">')[1].split('</strong')[0]

                                # check if there any share for the video
                                if shares == "Share" or shares == "שתף":
                                    shares = 0
                                else:
                                    shares = convert_number(shares)

                                # add number for the total likes, comments and shares
                                totalLikes += convert_number(likes)
                                totalComments += convert_number(comments)
                                totalShare += shares
                                totalViews += viewsArray[index]

                                releventVideo += 1

                            # if not pass about this video
                            else:
                                pass
                        else:
                            break
                if releventVideo == 0:
                    tiktok_average_views = 0
                    average_likes = 0
                    average_comments = 0
                    average_shares = 0
                    tiktok_engagement = 0
                else:
                    tiktok_average_views = totalViews / releventVideo
                    average_likes = totalLikes / releventVideo
                    average_comments = totalComments / releventVideo
                    average_shares = totalShare / releventVideo
                    tiktok_engagement = (totalLikes + totalComments + totalShare) / totalViews * 100

                sheet.update_cell(counter+1, 2, tiktok_followers)
                sheet.update_cell(counter+1, 3, human_format(tiktok_average_views))
                sheet.update_cell(counter+1, 4, human_format(average_likes))
                sheet.update_cell(counter+1, 5, human_format(average_comments))
                sheet.update_cell(counter+1, 6, human_format(average_shares))
                sheet.update_cell(counter+1, 7, str("{:.1f}".format(tiktok_engagement)) + "%")
                today = datetime.now()
                date = str(today.strftime("%d/%m/%Y %H:%M:%S"))
                sheet.update_cell(counter + 1, 8, date)
                print("ACCOUNT " + tiktok_account_name)
                print("FOLLOWERS " + tiktok_followers)
                print("Average Views " + str(tiktok_average_views))
                print("Average Likes " + str(average_likes))
                print("Average Comments " + str(average_comments))
                print("Average Shares " + str(average_shares))
                print("Engagement " + str(tiktok_engagement))
                print(len(videosArray))
                print(releventVideo)
    else:
        pass