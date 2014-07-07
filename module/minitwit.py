# -*- coding: utf-8 -*-
from __future__ import with_statement
#import time
import os, time, sys
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from contextlib import closing
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from werkzeug.security import check_password_hash, generate_password_hash
#import Adafruit_BBIO.GPIO as GPIO

#pipe
pipe_name = 'pipefile'
pipe_name2 = 'pipefile2'
if not os.path.exists(pipe_name):
	os.mkfifo(pipe_name)

if not os.path.exists(pipe_name2):
	os.mkfifo(pipe_name2)


pipout=os.open(pipe_name, os.O_WRONLY)
pipout2=os.open(pipe_name2, os.O_WRONLY)

con = sqlite3.connect("our_db.sqlite", check_same_thread=False)
con.isolation_level =None #auto commit
cursur = con.cursor()
cursur.execute("select ID from light order by ID DESC limit 1")
print cursur.fetchone()
print "hello mungchung"

#DB 설정 부분...추후 수정요
# configuration
DATABASE = './minitwit.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

#LED name and GPIO number
#key is 'RoomNum' -> how to send a message to bb?
#받으려는 비글본에 GPIO 설정이 되어있어야함
#GPIO의 ' ' 삭제해서 사용
#포트 설정은 단순한 임시값. 방 번호로 지정해서 메세지 보내기?
leds = {
	'Room1' : {'name' : 'led1', 'state' : 'GPIO.LOW'},
	'Room2' : {'name' : 'led2', 'state' : 1},
	'Room3' : {'name' : 'led3', 'state' : 'GPIO.LOW'},
	'Room4' : {'name' : 'led4', 'state' : 'GPIO.LOW'}
	}

windows = {
	'Room1' : {'name' : 'window1', 'state' : 0},
	'Room2' : {'name' : 'window2', 'state' : 0},
	'Room3' : {'name' : 'window3', 'state' : 1},
	'Room4' : {'name' : 'window4', 'state' : 0}
	}
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('HOME_MANAGEMENT', silent=True)


def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """Creates the database tables."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


#??????
def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = g.db.execute('select user_id from user where username = ?',
                       [username]).fetchone()
    return rv[0] if rv else None

#TIME STAMP
def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')

#필요한가??
def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), 
         size)


@app.before_request
def before_request():
    """Make sure we are connected to the database each request and look
    up the current user so that we know he's there.
    """
    g.db = connect_db()
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?',
                          [session['user_id']], one=True)


@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def home():
       
	cursur.execute("select * from light order by ID DESC limit 1")
	print cursur.fetchone()
	print "hello mungchung"
	error = None
	return render_template('home.html', error = error)

#기본은 자동모드?
#로그인을 하면 뜨는 페이지!
#test.html -> current state
@app.route('/<username>')
def user_timeline(username):
    """Display's a users tweets."""
    profile_user = query_db('select * from user where username = ?',
                            [username], one=True)
    if profile_user is None:
        abort(404)
    followed = False
    if g.user:
        followed = query_db('''select 1 from follower where
            follower.who_id = ? and follower.whom_id = ?''',
            [session['user_id'], profile_user['user_id']],
            one=True) is not None
    return render_template('test.html')

@app.route('/Automatic')
def Automatic():
	"""test GPIO"""
	light = []
	temper = []
	humid = []
	totalnum = 2
#	cursor.execute("SELECT ID FROM cur_person order by ID DESC limit 1")
#	totalnum = int(cursor.fetchone()[1])
        print "before"
	cursur.execute("SELECT * FROM light order by ID DESC limit 1")
	print "after"
        for i in range(totalnum):
		light.append(0)
		temper.append(0)
		humid.append(0)
	lighttable = cursur.fetchone()
	for i in range(totalnum):
		
		light[i] = lighttable[i+1]
	
	cursur.execute("SELECT * FROM temper order by ID DESC limit 1")
        tempertable = cursur.fetchone()
	for i in range(totalnum):
		temper[i] = tempertable[i+1]


	cursur.execute("SELECT * FROM humid order by ID DESC limit 1")
	humidtable = cursur.fetchone()
	for i in range(totalnum):
		humid[i] = humidtable[i+1]
	
	error = None
	return render_template('Automatic.html', error=error, light=light, \
			temper=temper, humid=humid, totalnum=totalnum)

@app.route('/Manual')
def Manual():
	light = []
	temper = []
	humid = []
	totalnum = 2
