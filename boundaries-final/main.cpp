#include <QGuiApplication>
#include <QDebug>
#include <QQmlApplicationEngine>
#include <QJsonDocument>
#include "web_requests.h"


int main(int argc, char *argv[]) {


    QGuiApplication app(argc, argv);
    qDebug() << "Hello World";


    QGuiApplication::setOrganizationName("Boundaries");
    QGuiApplication::setOrganizationDomain("boundaries.com");
    QGuiApplication::setApplicationName("Boundaries");


    QQmlApplicationEngine engine;

    QObject::connect(
            &engine,
            &QQmlApplicationEngine::objectCreationFailed,
            &app,
            []() { QCoreApplication::exit(-1); },
            Qt::QueuedConnection);

    engine.loadFromModule("resources", "MainWindow");


    qDebug() << "Making request.. ";

    QString jsonString = R"(
    {
        "mouse_clicks": 10,
        "timestamp": "2025-04-18 17:28:39",
        "keys_pressed": 31,
        "mouse_travel": 30,
        "feedback_response": 1,
        "tabs_changed": 3,
        "app_focus_type": 3
        }
    )";

    QJsonDocument jsonDoc = QJsonDocument::fromJson(jsonString.toUtf8());
    QJsonObject jsonObject = jsonDoc.object();
    QNetworkReply* reply = make_post_request("http://127.0.0.1:5000/predict", jsonObject);

    if(reply != nullptr) {
        reply->deleteLater();
    }

    return QGuiApplication::exec();
}


void sendPopupNotification() {

}