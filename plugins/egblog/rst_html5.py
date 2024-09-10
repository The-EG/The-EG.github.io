from docutils.writers.html5_polyglot import HTMLTranslator, Writer
from docutils import nodes

from pelican import signals

class Html5Writer(Writer):
    def __init__(self):
        super().__init__()
        self.translator_class = Html5Translator

class Html5Translator(HTMLTranslator):
    def visit_abbreviation(self, node):
        attrs = {}
        if node.hasattr("explanation"):
            attrs["title"] = node["explanation"]
        self.body.append(self.starttag(node, "abbr", "", **attrs))

    def depart_abbreviation(self, node):
        self.body.append("</abbr>")

    def visit_image(self, node):
        # set an empty alt if alt is not specified
        # avoids that alt is taken from src
        node["alt"] = node.get("alt", "")
        return HTMLTranslator.visit_image(self, node)
    
    # from html4css1
    def should_be_compact_paragraph(self, node):
        """
        Determine if the <p> tags around paragraph ``node`` can be omitted.
        """
        if (isinstance(node.parent, nodes.document)
            or isinstance(node.parent, nodes.compound)):
            # Never compact paragraphs in document or compound.
            return False
        for key, value in node.attlist():
            if (node.is_not_default(key)
                and not (key == 'classes'
                         and value in ([], ['first'],
                                       ['last'], ['first', 'last']))):
                # Attribute which needs to survive.
                return False
        first = isinstance(node.parent[0], nodes.label)  # skip label
        for child in node.parent.children[first:]:
            # only first paragraph can be compact
            if isinstance(child, nodes.Invisible):
                continue
            if child is node:
                break
            return False
        parent_length = len([n for n in node.parent if not isinstance(
            n, (nodes.Invisible, nodes.label))])
        if (self.compact_simple
            or self.compact_field_list
            or self.compact_p and parent_length == 1):
            return True
        return False

    def visit_paragraph(self, node):
        if self.should_be_compact_paragraph(node):
            self.context.append('')
        else:
            self.body.append(self.starttag(node, 'p', ''))
            self.context.append('</p>\n')

    def depart_paragraph(self, node):
        self.body.append(self.context.pop())

    # bootstrap classes
    def visit_table(self, node):
        atts = {'classes': self.settings.table_style.replace(',', ' ').split()}
        if 'align' in node:
            atts['classes'].append('align-%s' % node['align'])
        if 'width' in node:
            atts['style'] = 'width: %s;' % node['width']
        atts['classes'].append('table')
        #atts['classes'].append('table-striped')
        tag = self.starttag(node, 'table', **atts)
        self.body.append(tag)

    def depart_table(self, node):
        self.body.append('</table>\n')

    def visit_figure(self, node):
        atts = {}
        atts = {'classes': []}
        if node.get('width'):
            atts['style'] = f"width: {node['width']}"
        if node.get('align'):
            atts['classes'].append(f"align-{node['align']}")
        atts['classes'].append('figure')
        self.body.append(self.starttag(node, 'figure', **atts))

    def depart_figure(self, node):
        if len(node) > 1:
            self.body.append('</figcaption>\n')
        self.body.append('</figure>\n')

    def visit_caption(self, node):
        if isinstance(node.parent, nodes.figure):
            self.body.append('<figcaption class="figure-caption">\n')
        self.body.append(self.starttag(node, 'p', ''))

    def depart_caption(self, node):
        self.body.append('</p>\n')
        # <figcaption> is closed in depart_figure(), as legend may follow.

    def visit_container(self, node):
        self.body.append(self.starttag(node, 'div',
                                       CLASS=''))

    def depart_container(self, node):
        self.body.append('</div>\n')

    def visit_admonition(self, node):
        self.body.append(self.starttag(node, 'div', classes=['admonition','alert','alert-primary']))

    def depart_admonition(self, node):
        self.body.append('</div>')

def add_reader(readers):
    readers.reader_classes['rst'].writer_class = Html5Writer

def register():
    signals.readers_init.connect(add_reader)
