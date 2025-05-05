import QtQuick
import QtQuick.Controls


ApplicationWindow {


    width: 400
    height: 400
    visible: true
    title: qsTr("Hello World")

    Button {
        id: buttonp
        text: "A Special Button"
    }
}