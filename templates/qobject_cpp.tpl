#include "{{ cls.name|lower }}.h"

{{ cls.name }}::{{ cls.name }}(QObject *parent)
    : {{ cls.base }}(parent)
{

}
{% for prop in cls.props %}{% if prop.read %}

{{ prop.type }} {{ cls.name }}::{{ prop.name }}() const
{
    return m_{{ prop.name }};
}
{% endif %}{% if prop.write %}

void {{ cls.name }}::set{{ prop.name|firstUpper }}({% if '*' not in prop.type %}const {% endif %}{{ prop.type }} {% if '*' in prop.type %}const {% endif %}&{{ prop.name }})
{
    if (m_{{ prop.name }} != {{ prop.name }}) {
        m_{{ prop.name }} = {{ prop.name }};
{% if prop.notify %}
        emit {{ prop.name }}Changed();
{% endif %}
    }
}
{% endif %}{% endfor -%}
