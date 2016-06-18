source = "3182990075"
access_token = "2.00orEdqCbHV6TDfe7c3ed211P_oIRB",


from urllib2 import Request, urlopen, URLError
request = Request('http://weibo.com/1098618600/DrIJEdVVm?ref=home&rid=0_0_0_2666930805480913525&type=comment')

try:
    response = urlopen(request)
    tri = response.read()
    print tri
except URLError, e:
    print 'No text. Got an error code:', e
# The above will return the HTML code.
   
#############################################################
import requests
url = 'http://ES_search_demo.com/document/record/_search?pretty=true'
data = '{"query":{"bool":{"must":[{"text":{"record.document":"SOME_JOURNAL"}},{"text":{"record.articleTitle":"farmers"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}'
response = requests.get(url, data=data)


import requests
from requests.auth import HTTPDigestAuth
import json


# Replace with the correct URL
url = "http://api_url"

# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
myResponse = requests.get(url,auth=HTTPDigestAuth(raw_input("username: "), raw_input("Password: ")), verify=True)
#print (myResponse.status_code)

# For successful API call, response code will be 200 (OK)
if(myResponse.ok):

    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    jData = json.loads(myResponse.content)

    print("The response contains {0} properties".format(len(jData)))
    print("\n")
    for key in jData:
        print key + " : " + jData[key]
else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()

##########################################################

import urllib, urllib2
the_url = 'https://api.weibo.com/2/suggestions/users/hot.json?client_id=3182990075&access_token=2.00orEdqCbHV6TDfe7c3ed211P_oIRB&category=DEFAULT'
http_body = None

# 发送请求并读取返回 返回的内容是真个html源代码，或者json数据，可以通过文件输出或者包一层repr()来查看内容
req = urllib2.Request(the_url, data=http_body)

#当然也可以用此来发送请求，并读取返回的内容是真个html源代码，可以通过文件输出或者包一层repr()来查看内容
#req = urllib2.Request("http://www.baidu.com", data=http_body)

resp = urllib2.urlopen(req)
print repr(resp.read())

##########################################################
# https://github.com/michaelliao/sinaweibopy/blob/master/README.md
from weibo import APIClient
import webbrowser
APP_KEY = '3182990075'
APP_SECRET = 'cf1f746ac349daae676c4d583587b508'
CALLBACK_URL = 'https://github.com/azzurraying'
client = APIClient(app_key = APP_KEY,
                  app_secret = APP_SECRET,
                  redirect_uri = CALLBACK_URL)
url = client.get_authorize_url()
webbrowser.open_new(url)
# Web browser opens. Copy the last 32 digits: that's the code.

code = 'd2722c31d1f60d508330ce29d7aa8bf7' # as an e.g.
r = client.request_access_token(code)
access_token1 = r.access_token # e.g. '2.00orEdqCbHV6TDfe7c3ed211P_oIRB'
expires_in = r.expires_in # e.g. '157679999'

########
# This part uses the weibo.py module to get actual API. But it doesn't seem to allow that much control.
# I prefer using 'urllib' and 'request'
c =  client.statuses.user_timeline.get(uid = 2609948640)
for st in c.statuses:
    print st.text
########

########
import urllib2
from urllib2 import Request, urlopen, URLError
import json

the_url = 'https://api.weibo.com/2/suggestions/users/hot.json?client_id=3182990075&access_token=2.00orEdqCbHV6TDfe7c3ed211P_oIRB&category=DEFAULT'

j = json.load(urllib2.urlopen(the_url))
# All API texts become a list of lists! (JSON)

j1 = json.load(urllib2.urlopen(Request(the_url)), )

j2 = json.dumps(tri, encoding="utf-8", ensure_ascii = False)

j3 = response.json()
########

########
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
########

import requests
r = requests.get(the_url)

j = r.json()
j[0].values()[0]
# Gets all data into a json.

print j[0].values() # Prints unintelligible unicode.
for i in j[0].values():
    print i
# This prints out all the normal, Chinese texts.

for i in j[0].values()[0].values():
    print i
