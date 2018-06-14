
#  Modified code to work with Django 1.9, and to add the --database option.

# Based on https://djangosnippets.org/snippets/10506/
# This intermediary version had the following header:

# Based on: https://djangosnippets.org/snippets/918/
# Altered to use: http://stackoverflow.com/questions/2233883/get-all-related-django-model-objects
# v0.1 -- current version
# Known issues:
# No support for generic relations

from optparse import make_option
from django.contrib.admin.utils import NestedObjects
from django.core import serializers
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management.base import LabelCommand
# from django.db.models.loading import get_models
from django.apps import apps
from django.db.utils import DEFAULT_DB_ALIAS

DEBUG = False


def model_name(m):
    module = m.__module__.split('.')[:-1]  # remove .models
    return ".".join(module + [m._meta.object_name])


class Command(LabelCommand):
    help = 'Output the contents of the database as a fixture of the given format.'
    args = 'modelname[pk] or modelname[id1:id2] repeated one or more times'
    option_list = BaseCommand.option_list + (
        make_option('--skip-related', default=True, action='store_false', dest='propagate',
                    help='Specifies if we shall not add related objects.'),
        make_option('--format', default='json', dest='format',
                    help='Specifies the output serialization format for fixtures.'),
        make_option('--indent', default=None, dest='indent', type='int',
                    help='Specifies the indent level to use when pretty-printing output'),
        make_option('--natural-foreign', default=False, action='store_true', dest='use_natural_foreign_keys',
                    help=''),
        make_option('--natural-primary', default=False, action='store_true', dest='use_natural_primary_keys',
                    help=''),
        make_option('--database', action='store', dest='database', default=DEFAULT_DB_ALIAS,
                    help='Nominates a specific database to dump fixtures from. Defaults to the "default" database.'),
        make_option('--filter', action='store', dest='filter', default=None,
                help='Standard filtering code in quotes, e.g. "field=\'abcdef\'" ')
    )

    @staticmethod
    def handle_models(models, **options):
        output_format = options.get('format', 'json')
        indent = options.get('indent', None)
        show_traceback = options.get('traceback', False)
        propagate = options.get('propagate', True)
        using = options.get('database')
        use_natural_foreign_keys = options.get('use_natural_foreign_keys', False)
        use_natural_primary_keys = options.get('use_natural_primary_keys', False)

        # Check that the serialization format exists; this is a shortcut to
        # avoid collating all the objects and _then_ failing.
        if output_format not in serializers.get_public_serializer_formats():
            raise CommandError("Unknown serialization format: %s" % output_format)

        try:
            serializers.get_serializer(output_format)
        except KeyError:
            raise CommandError("Unknown serialization format: %s" % output_format)

        objects = set()
        for model, model_slice in models:
            if isinstance(model_slice, basestring):
                objects.update(list(model._default_manager.using(using).filter(pk__exact=model_slice)))
            elif not model_slice or type(model_slice) is list:
                items = model._default_manager.using(using).all()
                if model_slice and model_slice[0]:
                    items = items.filter(pk__gte=model_slice[0])
                if model_slice and model_slice[1]:
                    items = items.filter(pk__lt=model_slice[1])
                items = items.order_by(model._meta.pk.attname)
                objects.update(list(items))
            else:
                raise CommandError("Wrong slice: %s" % model_slice)

        def flatten(container):
            for i in container:
                if isinstance(i, list) or isinstance(i, tuple):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if propagate:
            root_objects = list(objects)
            collector = NestedObjects(using='default')
            collector.collect(root_objects)

        return serializers.serialize(
            output_format,
            flatten(collector.nested()),
            indent=indent,
            use_natural_foreign_keys=use_natural_foreign_keys,
            use_natural_primary_keys=use_natural_primary_keys,
        )

    @staticmethod
    def get_models():
        return [(m, model_name(m)) for m in apps.get_models()]

    def handle_label(self, labels, **options):
        parsed = []
        for label in labels:
            search, pks = label, ''
            if '[' in label:
                search, pks = label.split('[', 1)
            model_slice = ''
            if ':' in pks:
                model_slice = pks.rstrip(']').split(':', 1)
            elif pks:
                model_slice = pks.rstrip(']')
            model_slice = model_slice if model_slice != '' else ['', '']
            models = [model for model, name in self.get_models()
                      if name.endswith('.' + search) or name == search]
            if not models:
                raise CommandError("Wrong model: %s" % search)
            if len(models) > 1:
                raise CommandError("Ambiguous model name: %s" % search)
            parsed.append((models[0], model_slice))
        return self.handle_models(parsed, **options)

    def list_models(self):
        names = [name for _model, name in self.get_models()]
        raise CommandError('Neither model name nor slice given. Installed model names: \n%s' % ",\n".join(names))

    def handle(self, *labels, **options):
        if not labels:
            self.list_models()

        output = []
        label_output = self.handle_label(labels, **options)
        if label_output:
            output.append(label_output)
        return '\n'.join(output)