from flask import Flask, render_template
from threading import Thread
import logging

app = Flask('')

# make ping log go away
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#PAGES
# ---------------------------------------

@app.route('/')
def base():
  return render_template('base.html')


@app.route('/six')
def six():
  return 'six'

# ---------------------------------------

def run():
  app.run(host='0.0.0.0',port=8080)

def online():
  t = Thread(target=run)
  t.start()