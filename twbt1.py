from __future__ import print_function
from __future__ import absolute_import
import requests
import simplejson
from PIL import Image
from StringIO import StringIO
import twitter
import sys
import os

input = raw_input

#Retrieve random word!
r = requests.get('http://randomword.setgetgo.com/get.php')
word = r.text

#Google image search word
r = requests.get('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + r.text)
results = simplejson.loads(r.text)

data = results['responseData']
dataInfo = data['results']

#Download 3rd result
rescount = 0
savename = ''
for myUrl in dataInfo:
  rescount += 1
  if(rescount == 3):
    savename = myUrl['unescapedUrl'].rsplit('/',1)[1]
    rImage = requests.get(myUrl['unescapedUrl'])
    i = Image.open(StringIO(rImage.content))
    i.save(savename)

#Twitter Step

#  AUTHENTICATION PROCESS
oauthInfo = sys.argv
tweeet = twitter.Api(consumer_key=oauthInfo[1],
  consumer_secret=oauthInfo[2],
  access_token_key=oauthInfo[3],
  access_token_secret=oauthInfo[4])

#Tweet Media
tweeet.PostMedia('random word: ' + word,savename)

#Deletes files to keep folder clean
os.remove(savename)