# This prints out the POST information. (the rest of j[0] contains user info, which we don't need)


# request = Request(the_url)
# response = urlopen(request)
# r2 = response.read()
# # Gets all the texts in the API call as 1 gigantic string!

# word = '孙坚'
# word.find('孙') # 0
# word.find('坚') # 1
# word1 = u'孙坚'

# counter = 0
# for i in word2:
#     if '吃' in i:
#     # Or:
#     # if i.find('吃') >= 0:
#         counter += 1
#######################################################


import urllib2
from urllib2 import Request, urlopen, URLError
import json
import requests

#########
# Trial #
#########
url = 'https://api.weibo.com/2/statuses/friends_timeline.json?access_token=2.00orEdqCbHV6TDfe7c3ed211P_oIRB&count=100&page=1'

r = requests.get(the_url)
j = r.json()

for i in j.keys():
    print i
# advertises (empty list)
# interval
# hasvisible
# ad (empty list)
# total_number
# uve_blank
# previous_cursor
# has_unread
# since_id
# next_cursor
# max_id
# statuses (contains all the information. A list of 100 dicts)
len(j.values()[11]) # 100
len(j.keys()[11][0]) # 1
j.keys()[11] # u'statuses'. This key has multiple values - all the information there is to the posts and users.
len(j.values()[11][0]) # 33

for i in j.values()[11][0].items():
    print i # A tuple of Post#0 information (key and value)
    print i[1] # Post#0 contents (created_at, post id, reposts_count, comment_count, user info)

j.values()[11][1].items() # Post#1
j.values()[11][2].items() # Post#2
j.values()[11][3].items() # Post#3 ...

for i in j.values()[11][0].items()[25][1].items(): # Post#0's user info
    print i
#############
# End trial #
#############


# Get data ('friends' timeline posts)
counter = 1
followedPosts = []
while counter < 201: # Went for 200 pages, 100 posts on each. But it doesn't seem to go beyond 2 pages!
    url = 'https://api.weibo.com/2/statuses/friends_timeline.json?access_token=2.00orEdqCbHV6TDfe7c3ed211P_oIRB&count=100&page=' + str(counter)
    r = requests.get(url)
    followedPosts.append(r.json())
    counter += 1

# After one day: re-executed the above code
followedPosts1 = []
url = 'https://api.weibo.com/2/statuses/friends_timeline.json?access_token=2.00orEdqCbHV6TDfe7c3ed211P_oIRB&count=100&page=1'
r = requests.get(url)
followedPosts1.append(r.json())
# Combined:
followedPosts = followedPosts[:2]
followedPosts.extend(followedPosts1) # len(followedPosts) is 3. Contains 100, 49, 100 posts.

# Altogether, execute the above at different time points.
##############################
# Scheduled execution trial: #
##############################
import sched, time
from threading import Timer
s = sched.scheduler(time.time, time.sleep)
def print_time():
    print "From print_time", time.time()

def print_some_times():
    print time.time()
    s.enter(5, 1, print_time, ())
    s.enter(10, 1, print_time, ())
    s.run()
    print time.time()

def addNumbers(a, b):
    print a + b

def add_some_times():
    print time.time()
    s.enter(5, 1, addNumbers, (1, 2))
    s.enter(10, 1, addNumbers, (3, 4))
    s.run()
    print time.time()

add_some_times()
# Output:
# 1461482836.37
# 3
# 7
# 1461482846.37

def add_sched(interval=5, n=10):
    print time.time()
    for i in range(n):
        timePassed = i*interval
        s.enter(timePassed, 1, print_time, ())
        s.enter(timePassed, 1, addNumbers, (1.2, 3.4))
    s.run()
    print time.time()

# Run
add_sched()

#############
# End trial #
#############

#########################################################
### Part 1: Get data
import sched, time
from threading import Timer
s = sched.scheduler(time.time, time.sleep)

