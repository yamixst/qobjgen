#!/usr/bin/python3

import sys
import os
import re
import jinja2

app_dir = os.path.dirname(__file__)
templates_dir = os.path.join(app_dir, 'templates')

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(templates_dir)
)

env.trim_blocks = True


def firstLower(s):
    return s[0].lower() + s[1:]


def firstUpper(s):
    return s[0].upper() + s[1:]


env.filters['firstLower'] = firstLower
env.filters['firstUpper'] = firstUpper


class QObjectProperty:

    def __init__(self, type, name, access='RWN', vars={}):
        self.type = type
        self.name = name
        self.read = access.upper().find('R') != -1
        self.write = access.upper().find('W') != -1
        self.notify = access.upper().find('N') != -1
        self.vars = vars

        print(self.__dict__)


class QObjectClass:

    def __init__(self):
        self.tpl = 'qobject'
        self.name = self.__class__.__name__
        self.base = 'QObject'
        self.props = [] # [QObjectProperty,]
        self.vars = {}

    def load(self, qobj_path):

        with open(qobj_path, 'r') as qobj_file:
            for line, text in enumerate(qobj_file):
                line += 1
                text = text.strip()

                if text == '' or text.startswith('#'): continue

                words = text.split()
                cmd = words[0].lower()
                args = words[1:]
                
                if len(args) < 1:
                    print('Error: Too few arguments in a line {0}: {1}'.format(line, text))
                    continue

                if cmd == 'class':
                    self.name = args[0]

                    if len(args) > 1:
                        self.base = args[1]

                    if len(args) > 2:
                        print('Warring: Too many arguments in a line {0}: {1}'.format(line, text))

                elif cmd == 'tpl' or cmd == 'template':
                    self.tpl = args[0]

                elif cmd == 'var':
                    if len(args) < 2:
                        print('Error: Too few arguments in a line {0}: {1}'.format(line, text))
                        continue

                    self.vars[args[0]] = text.split(maxsplit=2)[2]

                elif cmd == 'prop' or cmd == 'property':

                    if len(args) < 2:
                        print('Error: Too few arguments in a line {0}: {1}'.format(line, text))
                        continue

                    vars = {}

                    if len(args) > 2 and re.match(r'.*[^RWN]', args[2].upper()):
                        args.insert(2, 'RWN')

                    if len(args) > 2 and not len(args) % 2:
                        print('Warring: Wrong number of arguments in a line {0}: {1}'.format(line, text))

                    if len(args) > 3:
                        flatvars = args[3:]
                        vars = dict(zip(flatvars[::2], flatvars[1::2]))

                    self.props.append(QObjectProperty(*args[:3], vars=vars))

                else:
                    print('Error: Unknown instruction on line {0}: {1}'.format(line, text))

class Message:

    tpl = 'qobject'
    name = 'Message'
    base = 'QObject'
    props = [
        QObjectProperty('int', 'id', 'RWN'),
        QObjectProperty('QString', 'text', 'RWN'),
    ]


def jinja_generate(tpl_path, context, out_path):
    template = env.get_template(tpl_path)
    content = template.render(context)
    with open(out_path, 'w') as file:
        file.write(content)


def qobjgen(qobj_path, out_dir):
    qobjcls = QObjectClass()

    qobjcls.load(qobj_path)

    jinja_generate(qobjcls.tpl + '_h.tpl',   {'cls': qobjcls}, os.path.join(out_dir, qobjcls.name.lower() + '.qobj.h'))
    jinja_generate(qobjcls.tpl + '_cpp.tpl', {'cls': qobjcls}, os.path.join(out_dir, qobjcls.name.lower() + '.qobj.cpp'))


if __name__ == "__main__":
    
    if not 1 < len(sys.argv) < 4:
        print("Using: qobjgen QOBJFILE [OUTDIR]")
        sys.exit(1)

    qobj_path = sys.argv[1]

    if not os.path.isfile(qobj_path):
        print('Error: File "{0}" not exists'.format(qobj_path))
        sys.exit(2)
    
    if len(sys.argv) == 3:
        out_dir = sys.argv[2]
    else:
        out_dir = os.path.dirname(qobj_path)

    if not os.path.isdir(out_dir):
        print('Error: Directory "{0}" not exists'.format(out_dir))
        sys.exit(3)

    qobjgen(qobj_path, out_dir)
