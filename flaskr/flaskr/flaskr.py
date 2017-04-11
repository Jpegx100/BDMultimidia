import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from werkzeug import secure_filename
from base64 import b64encode

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'flaskr.db'),
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORK='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
	"""Connects to the specific database."""
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

@app.cli.command('initdb')
def initdb_command():
	init_db()
	print('Initialized the database.')

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

@app.route('/')
def show_entries():
	db = get_db()
	cur = db.execute('select id, nome, metadados, imagem from imagens order by id desc')
	entries = cur.fetchall()
	
	dictrows = [dict(row) for row in entries]
	for r in dictrows:
		img = str(b64encode(r['imagem']))
		r['imagem'] = img[2:-3]

	return render_template('show_imagens.html', entries=dictrows)


@app.route('/add', methods=['POST'])
def add_entry():
	imagem = request.files['imagem'].read()
	db = get_db()
	db.execute('insert into imagens (nome, metadados, imagem) values (?, ?, ?)',[request.form['nome'], request.form['metadados'], imagem])
	db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

