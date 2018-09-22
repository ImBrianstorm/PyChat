# *PyChat*

Chat client server built in Python

I have eliminated this repository a couple of times because it was not what I wanted to be, but finally
I have done something decent.

## Prerequisites

  * Python 3.x
  * Tkinter

## The Server

The first thing we need is to deploy our server with the following command

    $ python3 run_chat_server.py

## The Client

Once we have deployed our server, then we can use our client to enjoy our chat, by running the following command

    $ python3 run_chat_server.py

> I'm having trouble with this one, but I will fix it.

## The tests

In an attempt to make better software,  I have added a couple of scripts that deploy unit tests, so we can be a little safer that we are making the things right :)

  	# To test the server, we must execute the next line
    $ python3 test_server.py
    # Similarly, we execute the next to test the client
    $ python3 test_client.py
    # And finally, we can run the following to test our chatrooms
    $ python3 test_chat_room.py

These tests are suppossed to test the code and not to throw errors.

> Dev: [Mauricio Chávez](https://twitter.com/ImBrianstorm)
