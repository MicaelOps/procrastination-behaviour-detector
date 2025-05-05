import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts


ApplicationWindow {

    id: root
    width: 640
    height: 480
    visible: true
    title: qsTr("Boundaries Productivity Tool")


    maximumWidth: 1000
    maximumHeight: 900


    color: "lightgray"
    ColumnLayout {

        id: layout
        anchors.fill: parent
        spacing: 1

        Pane {


            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 300
            Layout.preferredHeight: 300


            background: Rectangle  {

                border.color: "gray"
                border.width: 1
            }

            ColumnLayout {
                anchors.fill: parent
                spacing: 10
                Label {
                    text: "Welcome, please authenticate."
                }
                TextArea {
                    placeholderText: "Username"
                    Layout.fillWidth: true
                    background: Rectangle {
                        border.color: "gray"
                        border.width: 1
                        radius: 4
                    }
                }
                TextArea {
                    Layout.fillWidth: true
                    placeholderText: "Password"
                    background: Rectangle {
                        border.color: "gray"
                        border.width: 1
                        radius: 4
                    }

                }
                Button {

                    Layout.fillWidth: true

                    contentItem: Text {
                        text: "Enter"
                        color: "white"
                        horizontalAlignment: Text.AlignHCenter
                    }
                    background: Rectangle {
                        color: "black"
                        radius: 4
                    }
                }
                Label {
                    Layout.alignment: Qt.AlignHCenter
                    text: "Don't have an account? Click here."
                    font.bold: true
                    font.underline: true
                }
            }
        }
    }

}