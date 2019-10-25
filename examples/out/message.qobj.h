#ifndef MESSAGE_H
#define MESSAGE_H

#include <QtCore>

class Message : public QObject
{
    Q_OBJECT

    Q_PROPERTY(int id READ id NOTIFY idChanged)
    Q_PROPERTY(QString text READ text WRITE setText NOTIFY textChanged)

public:
    explicit Message(QObject *parent = nullptr);

    int id() const;
    QString text() const;

signals:
    void idChanged();
    void textChanged();

public slots:
    void setId(const int &id);
    void setText(const QString &text);
    
private:
    int m_id;
    QString m_text;
};

#endif // MESSAGE_H
