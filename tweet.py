#!/usr/local/bin/python3

TwitterAPIKey = "QIiVmMFqExJTzsOeQItue6z7E"
TwitterAPIKeySecret = "0ZamOx1PrgdP693YUHqvNz5nm8dysUDmFwGPfUE0vjwqr8y1fX"
TwitterAccessToken = "788872435965628416-1Xz8H0RhETDynI0m9MMLPzcK230e32Z"
TwitterAccessTokenSecret = "FchHX70ckdkQ9bIWFVtMiPQ8BXza1hUyvEWNfwdZyLn2D"

import matplotlib

matplotlib.use("TkAgg")

import tweepy
import json
import tkinter
import sys
import numpy
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as mtk
import matplotlib.animation

auth = tweepy.OAuthHandler(TwitterAPIKey, TwitterAPIKeySecret)
auth.set_access_token(TwitterAccessToken, TwitterAccessTokenSecret)

api = tweepy.API(auth)


class TwitterListener(tweepy.StreamListener):

    def __init__(self, api=None):
        super(tweepy.StreamListener, self).__init__()
        self.num_tweets = 0

    def on_data(self, data):
        global tweetstream
        self.num_tweets += 1
        newtweet = json.loads(data)
        cleantext = newtweet['text'].encode('ascii', "ignore")
        cleantext = cleantext.decode('utf-8')
        tweetstream.insert(tkinter.END, newtweet['user']['screen_name'] + '    ' + newtweet[
            'created_at'] + '\n' + cleantext + '\n\n')

    def on_error(self, error):
        if error == 420:
            return False


def quitnow():
    MyStream.disconnect()
    sys.exit()
    # rootwindow.destroy()


def follow_hashtag():
    MyStream.filter(track=[hashtagtext.get()], is_async=True)


MyTwitterListener = TwitterListener()
MyStream = tweepy.Stream(auth=api.auth, listener=MyTwitterListener)

rootwindow = tkinter.Tk()
rootwindow.title("Twitter Stream Follower")

hashtaglabel = tkinter.Label(rootwindow, text="Enter hashtag: ")
hashtaglabel.grid(row=0, column=0, sticky="nsew")

hashtagtext = tkinter.StringVar()
hashtagin = tkinter.Entry(rootwindow, textvariable=hashtagtext)
hashtagin.grid(row=0, column=1, sticky="nsew")

goforit = tkinter.Button(rootwindow, text="Follow Hashtag", command=follow_hashtag)
goforit.grid(row=0, column=2, sticky="nsew")

quitbutton = tkinter.Button(rootwindow, text="Quit", command=quitnow)
quitbutton.grid(row=2, column=0, columnspan=4, sticky="nsew")

tweetstream = tkinter.Text(rootwindow)
tweetstream.grid(row=1, column=2, columnspan=2, sticky="nsew")

textscroll = tkinter.Scrollbar(rootwindow, orient=tkinter.VERTICAL)
textscroll.grid(row=1, column=4, sticky="nsew")
textscroll.config(command=tweetstream.yview)
tweetstream.config(yscrollcommand=textscroll.set)

fig = plt.figure()

figcanvas = mtk.FigureCanvasTkAgg(fig, rootwindow)
figcanvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky="nsew")

xdata = numpy.arange(0, 12)
ydata = numpy.zeros(12)

rateplot, = plt.plot(xdata, ydata)
plt.ylim(0, 20)


def animinit():
    pass


def rateanim(index):
    ydata[0:11] = ydata[1:12]
    ydata[11] = MyTwitterListener.num_tweets
    MyTwitterListener.num_tweets = 0
    rateplot.set_ydata(ydata)
    return rateplot,


rateani = matplotlib.animation.FuncAnimation(fig, rateanim, frames=12, interval=5000, init_func=animinit, blit=False,
                                             repeat=True)

rootwindow.mainloop()


