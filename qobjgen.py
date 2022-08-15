#!/usr/bin/python3

import sys, os, re
import argparse
import jinja2


class QObjectProperty:

    def __init__(self, type, name, access='RWN', vars={}):
        self.type = type
        self.name = name
        self.read = access.upper().find('R') != -1
        self.write = access.upper().find('W') != -1
        self.notify = access.upper().find('N') != -1
        self.vars = vars


class QObjectClass:

    def __init__(self):
        self.tpl = 'qobject'
        self.name = 'Unknown'
        self.base = 'QObject'
        self.props = [] # [QObjectProperty,]
        self.vars = {}

    def load(self, qobj_path):
        self.name = os.path.splitext(os.path.basename(qobj_path))[0]

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


class QObjectGenerator:

    def __init__(self, tpl_dir=''):
        def firstLower(s):
            return s[0].lower() + s[1:]

        def firstUpper(s):
            return s[0].upper() + s[1:]

        if tpl_dir == '':
            app_dir = os.path.dirname(__file__)
            templates_dir = os.path.join(app_dir, 'templates')
        else:
            templates_dir = tpl_dir

        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))
        self.env.trim_blocks = True
        self.env.filters['firstLower'] = firstLower
        self.env.filters['firstUpper'] = firstUpper

    def _jinja_render(self, tpl_path, context, out_path):
        template = self.env.get_template(tpl_path)
        content = template.render(context)

        with open(out_path, 'w') as file:
            file.write(content)

        print('    Success {0}'.format(out_path))

    def generate(self, qobj_path, out_dir, suffix='.qobj', replace=True):
        qobjcls = QObjectClass()
        qobjcls.load(qobj_path)

        for ext in ('h', 'cpp'):
            out_path = os.path.join(out_dir, qobjcls.name.lower() + suffix + '.' + ext)
            if not replace and os.path.exists(out_path):
                print('Error: File already exists: ' + out_path)
            else:
                self._jinja_render(qobjcls.tpl + '_' + ext + '.tpl', {'cls': qobjcls}, out_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--tpldir", default='')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--nosuffix", action='store_true')
    group.add_argument("--suffix",  default='.qobj')
    parser.add_argument("-f", "--force", action='store_true')
    parser.add_argument("-o", "--outdir", default='')
    parser.add_argument("qobjfile", nargs="+")

    args = parser.parse_args()

    if not args.nosuffix:
        suffix = args.suffix
    else:
        suffix = ''

    out_dir = args.outdir

    qobjgen = QObjectGenerator(args.tpldir)

    for qobj_path in args.qobjfile:
        if not os.path.isfile(qobj_path):
            print('Error: File "{0}" not exists'.format(qobj_path))
            continue

        print('Proccessing {0}'.format(qobj_path))

        if out_dir == '':
            out_dir = os.path.dirname(qobj_path)

        if not os.path.isdir(out_dir):
            print('Error: Directory "{0}" not exists'.format(out_dir))
            sys.exit(1)
        
        qobjgen.generate(qobj_path, out_dir, suffix, args.force)
