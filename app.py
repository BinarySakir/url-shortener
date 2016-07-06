from flask import Flask, render_template, request, abort, redirect
from werkzeug import url_fix
from flask_mysqldb import MySQL
from hashids import Hashids
from re import match
import json

app = Flask(__name__)
mysql = MySQL()
hashids = Hashids(min_length=3)

app.config.update(
    DEBUG = True,
    MYSQL_USER = 'root',
    MYSQL_PASSWORD = '',
    MYSQL_DB = 'urlshort',
    MYSQL_HOST = 'localhost'
)

mysql.init_app(app)

def validateUrl(url):
	"""
		Checks if the given input is URL
		using Regular Expressions
		Returns True When:
			http://google.com
			http://www.google.com
			http://developers.google.com
		Returns False when:
			www.google.com
			google.com
			developers.google.com
	"""
	regex = r'^(http:\/\/www\.|https:\/\/www\.|'\
			r'http:\/\/|https:\/\/)[a-z0-9]+([\-'\
			r'\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]'\
			r'{1,5})?(\/.*)?$'

	if match(regex, url):
		return True
	else:
		return False

def shortenUrl(url):
	"""
		Checks if the given url already
		exists in the table.
		If it does then returns the `id` of the
		row.
		Else, inserts the URL in the table and
		returns the new `id`.
		`id` is the primary key and auto incerement
		value for each ow.
	"""
	cursor = mysql.connection.cursor()
	try:
		cursor.execute(
			"""SELECT id FROM urls WHERE long_url=(%s)""", [url]
			)
		plain_id = cursor.fetchone()[0]
		return str(plain_id)
	except:
		cursor.execute(
			"""INSERT INTO urls VALUES (%s,%s,%s)""",('',url,'')
			)
		mysql.connection.commit()
		return str(cursor.lastrowid)


@app.route('/')
def index():
	"""
		Home Page
	"""
	return render_template('index.html')

@app.route('/urlShortener', methods=['POST'])
def urlShortener():
	"""
		strips and encodes the URL.
		if the url is validate then
		returns the encoded `id` in
		json format.
	"""
	originalUrl =  request.form['originalUrl'].strip()
	originalUrl = url_fix(originalUrl)
	if validateUrl(originalUrl):
		return json.dumps({
			'status': 'OK',
			'message': hashids.encode(int(shortenUrl(originalUrl)))
			})
	else:
		return json.dumps({
			'status': 'ERROR',
			'message': 'This URL is Not Valid'
			})


@app.route('/<short_url>')
def redirectToLongUrl(short_url):
	"""
		Checks if the decoded `short_url`
		is valid and exists is the database.
		If does then increase `hits` by 1
		and redirect to the original URL.
	"""
	plain_id = hashids.decode(short_url)
	if len(plain_id) != 1:
		return abort(404)
	plain_id = str(plain_id[0])
	cursor = mysql.connection.cursor()
	try:
		cursor.execute(
			"""SELECT long_url FROM urls WHERE id=(%s)""", [plain_id]
			)
		url = cursor.fetchone()[0]
		cursor.execute(
			"""UPDATE urls SET hits = hits+1 WHERE id = %s""", [plain_id]
		)
		mysql.connection.commit()
		return redirect(url, code=302)
	except Exception as e:
		# return str(e)
		return abort(404)

if __name__ == '__main__':
	app.run()