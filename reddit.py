
import pdb; pdb.set_trace()

import praw,time,pyprind,requests

r = praw.Reddit(user_agent='my_cool_application')
submissions = r.get_subreddit('opensource').get_hot(limit=299)
# print [str(x) for x in submissions]

#potential blacklist items
#(like i'm five)
#edit

lineBreak = '\n\n\n'
print lineBreak
rawInput = raw_input("What do you want me to explain: ")
rawInput = rawInput.lower()

#spell checker
base_url = 'http://www.google.com/complete/search?output=toolbar&q=%s'
url = base_url % rawInput
response = requests.get(url)
# print response

try:
    first_suggestion = response.text.split('suggestion data=')[1].split('"/>')[0][1:]
    # first_suggestion = first_suggestion.lower()
except:
	first_suggestion = ""

if len(rawInput)<1:
    print lineBreak
    rawInput = raw_input("looks like you didn't enter anything, try again: ")

while len(rawInput)>0:
    if first_suggestion != rawInput:
        print lineBreak
        rawInput2 = raw_input("Did you mean " + first_suggestion +" ... Y/N?" ": ")
        rawInput2 = rawInput2.lower()
        if "y" or "Y" in rawInput2:
            rawInput = first_suggestion
        if "n" or "N" in rawInput2:
            continue

    print lineBreak
    print "fetching answer..."
    print lineBreak

    query = r.search(rawInput, subreddit="explainlikeimfive", sort=None, syntax=None, period=None)
    queryArr = []
    for i in query:
        queryArr.append(i)

    try:
        if queryArr[0]:
            submissionID = queryArr[0]
        else:
            submissionID = queryArr[1]
    except:
        print "error pulling data from Reddit... goodbye!!"
        print lineBreak
        break

    submissionURL = submissionID.url
    submissionID = queryArr[0].id
    submission = r.get_submission(submission_id=submissionID)
    itemlist = submission.comments

    if len(itemlist[0].body)<4400 and len(itemlist[0].body)>30:
        if queryArr[0].title:
            postTitle = queryArr[0].title
        else:
            postTitle = "could not fetch post title"
        postTitle = postTitle.replace("ELI5:","").replace(" ,","")
        print ("%s,%s") % ("POST URL: ",submissionURL)
        print lineBreak
        print ("%s,%s") % ("POST TITLE: ",postTitle)
        print lineBreak
        print itemlist[0].body

    else:
        if queryArr[1].title:
            postTitle = queryArr[1].title
            # print queryArr[1].url
        else:
            postTitle = "could not fetch post title"
        postTitle = postTitle.replace("ELI5:","").replace(" ,","")
        print ("%s,%s") % ("POST URL: ",submissionURL)
        print lineBreak
        print ("%s,%s") % ("POST TITLE: ",postTitle)
        print lineBreak
        print itemlist[1].body

    print lineBreak
    break
exit()
