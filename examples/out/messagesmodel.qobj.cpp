#include "messagesmodel.h"

MessagesModel::MessagesModel(QObject *parent)
    : QAbstractListModel(parent)
{
}

const QList<MessagesModel::Item> &MessagesModel::items() const
{
    return m_items;
}

void MessagesModel::setItems(const QList<MessagesModel::Item> &items)
{
    beginResetModel();

    m_items = items;

    endResetModel();
}

int MessagesModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid())
        return 0;

    return m_items.count();
}

QVariant MessagesModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid())
        return {};

    int row = index.row();

    if (row > m_items.count())
        return {};

    switch (role) {
    case IdRole:
        return m_items.at(row).id;
    case TextRole:
        return m_items.at(row).text;
    }

    return {};
}

QHash<int, QByteArray> MessagesModel::roleNames() const
{
    static QHash<int, QByteArray> roleNames {
        {IdRole, "id"},
        {TextRole, "text"},
    };

    return roleNames;
}