def getWeiboFriendsPosts():
    url = 'https://api.weibo.com/2/statuses/friends_timeline.json?access_token=2.00orEdqCbHV6TDfe7c3ed211P_oIRB&count=100&page=1'
    r = requests.get(url)
    #followedPosts.append(r.json())
    import pickle
    pickle.dump(r.json(), open(str(time.time()) + 'followedPosts.p', 'wb'))

#followedPosts = []
def getWeiboFriendsPostsSched(interval=3600, n=10):
    '''
    interval: integer, no. seconds between collection of data.
        E.g. 120 for 2 h
    n: integer, no. collections
        E.g. 10 collections at 2 h each.
    '''
    for i in range(n):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        timePassed = i * interval
        s.enter(timePassed, 1, getWeiboFriendsPosts, ())
        s.run()

getWeiboFriendsPostsSched()



### Part 2: Load data
###################
# Save file trial #
###################
import pickle
import os

pickle.dump(followedPosts, open('followedPosts.p', 'wb'))
listfile = os.listdir('/Users/yingjiang/Dropbox/Learnings/Stats_data/Projects/Weibo/Sinaweibopy')
followedPosts2 = []
for i in listfile:
    if i.endswith('.p'):
        print i
        followedPosts2.append(pickle.load(open(i, 'rb')))
followedPosts = pickle.load(open('followedPosts.p', 'rb'))
#############
# End trial #
#############

def loadWeiboData(directory = '/Users/yingjiang/Dropbox/Learnings/Stats_data/Projects/Weibo/Sinaweibopy'):
    import pickle
    import os
    listfile = os.listdir(directory)
    followedPosts = []
    for i in listfile:
        if i.endswith('.p'):
            print i
            followedPosts.append(pickle.load(open(i, 'rb')))
    return followedPosts
followedPosts = loadWeiboData() # a list of dicts

### Part 3: Get Post status info (id, uid, etc)
#######################
# Get post info trial #
#######################
# Get the above parameters: postID, createdAt, userInfo, isRetweet
# followedPosts[0].values()[11][0].keys().index(u'id') # Get index of post id
# followedPosts[0].values()[11][0].keys().index(u'created_at') # Get index of post date
# followedPosts[0].values()[11][0].keys().index(u'reposts_count') # Get index of post date
# followedPosts[0].values()[11][0].keys().index(u'attitudes_count') # Get index of post date
# followedPosts[0].values()[11][0].keys().index(u'comments_count') # Get index of post date
# followedPosts[0].values()[11][0].keys().index(u'user') # Get index of user info (another dict)

# followedPosts[0].values()[11][0].keys().index(u'retweeted_status') # Get index of retweet info (another dict)
# followedPosts[0].values()[11][0].values()[followedPosts[0].values()[11][0].keys().index(u'id')]
# followedPosts[0].values()[11][0].values()[followedPosts[0].values()[11][0].keys().index(u'created_at')]
# followedPosts[0].values()[11][0].values()[followedPosts[0].values()[11][0].keys().index(u'reposts_count')]
# followedPosts[0].values()[11][0].values()[followedPosts[0].values()[11][0].keys().index(u'attitudes_count')]
# followedPosts[0].values()[11][0].values()[followedPosts[0].values()[11][0].keys().index(u'comments_count')]
# userInfo = followedPosts[0].values()[11][0].values()[followedPosts[0].values()[11][0].keys().index(u'user')]
# userInfo.values()[userInfo.keys().index(u'id')]
# followedPosts[0].values()[11][0].values()[followedPosts[0].values()[11][0].keys().index(u'retweeted_status')]
'''
About retweet info:
If the post is a retweet of another post, then the field (key = u'retweeted_status') exists.
This field returns another set of post info:
~30-length dict, with statuses, reposts_count etc.
Otherwise, the key doesn't exist.
'''
#############
# End trial #
#############

