#ifndef {{ cls.name|upper }}_H
#define {{ cls.name|upper }}_H

#include <QtCore>

class {{ cls.name }} : public {{ cls.base }}
{
    Q_OBJECT

{% for prop in cls.props %}
    Q_PROPERTY({{ prop.type }} {{ prop.name }}{% if prop.read %} READ {{ prop.name }}{% endif %}{% if prop.write %} WRITE set{{ prop.name|firstUpper }}{% endif %}{% if prop.notify %} NOTIFY {{ prop.name }}Changed{% endif %})
{% endfor %}

public:
    explicit {{ cls.name }}({{ cls.base }} *parent = nullptr);

{% for prop in cls.props %}{% if prop.read %}
    {{ prop.type }} {{ prop.name }}() const;
{% endif %}{% endfor %}

signals:
{% for prop in cls.props %}{% if prop.notify %}
    void {{ prop.name }}Changed();
{% endif %}{% endfor %}

public slots:
{% for prop in cls.props %}{% if prop.write %}
    void set{{ prop.name|firstUpper }}(const {{ prop.type }} &{{ prop.name }});
{% endif %}{% endfor %}

private:
{% for prop in cls.props %}
    {{ prop.type }} m_{{ prop.name }};
{% endfor %}
};

#endif // {{ cls.name|upper }}_H

