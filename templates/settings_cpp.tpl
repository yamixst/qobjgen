#include "{{ cls.name|lower }}.h"

{{ cls.name }}::{{ cls.name }}(QObject *parent)
    : {{ cls.base }}(parent)
{

}

void Settings::sync()
{
    m_settings.sync();
}

bool Settings::autoSync() const
{
    return m_autoSync;
}

void Settings::setAutoSync(bool autoSync)
{
    m_autoSync = autoSync;
}
{% for prop in cls.props %}
{% set section = prop.vars.section if 'section' in prop.vars else cls.vars.section if 'section' in cls.vars else '' %}
{% set key = prop.vars.key if 'key' in prop.vars else prop.name %}
{% set key = section + '/' + key if section else key %}

{{ prop.type }} {{ cls.name }}::{{ prop.name }}() const
{
    return m_settings.value("{{ key }}"{% if 'default' in prop.vars %}, {{ prop.vars.default }}{% endif %}).to{{ prop.vars.qvartype }}();
}

void {{ cls.name }}::set{{ prop.name|firstUpper }}(const {{ prop.type }} &{{ prop.name }})
{
    if (this->{{ prop.name }}() == {{ prop.name }})
        return;

    m_settings.setValue("{{ key }}", {{ prop.name }});
    
    if (autoSync()) 
        sync();
    
    emit {{ prop.name }}Changed();
}
{% endfor -%}