###########################
# Get post info 1st batch #
###########################
# iterate over followedPosts[0].values()[11][i]
postID = []
createdAt = []
userID = []
isRetweet = []
for i in followedPosts[0].values()[11]: # Page 1, 100 data points
    # print i.values()[i.keys().index(u'id')]
    # print i.values()[i.keys().index(u'created_at')]
    postID.append(i.values()[i.keys().index(u'id')])
    createdAt.append(i.values()[i.keys().index(u'created_at')])
    userInfo = i.values()[i.keys().index(u'user')]
    # print userInfo[userInfo.keys().index(u'id')]
    userID.append(userInfo.values()[userInfo.keys().index(u'id')])
    if u'retweeted_status' in i.keys():
        isRetweet.append(True)
    else:
        isRetweet.append(False)
    print isRetweet

for i in followedPosts[1].values()[11]: # 2nd and last page, 49 more data points
    postID.append(i.values()[i.keys().index(u'id')])
    createdAt.append(i.values()[i.keys().index(u'created_at')])
    userInfo = i.values()[i.keys().index(u'user')]
    userID.append(userInfo.values()[userInfo.keys().index(u'id')])
    if u'retweeted_status' in i.keys():
        isRetweet.append(True)
    else:
        isRetweet.append(False)

for i in followedPosts1[0].values()[11]: # 2nd batch; 100 more
    postID.append(i.values()[i.keys().index(u'id')])
    createdAt.append(i.values()[i.keys().index(u'created_at')])
    userInfo = i.values()[i.keys().index(u'user')]
    userID.append(userInfo.values()[userInfo.keys().index(u'id')])
    if u'retweeted_status' in i.keys():
        isRetweet.append(True)
    else:
        isRetweet.append(False)
len(postID) # 248
#################
# End 1st batch #
#################

def getStatusInfo(APIResponseList):
    postID = []
    createdAt = []
    userID = []
    isRetweet = []
    for i in APIResponseList:
        #print APIResponseList.index(i)
        if len(i.values()) > 11:
            for j in i.values()[11]:
                # print i.index(j)
                # postID.append(j.values()[j.keys().index(u'id')])
                postID.append(j.get(u'id'))
                # print postID
                createdAt.append(j.get(u'created_at'))
                userInfo = j.get(u'user')
                # print userInfo[userInfo.keys().index(u'id')]
                userID.append(userInfo.values()[userInfo.keys().index(u'id')])
                if u'retweet_status' in j.keys():
                    isRetweet.append(True)
                else:
                    isRetweet.append(False)
    return postID, createdAt, userID, isRetweet

postID_tmp, createdAt_tmp, userID_tmp, isRetweet_tmp = getStatusInfo(followedPosts)
len(postID_tmp)
len(set(postID_tmp)) # Check that we didn't get overlapped posts

postID = []
createdAt = []
userID = []
isRetweet = []

postID.extend(postID_tmp)
createdAt.extend(createdAt_tmp)
userID.extend(userID_tmp)
isRetweet.extend(isRetweet_tmp)
len(postID)
len(set(postID)) # Check that we didn't get overlapped posts

### Part 4: Get post info - the most updated repostNo, commentNo
def getPostInfo(postID):
    likeNo = []
    commentNo = []
    repostNo = []
    try:
        for i in postID:
            url = 'https://api.weibo.com/2/statuses/count.json?access_token=2.00orEdqCbHV6TDfe7c3ed211P_oIRB&ids=' + str(i)
            r = requests.get(url)
            status = r.json()
            likeNo.append(status[0].values()[0])
            commentNo.append(status[0].values()[2])
            repostNo.append(status[0].values()[3])
    except KeyError, e:
        print 'There is an error. Most likely user rate limit has been exceeded:', e
    return likeNo, commentNo, repostNo
likeNo_tmp, commentNo_tmp, repostNo_tmp = getPostInfo(postID[152:])
likeNo = []
commentNo = []
repostNo = []
print len(likeNo_tmp) # see how many new posts have been processed

likeNo.extend(likeNo_tmp)
commentNo.extend(commentNo_tmp)
repostNo.extend(repostNo_tmp)
print len(likeNo) # see how many posts' info has been accumulated

