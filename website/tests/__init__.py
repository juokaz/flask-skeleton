from flask.ext.testing import TestCase
from ..admin import app, db

from sqlalchemy.schema import CreateTable

created = []


class TestCase(TestCase):
    transaction = None
    connection = None

    def create_app(self):
        app.config.from_object('website.settings.TestConfig')

        return app

    def setUp(self):
        # Borrowed from https://gist.github.com/alexmic/7857543
        connection = db.engine.connect()
        transaction = connection.begin()

        options = dict(bind=connection, binds={})
        session = db.create_scoped_session(options=options)

        db.session = session

        self.connection = connection
        self.transaction = transaction

        self._create()

    def tearDown(self):
        self.transaction.rollback()
        self.connection.close()
        db.session.remove()

    def _create(self):
        global created

        # create tables once per app
        # not sure why this is needed, I think because on each app creation
        # a new database gets created
        module = self.app.name
        if module in created:
            return

        create = []
        for table in db.metadata.tables.values():
            create.append(str(CreateTable(table)))

        for sql in create:
            db.engine.execute(sql)

        created.append(module)

    def assertRaisesWithMessage(self, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            assert False
        except Exception as inst:
            self.assertEqual(str(inst), msg)

    def _get(self, method_name, *args, **kwargs):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
                sess['_fresh'] = True
            method = getattr(self.client, method_name)
            response = method(*args, **kwargs)

        return response
