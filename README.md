Simple boilerplate flask app, to test flask sessions with SQLAlhemy binds

```
$ docker-compose build --parallel
$ docker-compose up
```

env variables in .env file

Flask app -> http://127.0.0.1/

- index (/) route tries to set session key/value pair
- /get_session route display current session value if set

PostgreSQL adminer (easy database verify - creation and operations) -> http://127.0.0.1:8081/

PosgreSQL has a seed.sh script to initialize database for 1st time + to add 3 databases (db1, db2 and db3), it's called from Dockerfile.

Issue with db instance being called twice, via flask_session/sessions.py, trying to initialize db, twice:

```flask_app | [2024-03-03 19:34:51 +0000] [10] [ERROR] Exception in worker process
flask_app | Traceback (most recent call last):
flask_app | File "/usr/local/lib/python3.11/site-packages/gunicorn/arbiter.py", line 609, in spawn_worker
flask_app | worker.init_process()
flask_app | File "/usr/local/lib/python3.11/site-packages/gunicorn/workers/gthread.py", line 95, in init_process
flask_app | super().init_process()
flask_app | File "/usr/local/lib/python3.11/site-packages/gunicorn/workers/base.py", line 134, in init_process
flask_app | self.load_wsgi()
flask_app | File "/usr/local/lib/python3.11/site-packages/gunicorn/workers/base.py", line 146, in load_wsgi
flask_app | self.wsgi = self.app.wsgi()
flask_app | ^^^^^^^^^^^^^^^
flask_app | File "/usr/local/lib/python3.11/site-packages/gunicorn/app/base.py", line 67, in wsgi
flask_app | self.callable = self.load()
flask_app | ^^^^^^^^^^^
flask_app | File "/usr/local/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 58, in load
flask_app | return self.load_wsgiapp()
flask_app | ^^^^^^^^^^^^^^^^^^^
flask_app | File "/usr/local/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 48, in load_wsgiapp
flask_app | return util.import_app(self.app_uri)
flask_app | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
flask_app | File "/usr/local/lib/python3.11/site-packages/gunicorn/util.py", line 371, in import_app
flask_app | mod = importlib.import_module(module)
flask_app | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
flask_app | File "/usr/local/lib/python3.11/importlib/**init**.py", line 126, in import_module
flask_app | return \_bootstrap.\_gcd_import(name[level:], package, level)
flask_app | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
flask_app | File "<frozen importlib._bootstrap>", line 1204, in \_gcd_import
flask_app | File "<frozen importlib._bootstrap>", line 1176, in \_find_and_load
flask_app | File "<frozen importlib._bootstrap>", line 1147, in \_find_and_load_unlocked
flask_app | File "<frozen importlib._bootstrap>", line 690, in \_load_unlocked
flask_app | File "<frozen importlib._bootstrap_external>", line 940, in exec_module
flask_app | File "<frozen importlib._bootstrap>", line 241, in \_call_with_frames_removed
flask_app | File "/app/run.py", line 5, in <module>
flask_app | app = create_app()
flask_app | ^^^^^^^^^^^^
flask_app | File "/app/app/**init**.py", line 16, in create_app
flask_app | sess.init_app(app)
flask_app | File "/usr/local/lib/python3.11/site-packages/flask_session/**init**.py", line 55, in init_app
flask_app | app.session_interface = self.\_get_interface(app)
flask_app | ^^^^^^^^^^^^^^^^^^^^^^^^
flask_app | File "/usr/local/lib/python3.11/site-packages/flask_session/**init**.py", line 122, in \_get_interface
flask_app | session_interface = SqlAlchemySessionInterface(
flask_app | ^^^^^^^^^^^^^^^^^^^^^^^^^^^
flask_app | File "/usr/local/lib/python3.11/site-packages/flask_session/sessions.py", line 584, in **init**
flask_app | db = SQLAlchemy(app)
flask_app | ^^^^^^^^^^^^^^^
flask_app | File "/usr/local/lib/python3.11/site-packages/flask_sqlalchemy/extension.py", line 278, in **init**
flask_app | self.init_app(app)
flask_app | File "/usr/local/lib/python3.11/site-packages/flask_sqlalchemy/extension.py", line 312, in init_app
flask_app | raise RuntimeError(
flask_app | RuntimeError: A 'SQLAlchemy' instance has already been registered on this Flask app. Import and use that instance instead.
```

Issue with secret key, seems its related as when flask_session and Session() is removed, flask sessions working just fine:

```flask_app | [2024-03-03 18:51:18,379] ERROR in app: Exception on / [GET]
flask_app | Traceback (most recent call last):
flask_app | File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 1463, in wsgi_app
flask_app | response = self.full_dispatch_request()
flask_app | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
flask_app | File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 872, in full_dispatch_request
flask_app | rv = self.handle_user_exception(e)
flask_app | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
flask_app | File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 870, in full_dispatch_request
flask_app | rv = self.dispatch_request()
flask_app | ^^^^^^^^^^^^^^^^^^^^^^^
flask_app | File "/usr/local/lib/python3.11/site-packages/flask/app.py", line 855, in dispatch_request
flask_app | return self.ensure_sync(self.view_functions[rule.endpoint])(\*\*view_args) # type: ignore[no-any-return]
flask_app | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
flask_app | File "/app/app/guest/routes.py", line 20, in index
flask_app | session[key] = value
flask_app | ~~~~~~~^^^^^
flask_app | File "/usr/local/lib/python3.11/site-packages/flask/sessions.py", line 102, in \_fail
flask_app | raise RuntimeError(
flask_app | RuntimeError: The session is unavailable because no secret key was set. Set the secret_key on the application to something unique and secret.
```
