#include "{{ cls.name|lower }}.h"

{{ cls.name }}::{{ cls.name }}({{ cls.base }} *parent)
    : {{ cls.base }}(parent)
{

}
{% for prop in cls.props %}{% if prop.read %}

{{ prop.type }} {{ cls.name }}::{{ prop.name }}() const
{
    return m_{{ prop.name }};
}
{% endif %}{% if prop.write %}

void {{ cls.name }}::set{{ prop.name|firstUpper }}(const {{ prop.type }} &{{ prop.name }})
{
    if (m_{{ prop.name }} != {{ prop.name }}) {
        m_{{ prop.name }} = {{ prop.name }};
{% if prop.notify %}
        emit {{ prop.name }}Changed();
{% endif %}
    }
}
{% endif %}{% endfor -%}
