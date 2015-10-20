from django.db import router

__author__ = 'ubuntu'


class DBRouter(object):
    """
    A router to control all database operations on models in the
    auth application.


    READ ME!!!!!!

    This is basically the "default" router, so anything routes to the "new" database unless
    specifically directed not to.

    This differs from the other routers, which return False unless they specifically
    answer to that models app label

    """

    # TODO convert this to a list of ignored app labels to check in

    def db_for_read(self, model, **hints):

        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'old':
            return False

        if model._meta.app_label == 'old_qual':
            return False

        if model._meta.app_label == 'dataportal3':
            return 'new'
        return 'new'

    def db_for_write(self, model, **hints):

        """
        Attempts to write auth models go to auth_db.
        """

        if model._meta.app_label == 'old':
            return False

        if model._meta.app_label == 'old_qual':
            return False

        if model._meta.app_label == 'dataportal3':
            return 'new'
        return 'new'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """

        if obj1._meta.app_label == 'dataportal3' or obj2._meta.app_label == 'dataportal3':
            return True

        return None

    def allow_migrate(self, db, app_label, model=None, **hints):

        # try:
        #     print app_label, db, str(model._meta.__dict__['concrete_model'])
        # except Exception as e:
        #     print 'ex', e

        # """
        # Make sure the auth app only appears in the 'auth_db'
        # database.
        # """
        # if app_label == 'dataportal3' or app_label == 'sites' or app_label == 'contenttypes':
        #     print 'using this db'
        #     return db == 'new'

        if app_label == 'old':
            return None

        if app_label == 'old_qual':
            return None
        else:
            # if db == 'new':
            #     print app_label, db, str(model._meta.__dict__['concrete_model'])
            return db == 'new'
        return None
