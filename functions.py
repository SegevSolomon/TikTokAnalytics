import datetime

def convert_number(num):
    if 'K' in num:
        num = float(num.replace('K', '')) * 1000
    elif 'M' in num:
        num = float(num.replace('M', '')) * 1000000
    elif 'B' in num:
        num = float(num.replace('B', '')) * 1000000000
    else:
        num = float(num)
    return num

def check_if_tiktok_url(url):
    if "https://" in url:
        if "tiktok.com" in url:
            return True
        else:
            return False
    else:
        return False

def check_date(date):
    today = datetime.datetime.now()
    count = date.count("-")
    if count == 0:
        return True
    elif count == 1:
        splitDate = date.split("-")
        datetimeObject = datetime.datetime(int(today.year), int(splitDate[0]), int(splitDate[1]))
    elif count == 2:
        splitDate = date.split("-")
        datetimeObject = datetime.datetime(int(splitDate[0]), int(splitDate[1]), int(splitDate[2]))

    differenceDate = today - datetimeObject

    if differenceDate.days <= 30:
        return True
    else:
        return False

def video_array(videos):
    videosLinkArray = []
    for video in videos:
        link = str(video).split('<a href="')[1].split('">')[0]
        videosLinkArray.append(link)

    return videosLinkArray

def view_array(views):
    viewsArray = []
    for view in views:
        numberViews = view.text
        newNumber = convert_number(numberViews)
        viewsArray.append(newNumber)

    return viewsArray

def check_if_private_account(html, data):
    print(data)
    private_account = data['user']['privateAccount']
    print(private_account)
    if "tiktok-1tttox1-DivErrorContainer emuynwa0" in html or private_account == True:
        return True
    else:
        return False

#def get_tiktok_username(soup):
    #tiktok_username = soup.find(class_="tiktok-u0kg0z-DivShareTitleContainer e198b7gd3")
    #tiktok_username = str(tiktok_username)
    #tiktok_username = tiktok_username.split('h2')[1].split('>')[1].split('</h2>')[0].split('<')[0]
    #return tiktok_username

def get_tiktok_followers(data):
    print(data)
    tiktok_followers = data['stats']['followerCount']
    print(tiktok_followers)
    tiktok_followers = human_format(tiktok_followers)
    return tiktok_followers

def check_if_video_load(html):
    if "tiktok-1osbocj-DivErrorContainer emuynwa0" in html:
        return True
    else:
        return False

def get_publish_date(soup):
    # get the publish date of the video
    publishDate = soup.find(class_="tiktok-12dba99-StyledAuthorAnchor e10yw27c1")
    publishDate = str(publishDate)
    publishDate = publishDate.split('</span>')[1].split('</')[0]
    print(publishDate)
    return publishDate

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.1f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

def check_if_username_correct(data):
    json_string = str(data)
    print(json_string)
    if json_string == "{}":
        return True
    else:
        return False