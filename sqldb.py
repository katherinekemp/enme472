#import sqlite3

def create_db(file_name):
    db = sqlite3.connect(file_name)
    c = db.cursor()
    c.execute('drop table if exists data ')
    c.execute('drop table if exists last_run ')
    c.execute('create table data (run integer, time real, value real)')
    c.execute('create table last_run (run integer)')
    db.commit()
    return db


def save_data_sql(db, x_data, y_data):
    run_id = int(time.time())
    for i, x in enumerate(x_data):
        sql = 'insert into data (run, time, value) values (?,?,?)'
        db.execute(sql, (run_id, x, y_data[i]))
    c = db.cursor()
    c.execute('delete from last_run')
    c.execute('insert into last_run(run) values (?)', (run_id,))
    db.commit()

def get_sql_data():
    db = sqlite3.connect('katie.sql')
    c = db.execute(
        'select time,value from data join last_run where data.run=last_run.run'
    )
    x_data = []
    y_data = []
    for row in c:
        x_data.append(row[0])
        y_data.append(row[1])
xs    db.close()
    return x_data, y_data

if __name__ == 'main':
    create_db("katie_test")
    
