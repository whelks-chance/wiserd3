from django.db import router

__author__ = 'ubuntu'


class QualRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):

        """
        Attempts to read auth models go to auth_db.
        """
        print model._meta.app_label

        # if model._meta.app_label == 'old':
        #     return False
        if model._meta.app_label == 'old_qual':
            print 'returning qual_gis db for read'
            return 'qual_gis'
        return False

    def db_for_write(self, model, **hints):

        """
        Attempts to write auth models go to auth_db.
        """
        print model._meta.app_label

        if model._meta.app_label == 'old_qual':
            print 'returning qual_gis db for write'

            return 'qual_gis'
        return False

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """

        if obj1._meta.app_label == 'old_qual' or obj2._meta.app_label == 'old_qual':
            return True

        return None

    def allow_migrate(self, db, app_label, model=None, **hints):

        # """
        # Make sure the auth app only appears in the 'auth_db'
        # database.
        # """
        # if app_label == 'dataportal3' or app_label == 'sites' or app_label == 'contenttypes':
        #     print 'using this db'
        #     return db == 'new'


        if app_label == 'old_qual':
            return 'qual_gis'
        else:
            return None