key = ['postID', 'createdAt', 'userID', 'isRetweet', 'likeNo', 'commentNo', 'repostNo']
val = [postID, createdAt, userID, isRetweet, likeNo, commentNo, repostNo]
posts = dict(zip(key, val))
pickle.dump(posts, open('postInfo.p', 'wb')) # Saved all postInfo

### Part 5: Get comment text
cmtTextAll = []

for i in postID[34:]:
    '''
    Notes on startIndex:
    The algorithm may halt at postID.index(i) = startIndex+1
    At startIndex+1, the algorithm returns 10023 - the error code for user exceeding rate limit (API timeout).
    The code may overrun a little, returning 10023 for a few more indices afterwards.
    To the returned cmtTextAll list, cmtTextAll = cmtTextAll[:startIndex+1]
    This cuts off the remaining indices.
    To restart, manually modify the starting index! E.g. in this case, pick up from 34.
    '''

    print postID.index(i) ### Index

    url_cmt = 'https://api.weibo.com/2/comments/show.json?access_token='+access_token1+'&id=' + str(i) + '&count=200&page=1'
#    print url_cmt

    r = requests.get(url_cmt)
    nPages = r.json().values()[1] / 200 + 1 # Total_commentNo/200+1
    # if nPages > 10:
    #     nPages = 10 # maximum allowed pages returned is 10.
    print r.json().values()[1] ### Number of comments for the post
#    print nPages

    if r.json().values()[1]: # Check if the comments are empty (deleted post?)
        cmtText = []

        for p in [a+1 for a in range(nPages)]:
            url_cmt = 'https://api.weibo.com/2/comments/show.json?access_token='+access_token1+'&id=' + str(i) + '&count=200&page=' + str(p)
#            print url_cmt

            r = requests.get(url_cmt)
            if len(r.json()) > 3:
                print len(r.json().values()[3]) # If this number is 10023, it means request limit has exceeded. The connection needs to be reset.

                for comment in r.json().values()[3]: # Each comment on (200 max) on the page.
                    cmtText.append(comment.values()[3]) # comment text
                # print len(cmtText)

        cmtTextAll.append(cmtText)

    else:
        cmtTextAll.append(0)

'''
Types of errors:
10023: API request exceeded time limit
21327: access token expired
'''

# Case 1:
# If there's a weird error that stops collection half way, just append what's already collected.
len(cmtText)
# Append newly acquired, current data
cmtTextAll.append(cmtText)
# Check length of acquired data, to know where to start next
len(cmtTextAll)

# Case 2:
# If the script overruns and is getting 10023 errors (API timeout; no data is getting acquired), cut the vector at the index of API timeout. 
cmtTextAll = cmtTextAll[:1381]
# Append all newly acquired data upto the '10023' post.
cmtTextAll.append(cmtText)
# Check length of acquired data, to know where to start next
len(cmtTextAll)

# Back to the loop; manually modify the starting index!

#########
# TRIAL #
#########
def getComments(postID, startIndex = 72):
    '''
    Notes on startIndex:
    The algorithm may halt at postID.index(i) = startIndex+1
    At startIndex+1, the algorithm returns 10023 - the error code for user exceeding rate limit.
    The code may overrun a little, returning 10023 for a few more indices afterwards.
    To the returned cmtTextAll list, cmtTextAll = cmtTextAll[:startIndex+1]
    This cuts off the remaining indices.
    To restart, run getComments(postID, startIndex+1)
    '''

    cmtTextAll = []
    try:
        for i in postID[startIndex:]: # pick up from post #34.
            print postID.index(i) ### Index

            url_cmt = 'https://api.weibo.com/2/comments/show.json?access_token=2.00orEdqCbHV6TDfe7c3ed211P_oIRB&id=' + str(i) + '&count=200&page=1'
            r = requests.get(url_cmt)
            nPages = r.json().values()[1] / 200 + 1 # Total commentNo / 200 + 1
            if nPages > 10:
                nPages = 10 # maximum allowed pages returned is 10.

            print r.json().values()[1] ### Number of comments for the post

            if r.json().values()[1]: # Check if the comments are empty (deleted post?)
                cmtText = [] # create a storage for every post's comments

                for p in [a+1 for a in range(nPages)]:
                    url_cmt = 'https://api.weibo.com/2/comments/show.json?access_token=2.00orEdqCbHV6TDfe7c3ed211P_oIRB&id=' + str(i) + '&count=200&page=' + str(p)

                    r = requests.get(url_cmt)
                    if len(r.json()) > 3:
                        print len(r.json().values()[3]) ### Comments on each page. If this number is 10023, it means request limit has exceeded. The connection needs to be reset.

                        for comment in r.json().values()[3]: # Each comment on (200 max) on the page.
                            cmtText.append(comment.values()[3]) # comment text
                cmtTextAll.append(cmtText)
            else:
                cmtTextAll.append(0)
    except KeyboardInterrupt, e:
        print 'There is an error. User rate limit has been exceeded and user interrupted algorithm manually.', e
    return cmtTextAll

