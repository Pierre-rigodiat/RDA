import urls
import re
from mgi.models import Exporter
from mongoengine.errors import ValidationError
from modules.exceptions import ModuleError
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern
from django.contrib.admindocs.views import simplify_regex
from exporter import get_exporter

def __assemble_endpoint_data__(pattern, prefix='', filter_path=None):
    """
    Creates a dictionary for matched API urls
    pattern -- the pattern to parse
    prefix -- the API path prefix (used by recursion)
    """
    path = simplify_regex(prefix + pattern.regex.pattern)

    if filter_path is not None:
        if re.match('^/?%s(/.*)?$' % re.escape(filter_path), path) is None:
            return None

    path = path.replace('<', '{').replace('>', '}')

    return {
        'url': path,
        'view': pattern._callback_str,
        'name': pattern.name,
    }


def __flatten_patterns_tree__(patterns, prefix='', filter_path=None):
    """
    Uses recursion to flatten url tree.
    patterns -- urlpatterns list
    prefix -- (optional) Prefix for URL pattern
    """
    pattern_list = []

    for pattern in patterns:
        if isinstance(pattern, RegexURLPattern):
            endpoint_data = __assemble_endpoint_data__(pattern, prefix, filter_path=filter_path)

            if endpoint_data is None:
                continue

            pattern_list.append(endpoint_data)

        elif isinstance(pattern, RegexURLResolver):

            pref = prefix + pattern.regex.pattern
            pattern_list.extend(__flatten_patterns_tree__(
                pattern.url_patterns,
                pref,
                filter_path=filter_path
            ))

    return pattern_list



def discover_exporter():
    patterns = __flatten_patterns_tree__(urls.urlpatterns)
    list_add_or_update_exporters = []

    try:
        for pattern in patterns:
            try:
                #We try to instanciate the exporter to be sure that it will worked. If not, just print an error in the python console
                instance = get_exporter(pattern['view'])
                Exporter.objects.filter(name=pattern['name']).update(set__url=pattern['view'], set__name=pattern['name'], upsert=True)
                list_add_or_update_exporters.append(pattern['name'])

            except Exception, e:
                print('ERROR : Impossible to load the following exporter, class not found : ' + pattern['view'])

        #If there is an old exporter, we delete it.
        list_exporters = Exporter.objects.all().values_list("name")
        list_to_delete = list(set(list_exporters) - set(list_add_or_update_exporters))
        if len(list_to_delete) > 0:
            Exporter.objects(name__in=list_to_delete).delete()

    except ValidationError as e:
        raise ModuleError('A validation error occured during the exporter discovery :'+ e._get_message())
    except Exception, e:
        raise e


