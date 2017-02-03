import hashlib


class TreeInfo:
    title = ""
    key = ""
    key_hash = ""
    selected = False

    def __init__(self, title, key="", key_hash=""):
        self.title = title
        self.key = key
        self.key_hash = key_hash

    def __str__(self):
        return self.title

    def __eq__(self, other):
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)

    def __lt__(self, other):
        return self.title < other.title

    def is_selected(self):
        return "true" if self.selected else ""


def build_tree(tree, root, enums, dot_query):
    for enum in enums:
        t = tree
        t = t.setdefault(TreeInfo(title=root), {})
        groups = enum.attrib['value'].split(':')
        split_index = 0
        for part in groups:
            split_index += 1
            key = "{0}=={1}".format(dot_query, ':'.join(groups[:split_index]))
            key_hash = hashlib.sha1(key).hexdigest()
            g = TreeInfo(title=part, key=key, key_hash=key_hash)
            t = t.setdefault(g, {})


    return tree


def print_tree(tree, nb_occurrences_text=False):
    display = "[\n"
    for key, leaves in tree.iteritems():
        display += _print_leaves(key, leaves, nb_occurrences_text)
    display += "]"
    return _remove_last_comma(display)


def _print_leaves(key, leaves, nb_occurrences_text=False):
    if nb_occurrences_text:
        display = "{{\"title\": \"{0} " \
                  "(<text id='{1}'>-</text>)\", " \
                  "\"selected\": \"{2}\", " \
                  "\"key\": \"{3}\"".format(key.title, key.key_hash, key.is_selected(), key.key)
    else:
        display = "{{\"title\": \"{0}\", " \
                  "\"selected\": \"{1}\", " \
                  "\"key\": \"{2}\"".format(key.title, key.is_selected(), key.key)
    if len(leaves) == 0:
        return display + "},"
    elif len(leaves) > 0:
        display += ", \"folder\": true, \"children\": ["
        display += '\n'
        for key, value in sorted(leaves.iteritems()):
            display += _print_leaves(key, value, nb_occurrences_text) + '\n'
        display = _remove_last_comma(display)+"]},\n"
        return display


def _remove_last_comma(s):
    return "".join(s.rsplit(",", 1))
