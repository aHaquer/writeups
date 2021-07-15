# Secured Session - 247CTF

```
If you can guess our random secret key, we will tell you the flag securely stored in your session.

```

When we open up the website we're greeted with a plain-text page of what is presumably the code running server-side.

```python
import os
from flask import Flask, request, session
from flag import flag

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

def secret_key_to_int(s):
    try:
        secret_key = int(s)
    except ValueError:
        secret_key = 0
    return secret_key

@app.route("/flag")
def index():
    secret_key = secret_key_to_int(request.args['secret_key']) if 'secret_key' in request.args else None
    session['flag'] = flag
    if secret_key == app.config['SECRET_KEY']:
      return session['flag']
    else:
      return "Incorrect secret key!"

@app.route('/')
def source():
    return "

%s

" % open(__file__).read()

if __name__ == "__main__":
    app.run()

```



A [Flask](https://flask.palletsprojects.com/en/2.0.x/) website is created, and its [SECRET_KEY]() configuration variable is set to the result of an os.urandom(). At this point, I assumed that the os.urandom() was somehow predictable, and began to look into it. 

Python's urandom is actually insecure in some cases:

![](/home/ahaquer/Repos/writeups/ctfmisc/assets/secure-session/urandom.png)

On Linux, os.urandom() works by tapping into [/dev/urandom](https://linux.die.net/man/4/urandom), which gathers entropy from device drivers. When operating normally, this provides a rather secure source of randomness for applications, but when its entropy pool is low (such as at system boot), the data generated from /dev/urandom can be predictable. This article from [Linux Weekly News](https://lwn.net/Articles/693189/) goes into much more depth than I will here.

This is interesting, but it doesn't do much to aid in our exploitation. It seems unlikely that we would be able to use boot time to our advantage, and the session cookie we're actually targeting doesn't seem at all effected by the secret key in the code.

The session cookie we're targeting doesn't appear to be encrypted, so I started to wonder how Flask's secret key configuration variables actually protected the stored data.

![](/home/ahaquer/Repos/writeups/ctfmisc/assets/secure-session/session-cookie.png)

That led me to [this article](https://blog.miguelgrinberg.com/post/how-secure-is-the-flask-user-session) which helped me solve the challenge. The session cookie isn't at all encrypted, that's not what Flask's SECRET_KEY [actually does](https://stackoverflow.com/a/48596852). This session cookie is just [Base64](https://en.wikipedia.org/wiki/Base64) encoded, and the os.urandom snippet was a red herring! When we Base64 decode the session cookie, we're eventually led to our flag:

![](/home/ahaquer/Repos/writeups/ctfmisc/assets/secure-session/flag.png)

I got tunnel vision on os.urandom() before seeing the obvious.