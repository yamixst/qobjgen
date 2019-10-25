#include "settings.h"

Settings::Settings(QObject *parent)
    : QObject(parent)
{

}

bool Settings::debug() const
{
    return m_settings.value("main/debug", false).toBool();
}

void Settings::setDebug(const bool &debug)
{
    if (this->debug() != debug) {
        m_settings.setValue("main/debug", debug);
        emit debugChanged();
    }
}

QString Settings::host() const
{
    return m_settings.value("network/host", "localhost").toString();
}

void Settings::setHost(const QString &host)
{
    if (this->host() != host) {
        m_settings.setValue("network/host", host);
        emit hostChanged();
    }
}

QString Settings::username() const
{
    return m_settings.value("auth/username").toString();
}

void Settings::setUsername(const QString &username)
{
    if (this->username() != username) {
        m_settings.setValue("auth/username", username);
        emit usernameChanged();
    }
}

QString Settings::password() const
{
    return m_settings.value("auth/password").toString();
}

void Settings::setPassword(const QString &password)
{
    if (this->password() != password) {
        m_settings.setValue("auth/password", password);
        emit passwordChanged();
    }
}
