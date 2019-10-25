#ifndef SETTINGS_H
#define SETTINGS_H

#include <QtCore>

class Settings : public QObject
{
    Q_OBJECT

    Q_PROPERTY(bool debug READ debug)
    Q_PROPERTY(QString host READ host WRITE setHost NOTIFY hostChanged)
    Q_PROPERTY(QString username READ username WRITE setUsername NOTIFY usernameChanged)
    Q_PROPERTY(QString password READ password WRITE setPassword NOTIFY passwordChanged)

public:
    explicit Settings(QObject *parent = nullptr);

    bool debug() const;
    QString host() const;
    QString username() const;
    QString password() const;

signals:
    void debugChanged();
    void hostChanged();
    void usernameChanged();
    void passwordChanged();

public slots:
    void setDebug(const bool &debug);
    void setHost(const QString &host);
    void setUsername(const QString &username);
    void setPassword(const QString &password);
    
private:
    QSettings m_settings;
};

#endif // SETTINGS_H
