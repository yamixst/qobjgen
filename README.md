# QObject Class Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A powerful code generator for Qt C++ classes that creates boilerplate code from simple declarative files.

## Overview

QObject Class Generator simplifies Qt development by generating C++ header and implementation files from lightweight `.qobj` definition files. Instead of writing repetitive boilerplate code for Qt properties, signals, and slots, you can define your classes declaratively and let QObject Class Generator handle the rest.

## Features

- 🚀 **Fast Development**: Generate complete Qt classes from simple definitions
- 📝 **Declarative Syntax**: Clean, readable `.qobj` file format
- 🎯 **Multiple Templates**: Support for QObject, QAbstractListModel, and QSettings-based classes
- 🔧 **Customizable**: Flexible template system using Jinja2

## Installation

### Prerequisites

- Python 3.6 or higher
- Jinja2 template engine

```bash
pip install jinja2
```

### Clone the Repository

```bash
git clone https://github.com/yourusername/qobjgen.git
cd qobjgen
```

## Quick Start

1. **Create a `.qobj` file** describing your Qt class:

```qobj
class Person
prop QString name RWN
prop int age RWN
prop QString email RWN
```

2. **Generate the C++ files**:

```bash
python qobjgen.py person.qobj -o output/
```

3. **Use the generated files** in your Qt project:
   - `person.qobj.h` - Header file with class declaration
   - `person.qobj.cpp` - Implementation file with getters, setters, and signals

## Usage

```bash
python qobjgen.py [OPTIONS] QOBJFILE [QOBJFILE ...]
```

### Options

| Option | Description |
|--------|-------------|
| `--tpldir TPLDIR` | Custom template directory |
| `--nosuffix` | Don't add `.qobj` suffix to output files |
| `--suffix SUFFIX` | Custom suffix for output files (default: `.qobj`) |
| `-f, --force` | Overwrite existing files |
| `-o OUTDIR` | Output directory for generated files |
| `-h, --help` | Show help message |

### Examples

```bash
# Generate files with default settings
python qobjgen.py examples/message.qobj

# Generate multiple files to specific directory
python qobjgen.py examples/*.qobj -o output/

# Use custom suffix and overwrite existing files
python qobjgen.py person.qobj --suffix .gen -f -o src/
```

## QObj File Format

### Basic Syntax

```qobj
# Comments start with #
class ClassName [BaseClass]
prop PropertyType propertyName [Access] [key1 value1 key2 value2 ...]
tpl templateName
var variableName value
```

### Class Definition

```qobj
class MyClass              # Inherits from QObject (default)
class MyClass QWidget      # Inherits from QWidget
```

### Properties

Properties support different access modes:

- `R` - Read-only (generates getter and signal)
- `W` - Write-only (generates setter)
- `N` - Notify (generates change signal)
- `RW` - Read-Write (default if not specified)
- `RWN` - Read-Write with notification

```qobj
prop int id R                    # Read-only
prop QString name RW             # Read-Write
prop bool enabled RWN            # Read-Write with notifications
prop double value W              # Write-only
```

### Templates

Choose different code generation templates:

```qobj
tpl qobject      # Standard QObject (default)
tpl listmodel    # QAbstractListModel subclass
tpl settings     # QSettings-based configuration class
```

### Variables

Define template variables for customization:

```qobj
var section main                 # For settings template
var namespace MyApp              # Custom namespace
```

## Examples

### Simple Data Model

```qobj
class Person
prop QString firstName RWN
prop QString lastName RWN
prop int age RWN
prop QString email RWN
```

Generates a Qt class with:
- Properties with getters, setters, and change signals
- Q_PROPERTY macros for QML integration
- Proper const-correctness

### Settings Class

```qobj
class AppSettings
tpl settings
var section main
prop bool debug R qvartype Bool default false
prop QString host qvartype String section network default "localhost"
prop QString username qvartype String section auth
prop QString password qvartype String section auth
```

Generates a QSettings-based configuration class with:
- Automatic loading/saving to settings file
- Section-based organization
- Default values
- Type-safe property access

### List Model

```qobj
class MessagesModel
tpl listmodel
prop QList<Message*> messages RWN
```

Generates a QAbstractListModel subclass for use with QML ListView.

## Template System

QObject Class Generator uses Jinja2 templates located in the `templates/` directory:

- `qobject_h.tpl` / `qobject_cpp.tpl` - Standard QObject classes
- `listmodel_h.tpl` / `listmodel_cpp.tpl` - List model classes
- `settings_h.tpl` / `settings_cpp.tpl` - Settings classes

### Custom Templates

You can create custom templates and use them with `--tpldir`:

```bash
python qobjgen.py myclass.qobj --tpldir /path/to/custom/templates/
```

## Generated Code Features

- **Qt Properties**: Full Q_PROPERTY declarations for QML binding
- **Getters/Setters**: Const-correct getters and type-safe setters
- **Signals**: Change notification signals for reactive programming
- **Memory Safe**: Proper RAII and Qt parent-child relationships
- **QML Ready**: Properties automatically exposed to QML

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
