//
// Created by Micael Cossa on 05/05/2025.
//


#include <QHttpPart>
#include <QJsonDocument>
#include <QEventLoop>
#include "web_requests.h"




QNetworkReply* make_post_request(const QString& address, const QJsonObject& params) {

    QUrl url(address);

    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QByteArray jsonData = QJsonDocument(params).toJson(QJsonDocument::Compact);
    QEventLoop loop;
    QNetworkAccessManager manager;
    QNetworkReply* reply = manager.post(request, jsonData);
    QObject::connect(reply, &QNetworkReply::finished, &loop, &QEventLoop::quit);
    loop.exec();

    if (reply->error() == QNetworkReply::NoError)
        return reply;
    else {
        reply->deleteLater();
        return nullptr;
    }
}

