#/usr/bin/env python3

import psycopg2
from psycopg2.extensions import AsIs

def start():
	global conn
	global cur
	conn = psycopg2.connect(database='tencent',
                       		user='group01',
                        	password='To6tmwCB7bD07YpS',
                        	host='sustc.hguandl.com')

	print('Database connection ok')
	cur = conn.cursor()

def close():
	global conn
	conn.close()

def new_data(table, data):
	columns = ','.join(data.keys())
	values = ','.join([f"'{data[k]}'" for k in data])
	insert = f'INSERT INTO "{table}" ({columns}) VALUES ({values}) RETURNING id'
	cur.execute(insert, data)
	rows = cur.fetchall()
	if len(rows) <= 0:
		return -1
	else:
		return rows[0][0]

def find_id(table, data, key):
	cur.execute(f'SELECT id FROM "{table}" WHERE {key} = \'{data[key]}\'')
	rows = cur.fetchall()
	if len(rows) <= 0:
		return new_data(table, data)
	else:
		return (rows[0][0])

def add_record(commit_hash, author, func_sig, time, filename):
	commit_data = {'hash': commit_hash, 'time': time}
	commit_id = find_id('Commits', commit_data, 'hash')

	author_data = {'name': author}
	author_id = find_id('Authors', author_data, 'name')

	signature_data = {'signature': func_sig}
	signature_id = find_id('Signatures', signature_data, 'signature')

	file_data = {'file_path': filename}
	file_id = find_id('Files', file_data, 'file_path')

	cur.execute('INSERT INTO "Changes" \
				 (commit_id, author_id, signature_id, file_id) VALUES ' +
			   f'({commit_id}, {author_id}, {signature_id}, {file_id})')

	conn.commit()
