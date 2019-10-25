#ifndef MESSAGESMODEL_H
#define MESSAGESMODEL_H

#include <QAbstractListModel>

class MessagesModel : public QAbstractListModel
{
    Q_OBJECT

public:
    enum Roles {
        IdRole = Qt::UserRole,
        TextRole,
    };
    Q_ENUM(Roles)

    struct Item {
        int id;
        QString text;
    };

    explicit MessagesModel(QObject *parent = nullptr);

    const QList<Item> &items() const;
    void setItems(const QList<Item> &items);

    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    virtual QHash<int, QByteArray> roleNames() const override;

private:
    QList<Item> m_items;
};

#endif // MESSAGESMODEL_H