#/usr/bin/env python3

import psycopg2

conn = psycopg2.connect(database='tencent',
                        user='group01',
                        password='To6tmwCB7bD07YpS',
                        host='sustc.hguandl.com')

print('Database connection ok')
