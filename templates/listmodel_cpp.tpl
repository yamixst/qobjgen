#include "{{ cls.name|lower }}.h"

{{ cls.name }}::{{ cls.name }}(QObject *parent)
    : QAbstractListModel(parent)
{
}

const QList<{{ cls.name }}::Item> &{{ cls.name }}::items() const
{
    return m_items;
}

void {{ cls.name }}::setItems(const QList<{{ cls.name }}::Item> &items)
{
    beginResetModel();

    m_items = items;

    endResetModel();
}

int {{ cls.name }}::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid())
        return 0;

    return m_items.count();
}

QVariant {{ cls.name }}::data(const QModelIndex &index, int role) const
{
    if (!index.isValid())
        return {};

    int row = index.row();

    if (row > m_items.count())
        return {};

    switch (role) {
{% for prop in cls.props %}
    case {{ prop.name|firstUpper }}Role:
        return m_items.at(row).{{ prop.name }};
{% endfor %}
    }

    return {};
}

QHash<int, QByteArray> {{ cls.name }}::roleNames() const
{
    static QHash<int, QByteArray> roleNames {
{% for prop in cls.props %}
        { {{- prop.name|firstUpper }}Role, "{{ prop.name }}"},
{% endfor %}
    };

    return roleNames;
}
