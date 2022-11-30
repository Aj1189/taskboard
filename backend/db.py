import sqlite3
from flask import g
import os.path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('db')

database_path = 'task-board-db.sqlite'


def use_db(file_path):
    global database_path
    database_path = file_path


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def create_connection():
    db = sqlite3.connect(
        database_path,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = dict_factory
    db.set_trace_callback(logger.info)
    return db


def get_db():
    print('Database instance requested.')
    if 'db' not in g:
        g.db = create_connection()

    return g.db


def init_db():
    """
    Create db if not already present
    :return:
    """
    print('Initializing database...')
    if not os.path.exists(database_path):
        db = create_connection()
        with open('schema.sql') as f:
            print('Executing schema...')
            db.executescript(f.read())
    else:
        print('Database is already present. Skipping.')


init_db()


class Tasker:

    def create(self, title, description, status="todo"):
        logger.info('Create Request: ')
        with create_connection() as db:
            max_index_present = db.execute('select max(id) as max_after_id from tasks where status = "todo"') \
                .fetchone().get('max_after_id', 0)
            index_for_this_task = max_index_present if max_index_present is not None else 0
            res = db.execute(
                'insert into tasks(title, status, description, after_id) values(?, ? ,?, ?) returning *',
                (title, status, description, index_for_this_task))
            task = res.fetchone()
            return dict(task)

    def edit(self, id, title, description):
        with create_connection() as db:
            db.execute('update tasks set title = ?, description = ? where id = ?',
                       (title, description, id))

    def move(self, id, to_status, after_id):
        task = self.get_one(id)

        # if you want to move
        with create_connection() as db:
            # remove space from where it was
            db.execute('update tasks set after_id = after_id - 1 where after_id > ? and status = ?',
                       (task['after_id'], task['status']))

            # make space where it want to go
            db.execute('update tasks set after_id = after_id + 1 where after_id >= ? and status = ?',
                       (after_id, to_status))

            # update the task itself
            db.execute('update tasks set after_id = ?, status = ? where id = ?', (after_id, to_status, id))

        return self.get_one(id)

    def delete(self, id):
        # this is a clean delete
        # when we delete something, we also make sure that the after_id are consistent (consistent = incrementing by 1
        # without any gaps in them
        #
        # therefore, while deleting, we have to subtract 1 from all after_ids which are greater than the current one
        # in the given status
        task = self.get_one(id)

        if not task:
            raise ValueError('Task with id not found')

        assert task['after_id'] is not None
        assert task['status'] is not None

        with create_connection() as db:
            db.execute('delete from tasks where id = ?', (id,))
            db.execute('update tasks set after_id = after_id - 1 where after_id > ? and status = ?',
                       (task['after_id'], task['status']))

    def get(self):
        with create_connection() as db:
            res = list(db.execute("select * from tasks order by after_id"))
            return [dict(r) for r in res]

    def get_one(self, task_id):
        with create_connection() as db:
            res = db.execute("select * from tasks where id = ?", (task_id,))
            task = res.fetchone()
            if task:
                return dict(task)
            else:
                return None