# Check comment numbers for each post
def checkCommentNo(cmtTextAll):
    '''
    cmtTextAll: a list of lists.
    Each element is a list of comment lines for a post.
    '''
    commentNoAll = []
    for i in cmtTextAll:
        if type(i) is int:
            commentNoAll.append(i)
        else:
            commentNoAll.append(len(i))
    return commentNoAll
checkCommentNo(cmtTextAll)

# Remove duplicate postIDs if any.
def removeListDuplicates(ls):
    seen = set()
    ls1 = []
    for x in ls:
        if x not in seen:
            ls1.append(x)
            seen.add(x)
    return ls1
#############
# END TRIAL #
#############


'''
Notes on progress:
------------------

postID_batch    nPosts  nStatuses_gotten    nComments_gotten
1               735     735                 735
2               97      97                  97
3               99      99                  99
4               97      97                  97
5               100     100                 100
6               100     100                 (1228)
7               100     100
8               100     100
Total           1428    1428
'''
pickle.dump(cmtTextAll, open('cmtInfo.p', 'wb'))

### Part 6: Reopening the saved data; cleaning, feature processing
# Start new ipython notebook

# Import data
postInfo = pickle.load(open('postInfo.p', 'rb'))
cmtInfo = pickle.load(open('cmtInfo.p', 'rb'))
# To check if the data is opened correctly:
print len(postInfo), len(cmtInfo), len(postInfo.values()[0])
## 7 1428 1428

# Arrange imported dict into a dataframe
import pandas as pd
cmtData = pd.DataFrame(postInfo.values()).transpose()
cmtData.columns = postInfo.keys()
''' Order got rearranged: 
['postID',
 'repostNo',
 'userID',
 'likeNo',
 'commentNo',
 'isRetweet',
 'createdAt'] '''

# Create the feature of no of ad words -
# Count the number of ad words in each post!
adWord = '广告'
adWord = adWord.decode('utf8')
adWordNo = []
for i in cmtInfo:
#    print 'Post no.: ', cmtInfo.index(i)
    if isinstance(i, int):
        adWordNo.append('Empty post')
    if isinstance(i, list):
        counter = 0
        for j in i:
#             print 'Comment no.:', i.index(j)
#             print j
            if unicode(adWord) in j:
                counter += 1
        adWordNo.append(counter)

sum(i > 7 for i in adWordNo) # 395
sum(i > 10 for i in adWordNo) / float(len(adWordNo)) # 28%! (out of 1428 posts)
sum(i == 'Empty post' for i in adWordNo) # 387 empty posts
# Apparently, 'Empty post' counts as > 10... That's not good.


# Combine all features
# Add 1 column: noAdWords
cmtData['adWordNo'] = adWordNo

# Remove: Empty posts; isRetweet Posts
cmtData1 = cmtData[cmtData.adWordNo != 'Empty post'] # 1041 posts left
sum(i > 10 for i in cmtData1.adWordNo) # Only 8 posts. 
sum(i > 10 for i in cmtData1.adWordNo) / float(cmtData1.shape[0]) # Only 0.77%

