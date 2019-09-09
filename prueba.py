from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QApplication, QGraphicsLineItem
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPen, QColor
import sys


class Paint(QGraphicsView):
    def __init__(self, parent=None):
        super(Paint, self).__init__()
        self.parent = parent
        self.rect_f = QRectF(self.viewport().rect())
        self.setSceneRect(self.rect_f)
        self.scene = QGraphicsScene()
        self.paint_line()

    def paint_line(self):
        item = self.scene.addLine(0, 0, 100, 100)
        item.setSelected(True)
        self.scene.addItem(item)
        self.setScene(self.scene)

    def mousePressEvent(self, event):
        for i in self.scene.items():
            i.setSelected(False)
            i.setPen(QPen(QColor('black')))
        e = event.pos()
        area_selection = QRectF(e.x()-2, e.y()-2, 4, 4)
        items = self.scene.items(area_selection)
        if items:
            items[0].setSelected(True)
            for i in items:
                if i.isSelected:
                    pen = QPen()
                    pen.setColor(QColor('red'))
                    pen.setWidth(2)
                    pen.setStyle(Qt.DotLine)
                    i.setPen(pen)

                else:
                    i.setPen(QPen(QColor('black')))


app = QApplication(sys.argv)
win = Paint()
win.show()
app.exec_()