#include "message.h"

Message::Message(QObject *parent)
    : QObject(parent)
{

}

int Message::id() const
{
    return m_id;
}

void Message::setId(const int &id)
{
    if (m_id != id) {
        m_id = id;
        emit idChanged();
    }
}

QString Message::text() const
{
    return m_text;
}

void Message::setText(const QString &text)
{
    if (m_text != text) {
        m_text = text;
        emit textChanged();
    }
}
