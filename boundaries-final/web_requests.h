//
// Created by Micael Cossa on 05/05/2025.
//

#ifndef BOUNDARIES_FINAL_WEB_REQUESTS_H
#define BOUNDARIES_FINAL_WEB_REQUESTS_H


#include <QJsonObject>
#include <QNetworkReply>

QNetworkReply* make_post_request(const QString& address, const QJsonObject& params);
QNetworkReply* make_get_request(const QString& address);

#endif //BOUNDARIES_FINAL_WEB_REQUESTS_H
