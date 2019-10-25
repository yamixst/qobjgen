#include "{{ cls.name|lower }}.h"

{{ cls.name }}::{{ cls.name }}({{ cls.base }} *parent)
    : {{ cls.base }}(parent)
{

}
{% for prop in cls.props %}

{{ prop.type }} {{ cls.name }}::{{ prop.name }}() const
{
    return m_{{ prop.name }};
}

void {{ cls.name }}::set{{ prop.name|firstUpper }}(const {{ prop.type }} &{{ prop.name }})
{
    if (m_{{ prop.name }} != {{ prop.name }}) {
        m_{{ prop.name }} = {{ prop.name }};
        emit {{ prop.name }}Changed();
    }
}
{% endfor -%}