#	cursor.execute("SELECT ID FROM cur_person order by ID DESC limit 1")
#	totalnum = int(cursor.fetchone()[1])
	print "before"
	cursur.execute("SELECT * FROM light order by ID DESC limit 1")
	print "after"
        for i in range(totalnum):
		light.append(0)
		temper.append(0)
		humid.append(0)
	lighttable = cursur.fetchone()
	for i in range(totalnum):
		light[i] = lighttable[i+1]
	
	cursur.execute("SELECT * FROM temper order by ID DESC limit 1")
        tempertable = cursur.fetchone()
	for i in range(totalnum):
		temper[i] = tempertable[i+1]


	cursur.execute("SELECT * FROM humid order by ID DESC limit 1")
	humidtable = cursur.fetchone()
	for i in range(totalnum):
		humid[i] = humidtable[i+1]
	
	error = None
	return render_template('Manual.html', error=error, light=light, \
			temper=temper, humid=humid, totalnum=totalnum)


#LED ON/OFF 버튼 누를때 실행되는 부분
#LED state : GPIO.input("P8_10")
@app.route('/<led>/<num>/<act>')
def action(led, num, act):
	#비글본에 메세지 전달?
	command = 0
	if act == "on":
		command = 1
	else:
		command = 0
	
	message = "{'light' : '%d/%d'}\n"%(int(num), int(command))
        print message + "before wirte pipe=============="
	os.write(pipout, message)
	print message + "after wirte pipe============"
	
	light = []
	temper = []
	humid = []
	totalnum = 2
#	cursor.execute("SELECT ID FROM cur_person order by ID DESC limit 1")
#	totalnum = int(cursor.fetchone()[1])
        print "before"
	cursur.execute("SELECT * FROM light order by ID DESC limit 1")
	print "after"
        for i in range(totalnum):
		light.append(0)
		temper.append(0)
		humid.append(0)
	lighttable = cursur.fetchone()
	for i in range(totalnum):
		
		light[i] = lighttable[i+1]
	
	cursur.execute("SELECT * FROM temper order by ID DESC limit 1")
        tempertable = cursur.fetchone()
	for i in range(totalnum):
		temper[i] = tempertable[i+1]


	cursur.execute("SELECT * FROM humid order by ID DESC limit 1")
	humidtable = cursur.fetchone()
	for i in range(totalnum):
		humid[i] = humidtable[i+1]
	
	error = None
	return render_template('Manual.html', error=error, light=light, \
			temper=temper, humid=humid, totalnum=totalnum)

#WINDOWS
@app.route('/<window>/<num>/<winact>')
def winaction(window, num, winact):
	if act == "on":
		print "window open"
	return render_template('Manual.html', error=error)

#로그인 -> 디비에서 값 가져오는거 분석해서 센서 값들 가져오기
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('test'))
    error = None
    if request.method == 'POST':
        user = query_db('''select * from user where
            username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'],
                                     request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user['user_id']
            return redirect(url_for('test'))
    return render_template('login.html', error=error)

#자동 관리 페이지로 만들어보기//포스트는 필요없을듯
#Current State
@app.route('/test', methods=['GET', 'POST'])
def test():
	"""Current State"""
	light = []
	temper = []
	humid = []
	totalnum = 2
#	cursor.execute("SELECT ID FROM cur_person order by ID DESC limit 1")
#	totalnum = int(cursor.fetchone()[1])
        print "before"
	cursur.execute("SELECT * FROM light order by ID DESC limit 1")
	print "after"
        for i in range(totalnum):
		light.append(0)
		temper.append(0)
		humid.append(0)
	lighttable = cursur.fetchone()
	for i in range(totalnum):
		
		light[i] = lighttable[i+1]
	
	cursur.execute("SELECT * FROM temper order by ID DESC limit 1")
        tempertable = cursur.fetchone()
	for i in range(totalnum):
		temper[i] = tempertable[i+1]


	cursur.execute("SELECT * FROM humid order by ID DESC limit 1")
	humidtable = cursur.fetchone()
	for i in range(totalnum):
		humid[i] = humidtable[i+1]
	
	error = None
	return render_template('test.html', error=error, light=light, \
			temper=temper, humid=humid, totalnum=totalnum)


@app.route('/Usertemp', methods=['GET', 'POST'])
def Usertemp():
	if request.method == 'POST':
		print 'usertemp' + "============> USER TEMP 1"
		print 'usertemp2' + "============> USER TEMP 2"
		return render_template('tempset.html')
	return render_template('tempset.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    if g.user:
        return redirect(url_for('test'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                 '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            g.db.execute('''insert into user (
                username, email, pw_hash) values (?, ?, ?)''',
                [request.form['username'], request.form['email'],
                 generate_password_hash(request.form['password'])])
            g.db.commit()
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('home'))


# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime
app.jinja_env.filters['gravatar'] = gravatar_url


if __name__ == '__main__':
  init_db()
  app.run(host='0.0.0.0', port= 5000, debug = True)
  
