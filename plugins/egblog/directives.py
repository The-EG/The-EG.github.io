from docutils import nodes
from docutils.parsers.rst import directives, Directive

from pelican import signals

class BaseAlert(Directive):
    bootstrap_classes = []
    final_argument_whitespace = True
    has_content = True

    node_class = None

    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        admonition_node = self.node_class(text, **self.options)
        admonition_node.source, admonition_node.line = \
            self.state_machine.get_source_and_line(self.lineno)
        self.state.nested_parse(self.content, self.content_offset,
                                admonition_node)
        admonition_node['classes'] += self.bootstrap_classes
        return [admonition_node]
        
class Note(BaseAlert):
    bootstrap_classes = ['alert', 'alert-primary']
    node_class = nodes.container

class Warning(BaseAlert):
    bootstrap_classes = ['alert', 'alert-warning']
    node_class = nodes.container

class Info(BaseAlert):
    bootstrap_classes = ['alert', 'alert-info']
    node_class = nodes.container


def register():
    directives.register_directive('note', Note)
    directives.register_directive('warning', Warning)
    directives.register_directive('info', Info)
