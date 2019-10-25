#include "{{ cls.name|lower }}.h"

{{ cls.name }}::{{ cls.name }}({{ cls.base }} *parent) : {{ cls.base }}(parent)
{

}
{% for prop in cls.props %}
{% set section = prop.vars.section if 'section' in prop.vars else cls.vars.section if 'section' in cls.vars else '' %}
{% set key = section + '/' + prop.name if section else prop.name %}

{{ prop.type }} {{ cls.name }}::{{ prop.name }}() const
{
    return m_settings.value("{{ key }}"{% if 'default' in prop.vars %}, {{ prop.vars.default }}{% endif %}).to{{ prop.vars.qvartype }}();
}

void {{ cls.name }}::set{{ prop.name|firstUpper }}(const {{ prop.type }} &{{ prop.name }})
{
    if (this->{{ prop.name }}() != {{ prop.name }}) {
        m_settings.setValue("{{ key }}", {{ prop.name }});
        emit {{ prop.name }}Changed();
    }
}
{% endfor -%}
