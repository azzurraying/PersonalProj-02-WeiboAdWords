#########################################################
import requests
from requests.auth import HTTPDigestAuth
import json
import urllib, urllib2
from urllib2 import Request, urlopen, URLError

from weibo import APIClient
import webbrowser

import sched, time
from threading import Timer
import pickle
import os

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
##################################################

### Part 0: Get access token
APP_KEY = '3182990075'
APP_SECRET = 'cf1f746ac349daae676c4d583587b508'
CALLBACK_URL = 'https://github.com/azzurraying'
client = APIClient(app_key = APP_KEY,
                  app_secret = APP_SECRET,
                  redirect_uri = CALLBACK_URL)
url = client.get_authorize_url()
webbrowser.open_new(url)
# Web browser opens. Copy the last 32 digits: that's the code.

code = 'a5a3391a4cd81b01cabd09240df8a2b1'
r = client.request_access_token(code)
access_token1 = r.access_token # This is what we use
expires_in = r.expires_in


### Part 1: Get data

def getWeiboFriendsPosts():
    url = 'https://api.weibo.com/2/statuses/friends_timeline.json?access_token='+access_token1+'&count=100&page=1'
    r = requests.get(url)
    followedPosts.append(r.json())
    import pickle
    pickle.dump(r.json(), open(str(time.time()) + 'followedPosts.p', 'wb'))

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

# Use Elbow plot to verify number of clusters
# Approach 1: Manually calculate within-cluster SSE using labels
# This example is in R:
# https://datasciencelab.wordpress.com/2013/12/27/finding-the-k-in-k-means-clustering/
# This example isn't quite right in computing within-cluster SSE:
# http://datascience.stackexchange.com/questions/6508/k-means-incoherent-behaviour-choosing-k-with-elbow-method-bic-variance-explain

'''
# np.min:
d1 = np.array(
      [[ 0,  1],
        [ 2,  3],
        [ 4,  5]])
print np.min(d1, axis = 1)
'''
'''
# Find out dimensions of the arrays
for lab, cent, d in zip(labels, centroids, D_k):
    print len(set(lab)) # 1, 2, 3, 4, 5, 6, 7, 8, 9
    print len(cent) # 1, 2, 3, 4, 5, 6, 7, 8, 9
    print d.shape # (1042, 1), (1042, 2), (1042, 3) ... etc
    print ''
'''

'''
# Trial of getting within-cluster SSE
i = 1
x_c_tri = x[labels[i] == list(set(labels[i]))[0]]
# The following 3 ways are the same, to compute within-cluster distance:
print cdist(x_c_tri, np.array([[  1.19931213e+03,   4.12915851e-01]]), 'euclidean')
print cdist(x_c_tri, np.reshape(centroids[i][0], (-1, 2)), 'euclidean')
d = [cdist(x_c_tri, np.reshape(cent_, (-1, 2)), 'euclidean') for cent_ in centroids[i]]
print d[0]

# To find within-cluster SSE:
print sum(d[0]**2)
'''
x = cmtData1[['repostNo', 'adWordNo']]
K = range(1,10)
km = [KMeans(n_clusters=k).fit(x) for k in K]
labels = [k.labels_ for k in km]
centroids = [k.cluster_centers_ for k in km]

wcss = []
for lab, cent in zip(labels, centroids):
    x_c = []
    wcss.append(0)
    for lab_, cent_ in zip(list(set(lab)), cent): # lab_ within lab: 0, 1, etc; cent_ within cent
        x_c = x[lab == lab_] # Generate subset of x that corresponds to the current lab_
        d = cdist(x_c, np.reshape(cent_, (-1, 2)), 'euclidean') # Generate vector of distances between x_c and current cent_ 
        wcss[-1] += float(sum(d**2))

tss = wcss[0]
y_elbow = [i/x.shape[0] for i in wcss]
y_rss = [100-i/tss*100 for i in wcss]

kIdx = 3-1

# Elbow plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(K, y_elbow, 'b*-')
ax.plot(K[kIdx], y_elbow[kIdx],
        marker='o', markersize=12, markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
plt.grid(True)
plt.xlabel('Number of clusters')
plt.ylabel('Average within-cluster sum of squares')
plt.title('Elbow for KMeans clustering')

# Variance explained plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(K, y_rss, 'b*-')
ax.plot(K[kIdx], y_rss[kIdx],
        marker='o', markersize=12, markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
plt.grid(True)
plt.xlabel('Number of clusters')
plt.ylabel('Percentage of variance explained')
plt.title('Elbow for KMeans clustering')

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

