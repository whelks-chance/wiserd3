import warnings


class raise_deprecation(object):
    def __init__(self, suggested_alternative):
        self.suggested_alternative = suggested_alternative

    def __call__(self, fn):
        def wrapper(*args, **kwargs):

            print "\nWarning:\n'%s'. The hand coded API is due to be deprecated, try using '%s'\n%s\n" % (
                    fn.__name__,
                    self.suggested_alternative, DeprecationWarning)

            warnings.warn(
                "'%s The hand coded API is due to be deprecated, try using '%s'" % (
                    fn.__name__,
                    self.suggested_alternative,
                ),
                DeprecationWarning, stacklevel=2
            )
            return fn(*args, **kwargs)
        return wrapper