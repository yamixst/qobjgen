#ifndef {{ cls.name|upper }}_H
#define {{ cls.name|upper }}_H

#include <QAbstractListModel>

class {{ cls.name }} : public QAbstractListModel
{
    Q_OBJECT

public:
    enum Roles {
{% for prop in cls.props %}
        {{ prop.name|firstUpper }}Role{% if loop.index == 1 %} = Qt::UserRole{% endif %},
{% endfor %}
    };
    Q_ENUM(Roles)

    struct Item {
{% for prop in cls.props %}
        {{ prop.type }} {{ prop.name }};
{% endfor %}
    };

    explicit {{ cls.name }}(QObject *parent = nullptr);

    const QList<Item> &items() const;
    void setItems(const QList<Item> &items);

    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    virtual QHash<int, QByteArray> roleNames() const override;

private:
    QList<Item> m_items;
};

#endif // {{ cls.name|upper }}_H