sum(i > 0 for i in cmtData1.adWordNo) # Only 56 posts. 
sum(i > 0 for i in cmtData1.adWordNo) / float(cmtData1.shape[0]) # 5%

sum(cmtData1.isRetweet == True) # 0. All retweet posts have been removed.

# Plot the following graphs:
# 1. Cluster repostNo
# 2. repostNo vs comment No
# 3. Cluster noAdWords
# 4. noAdWords vs repost No

import matplotlib.pyplot as plt

# adWordNo histogram
%matplotlib inline
x = cmtData1.adWordNo
plt.hist(x, 100, normed = 1, facecolor = 'green', alpha = 0.75)
plt.show()

# repostNo histogram
x = cmtData1.repostNo
plt.hist(x, 50, normed = 1, facecolor = 'green', alpha = 0.75)
plt.show()

# 1. Cluster noAdWords vs repostNo
from sklearn.cluster import KMeans
x = cmtData1[['repostNo', 'adWordNo']]
nclusters = 3
km = KMeans(nclusters)
km.fit(x)
labels = km.labels_ # numpy 1D arrays
centroids = km.cluster_centers_ # numpy arrays
for i in range(nclusters):
    ds = x[labels == i]
    # Plot the data
    plt.plot(ds.ix[:, 0], ds.ix[:, 1], 'o')
    # Plot the centroids
    lines = plt.plot(centroids[i, 0], centroids[i, 1], 'kx')
    # Make the centroid 'x's bigger
    plt.setp(lines, ms = 15)
    plt.setp(lines, mew = 2)
plt.show()
# Conclusion: Higher adwd, lower repostNos.

# 2. Cluster adWordNo only
x = pd.DataFrame(cmtData1['adWordNo'])
nclusters = 2
km = KMeans(nclusters)
km.fit(x)
labels = km.labels_
centroids = km.cluster_centers_

for i in range(nclusters):
    ds = x[labels == i]
    # Plot the data
    plt.plot(ds, pd.DataFrame([1] * len(ds)), 'o')
    # Plot the centroids
    lines = plt.plot(centroids[i, 0], 1, 'kx')
    # Make the centroid 'x's bigger
    plt.setp(lines, ms = 15)
    plt.setp(lines, mew = 2)
plt.show()
# 2 clusters; the first at 0; the second at 40.

# 3. Cluster repostNo only
x = pd.DataFrame(cmtData1['repostNo'])
nclusters = 3
km = KMeans(nclusters)
km.fit(x)
labels = km.labels_
centroids = km.cluster_centers_

for i in range(nclusters):
    ds = x[labels == i]
    # Plot the data
    plt.plot(ds, pd.DataFrame([1] * len(ds)), 'o')
    # Plot the centroids
    lines = plt.plot(centroids[i, 0], 1, 'kx')
    # Make the centroid 'x's bigger
    plt.setp(lines, ms = 15)
    plt.setp(lines, mew = 2)
plt.show()
# 3 clusters: 1100; 20000; 65000

# 4. repostNo vs commentNo
x = cmtData1[['commentNo', 'repostNo']]
nclusters = 3
km = KMeans(nclusters)
km.fit(x)

labels = km.labels_
centroids = km.cluster_centers_

for i in range(nclusters):
    ds = x[labels == i]
    # Plot the data
    plt.plot(ds.ix[:, 0], ds.ix[:, 1], 'o')
    # Plot the centroids
    lines = plt.plot(centroids[i, 0], centroids[i, 1], 'kx')
    # Make the centroid 'x's bigger
    plt.setp(lines, ms = 15)
    plt.setp(lines, mew = 2)

plt.xlabel('Comment No')
plt.ylabel('Repost No')

plt.show()
# Cluster centroids do grow together, almost linearly. However:
# Cluster 1: Low repost, low comments - normal
# Cluster 2: Low comments, mid-high repost - rigged?
# Cluster 3: 1 outlier, high comments, high repost - normal

################
'''
To further analyze the "reach" of social media influencers (wanghong),
Need to know:
# Followers' age
# Followers' languages
# Followers' countries
# How many followers are active
# How many followers are paid

