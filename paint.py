#from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPen, QColor, QBrush, QPixmap, QPainter, QPolygonF
from WaterHID import Node, Reservoir, Pipe
from SecondWins import show_text_default


def polygon_bomb(line):
    a = 4
    c = line.line()
    long = ((c.x2() - c.x1()) ** 2 + (c.y2() - c.y1()) ** 2) ** .5
    c_a = (c.x2() - c.x1()) / long
    s_a = (-c.y2() + c.y1()) / long
    c_45 = s_45 = .7071067811865475
    c_a_2 = c_45*c_a - s_45*s_a
    s_a_2 = s_45*c_a + c_45*s_a
    c_a_3 = c_45*c_a + s_45*s_a
    s_a_3 = s_45*c_a - c_45*s_a
    c_x = c.x1() + (c.x2() - c.x1()) / 5
    c_y = c.y1() + (c.y2() - c.y1()) / 5
    p_1 = QPointF(c_x - 2*a*c_a, c_y+2*a*s_a)
    p_2 = QPointF(p_1.x()+a*c_a_2/c_45, p_1.y()-a*s_a_2/c_45)
    p_3 = QPointF(p_2.x()+3*a*c_a, p_2.y()-3*a*s_a)
    p_4 = QPointF(c_x + 2*a*c_a, c_y-2*a*s_a)
    p_5 = QPointF(c_x + a*c_a, c_y-a*s_a)
    p_6 = QPointF(p_5.x()+a*s_a, p_5.y()+a*c_a)
    p_9 = QPointF(p_1.x()+a*s_a, p_1.y()+a*c_a)
    p_8 = QPointF(p_9.x()+a*c_a_3/c_45, p_9.y()+a*s_a_3/c_45)
    p_7 = QPointF(p_8.x()+a*c_a, p_8.y()-a*s_a)
    c_bomb = QPolygonF([p_1, p_2, p_3, p_4, p_5, p_6, p_7, p_8, p_9])
    return c_bomb


def paint_node(self, is_node, c_e):
    if is_node:  # paint node
        return self.paint_node(c_e)
    else:
        return self.current_item


def paint_reservoir(self, c_e):
    if self.is_reservoir:
        return self.paint_reservoir(c_e)
    else:
        return self.current_item


def paint_pipe(self, c_e, is_pipe, l_i_nodes, cond_pipe, union_pipe, items, l_nodes):
    if is_pipe:
        if not cond_pipe:
            l_p = l_nodes + self.l_reservoir
            l_p_2 = l_i_nodes + self.l_i_reservoir
            node = l_p[l_p_2.index(items[0])]
            c_e.setX(node.x)
            c_e.setY(node.y)
            e_f = QPointF(c_e.x()+1, c_e.y()+1)
            item = self.scene_v.addLine(c_e.x(), c_e.y(), e_f.x(), e_f.y(), QPen(QColor('black')))
            union_pipe[0] = node
            return True, c_e, item, union_pipe
        else:
            self.scene_v.removeItem(self.current_item)
            l_p = l_nodes + self.l_reservoir
            l_p_2 = l_i_nodes + self.l_i_reservoir
            node = l_p[l_p_2.index(items[0])]
            e_f = QPointF()
            e_f.setX(node.x)
            e_f.setY(node.y)
            n_i = union_pipe[0]
            union_pipe[1] = node
            item = self.paint_pipe(self.start_e, e_f, n_i, node)
            return False, None, item, union_pipe

    else:
        return False, None, self.current_item, [None, None]


def paint_area(self, c_e, is_select, area_select):
    if is_select:
        if self.current_item is not None:
            if self.current_item.type() == 5 and self.current_item not in self.l_bombs:
                self.scene_v.removeItem(self.current_item)
        area_select.append(c_e)
        pol = QPolygonF(area_select)
        pen = QPen(QColor('black'))
        pen.setStyle(Qt.DotLine)
        pen.setWidth(1)
        item = self.scene_v.addPolygon(pol, pen, QBrush(QColor(0, 100, 100, 10)))
        return area_select, item
    else:
        return [], self.current_item


def line_f_nodes(items, self):
    lines = []
    l_i_points = self.l_i_reservoir + self.l_i_nodes
    l_points = self.l_reservoir + self.l_nodes
    for item in items:
        index = l_i_points.index(item)
        node = l_points[index]
        for el in self.l_pipes:
            if node == el.n_i or node == el.n_f:
                index_p = self.l_pipes.index(el)
                lines.append(self.l_i_pipes[index_p])
    lines_2 = []
    for i in lines:
        if i not in lines_2:
            lines_2.append(i)
    return lines_2


def bombs_i_lines(lines, self):
    l_bombs = []
    for i, bomb in enumerate(self.l_i_bombs):
        if bomb in lines:
            l_bombs.append(self.l_bombs[i])
    return l_bombs


def select_items(self):
    self.scene_v.removeItem(self.current_item)
    if len(self.area_select) > 2:
        items = self.scene_v.items(QPolygonF(self.area_select))
        items_2 = []
        for i in items:
            if i.type() == 4 or i.type() == 7:
                items_2.append(i)
        lines = line_f_nodes(items_2, self)
        bombs = bombs_i_lines(lines, self)
        return items_2 + lines + bombs
    else:
        return []


def paint_selected(self):
    for i in self.l_items:
        if i.type() == 4:
            color = QColor(255 - self.node_color.red(),
                           255 - self.node_color.green(),
                           255 - self.node_color.blue())

            i.setPen(QPen(color))
            i.setBrush(QBrush(color))
        elif i.type() == 6:
            color = QColor(255 - self.pipe_color.red(),
                           255 - self.pipe_color.green(),
                           255 - self.pipe_color.blue())
            pen = QPen(color)
            pen.setWidth(2)
            pen.setStyle(Qt.DotLine)
            i.setPen(pen)
        i.setSelected(True)


def selected_item(self, item):
    default_color(self)
    show_text_default(self)
    self.parent.win_show_results.hide()
    if self.is_select:
        lines = []
        bombs = []
        if item.type() == 4 or item.type() == 7:
            lines = line_f_nodes([item], self)
            bombs = bombs_i_lines(lines, self)
        elif item.type() == 6:
            bombs = bombs_i_lines([item], self)
        return [item] + lines + bombs
    else:
        return []

def default_color(self):
    for i in self.scene_v.items():
        if i.type() == 4:
            i.setPen(QPen(self.node_color))
            i.setBrush(QBrush(self.node_color))
        elif i.type() == 6:
            pen = QPen(self.pipe_color)
            pen.setWidth(self.pipe_width)
            i.setPen(pen)


class Paint(QGraphicsView):
    def __init__(self, data, parent=None):
        super(Paint, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle('unnamed.hid')
        self.setSceneRect(0, 0, 3000, 3000)
        self.scene_v = QGraphicsScene()
        self.is_node = False
        self.is_pipe = False
        self.is_select = False
        self.is_area_select = False
        self.is_move = False
        self.is_reservoir = False
        self.is_bomb = False
        self.cont_nodes = 1
        self.cont_pipes = 1
        self.cont_reservoir = 1
        self.l_pipes = []
        self.l_i_pipes = []
        self.l_nodes = []
        self.l_i_nodes = []
        self.l_reservoir = []
        self.l_i_reservoir = []
        self.l_i_bombs = []
        self.l_bombs = []
        self.node_size = data[0][0]
        self.node_color = QColor(data[0][1][0], data[0][1][1], data[0][1][2])
        self.pipe_width = data[1][0]
        self.pipe_color = QColor(data[1][1][0], data[1][1][1], data[1][1][2])
        self.node_name = data[2][0]
        self.pipe_name = data[2][1]
        self.res_name = data[2][2]
        self.text_font = data[2][3]
        self.pref_node = data[2][4]
        self.pref_pipe = data[2][5]
        self.pref_res = data[2][6]
        self.text_visible_node = bool(data[2][0])
        self.text_visible_pipe = bool(data[2][1])
        self.text_visible_res = bool(data[2][2])
        self.text_node = []
        self.text_pipe = []
        self.text_res = []
        self.current_item = None
        self.change_style(data)
        self.setScene(self.scene_v)
        self.cond_pipe = False
        self.start_e = None
        self.union_pipe = [None, None]
        self.setMouseTracking(True)
        self.area_select = []
        self.l_items = []
        # pixmap reservoir:
        size_res = self.node_size + 6
        self.p_r = QPixmap(size_res, size_res)
        self.p_r.fill(QColor(10, 10, 10, 0))
        p_painter = QPainter()
        pen_p = QPen(Qt.black)
        pen_p.setWidth(1)
        brush = QBrush(Qt.blue, Qt.SolidPattern)
        p_painter.begin(self.p_r)
        p_painter.setPen(pen_p)
        p_painter.setBrush(brush)
        p_painter.drawPolygon(QPolygonF([QPointF(0, 0), QPointF(0, size_res - 1), QPointF(size_res - 1, size_res - 1),
                                         QPointF(size_res - 1, 0), QPointF(size_res - 1, int(size_res / 2)),
                                         QPointF(0, int(size_res / 2))]))
        p_painter.end()
        self.zoom = 1
        self.buttonPressed = 1


    def mousePressEvent(self, event):
        c_e = event.pos()
        c_e = self.mapToScene(c_e)
        area_select = QRectF(c_e.x()-3, c_e.y()-3, 6, 6)
        items = self.scene_v.items(area_select)
        if event.button() == Qt.MidButton:
            self.buttonPressed = 0
            self.setMouseTracking(True)
            self._startPos = c_e
        if event.buttons() == Qt.LeftButton:
            self.buttonPressed = 1
            self.current_item = paint_node(self, self.is_node, c_e)
            self.current_item = paint_reservoir(self, c_e)
            self.area_select, self.current_item = paint_area(self, c_e, self.is_area_select, self.area_select)
            if len(items) != 0:
                if self.is_select:
                    self.l_items = selected_item(self, items[0])
                    paint_selected(self)
                if items[0].type() == 4 or items[0].type() == 7:
                    self.cond_pipe, self.start_e, self.current_item, self.union_pipe = paint_pipe(self, c_e,
                                                                                                  self.is_pipe,
                                                                                                  self.l_i_nodes,
                                                                                                  self.cond_pipe,
                                                                                                  self.union_pipe,
                                                                                                  items,
                                                                                                  self.l_nodes)
                if items[0].type() == 6:
                    self.current_item = self.paint_bomb(items[0])
            else:
                default_color(self)
                self.l_items = []

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self.zoom *= factor
        else:
            factor = 0.8
            self.zoom *= factor
        if self.zoom >= 1:
            self.scale(factor, factor)
        else:
            self.zoom = 1

    def resizePaint(self, x1, y1, x2, y2):
        self.setSceneRect(x1, y1, x2, y2)

    def mouseMoveEvent(self, event):
        e = event.pos()
        e = self.mapToScene(e)
        area_select = QRectF(e.x()-3, e.y()-3, 6, 6)
        items = self.scene_v.items(area_select)
        if not self.buttonPressed:
            dx = e.x() - self._startPos.x()
            dy = e.y() - self._startPos.y()
            new_x = self.horizontalScrollBar().value() - dx
            new_y = self.verticalScrollBar().value() - dy
            self.horizontalScrollBar().setValue(new_x)
            self.verticalScrollBar().setValue(new_y)
        if self.is_pipe and self.cond_pipe:
            if items:
                l_n = self.l_i_nodes + self.l_i_reservoir
                l_n_2 = self.l_nodes + self.l_reservoir
                if items[0] in l_n:
                    e.setX(l_n_2[l_n.index(items[0])].x)
                    e.setY(l_n_2[l_n.index(items[0])].y)
            self.current_item.setLine(self.start_e.x(), self.start_e.y(), e.x(), e.y())
            pen = QPen(QColor('black'))
            pen.setWidth(1)
            pen.setStyle(Qt.DotLine)
            self.current_item.setPen(pen)
        if self.is_area_select and len(self.area_select) > 1:
            self.area_select.append(e)
            self.current_item.setPolygon(QPolygonF(self.area_select))
            self.area_select = self.area_select[:-1]

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MidButton:
            self.buttonPressed = 1

    def keyPressEvent(self, event):
        if event.key() == 16777220 and self.is_area_select:  # press enter
            self.l_items = select_items(self)
            paint_selected(self)
            self.area_select = []
        elif event.key() == 16777216:  # press esc
            self.l_items = []
            default_color(self)
            self.parent.is_select()
            if self.cond_pipe:
                self.scene_v.removeItem(self.current_item)
                self.cond_pipe = False
            self.parent.win_show_results.hide()
        elif event.key() == 16777223:  # press supra
            self.delete_item(self.l_items)

    def delete_item(self, l_item):
        for i in l_item:
            self.scene_v.removeItem(i)
            if i.type() == 4:
                index = self.l_i_nodes.index(i)
                self.scene_v.removeItem(self.text_node[index])
                self.l_i_nodes.remove(i)
                self.l_nodes.pop(index)
                self.text_node.pop(index)
            elif i.type() == 5:
                index = self.l_bombs.index(i)
                self.l_bombs.remove(i)
                self.l_i_bombs.pop(index)
            elif i.type() == 6:
                index = self.l_i_pipes.index(i)
                self.scene_v.removeItem(self.text_pipe[index])
                self.l_i_pipes.remove(i)
                self.l_pipes.pop(index)
                self.text_pipe.pop(index)
            elif i.type() == 7:
                index = self.l_i_reservoir.index(i)
                self.scene_v.removeItem(self.text_res[index])
                self.l_i_reservoir.remove(i)
                self.l_reservoir.pop(index)
                self.text_res.pop(index)

    def paint_node(self, e):
        pen = QPen(self.node_color)
        brush = QBrush(self.node_color, Qt.SolidPattern)
        item = self.scene_v.addEllipse(e.x()-self.node_size/2, e.y()-self.node_size/2, self.node_size, self.node_size,
                                       pen, brush)
        item.setZValue(1)
        self.scene_v.addItem(item)
        new_node = Node()
        new_node.name = self.pref_node + '-' + str(self.cont_nodes)
        new_node.x = e.x()
        new_node.y = e.y()
        text_item = self.scene_v.addText(new_node.name)
        text_item.setFont(self.text_font)
        text_item.setX(e.x())
        text_item.setY(e.y())
        if not self.text_visible_node:
            text_item.hide()
        self.text_node.append(text_item)
        new_node.level = float(self.parent.default_data[0][0])
        item.setToolTip(new_node.name)
        self.l_nodes.append(new_node)
        self.l_i_nodes.append(item)
        self.cont_nodes += 1
        return item

    def paint_pipe(self, e_i, e_f, n_i, n_f):
        pen = QPen(self.pipe_color)
        pen.setWidth(self.pipe_width)
        item = self.scene_v.addLine(e_i.x(), e_i.y(), e_f.x(), e_f.y(), pen)
        self.scene_v.addItem(item)
        new_pipe = Pipe()
        new_pipe.name = self.pref_pipe + '-' + str(self.cont_pipes)
        text_item = self.scene_v.addText(new_pipe.name)
        text_item.setFont(self.text_font)
        text_item.setX((2 * e_i.x() + e_f.x()) / 3)
        text_item.setY((2 * e_i.y() + e_f.y()) / 3)
        if not self.text_visible_pipe:
            text_item.hide()
        self.text_pipe.append(text_item)
        new_pipe.item = item
        new_pipe.n_i = n_i
        new_pipe.n_f = n_f
        new_pipe.v_t = not bool(self.parent.default_data[1][2][0])
        if new_pipe.v_t:
            new_pipe.vis = float(self.parent.default_data[1][2][1])
        else:
            new_pipe.t = float(self.parent.default_data[1][3][1])
        if self.parent.default_data[1][4][0]:
            new_pipe.flow = float(self.parent.default_data[1][4][1])/1000
        new_pipe.diam = float(self.parent.default_data[0][2])/1000
        new_pipe.long = float(self.parent.default_data[0][1])
        if self.parent.default_data[1][1] == 0:
            new_pipe.ks = float(self.parent.default_data[0][3])
        if self.parent.default_data[1][1] == 1:
            new_pipe.C = float(self.parent.default_data[0][3])
        if self.parent.default_data[1][1] == 2:
            new_pipe.n_m = float(self.parent.default_data[0][3])
        item.setToolTip(new_pipe.name)
        self.l_pipes.append(new_pipe)
        self.l_i_pipes.append(item)
        self.cont_pipes += 1
        return item

    def paint_reservoir(self, e):
        new_res = Reservoir()
        new_res.name = self.pref_res + '-' + str(self.cont_reservoir)
        new_res.x = e.x()
        new_res.y = e.y()
        e.setX(e.x() - (self.node_size + 6) / 2)
        e.setY(e.y() - (self.node_size + 6) / 2)
        item = self.scene_v.addPixmap(self.p_r)
        item.setPos(e)
        item.setZValue(1)
        self.scene_v.addItem(item)
        new_res.item = item
        item.setToolTip(new_res.name)
        text_item = self.scene_v.addText(new_res.name)
        text_item.setFont(self.text_font)
        text_item.setX(new_res.x)
        text_item.setY(new_res.y)
        if not self.text_visible_res:
            text_item.hide()
        self.l_reservoir.append(new_res)
        self.l_i_reservoir.append(item)
        self.text_res.append(text_item)
        self.cont_reservoir += 1
        return item

    def paint_bomb(self, line):
        if self.is_bomb:
            if line not in self.l_i_bombs:
                c_bomb = polygon_bomb(line)
                item = self.scene_v.addPolygon(c_bomb, QPen(Qt.black), QBrush(Qt.black, Qt.SolidPattern))
                self.scene_v.addItem(item)
                self.l_bombs.append(item)
                self.l_i_bombs.append(line)
                return item
            else:
                return self.current_item
        else:
            return self.current_item

    def change_style(self, data):
        self.node_size = data[0][0]
        self.node_color = QColor(data[0][1][0], data[0][1][1], data[0][1][2])
        self.pipe_width = data[1][0]
        self.pipe_color = QColor(data[1][1][0], data[1][1][1], data[1][1][2])
        self.node_name = data[2][0]
        self.pipe_name = data[2][1]
        self.res_name = data[2][2]
        self.font_text = data[2][3]
        self.pref_node = data[2][4]
        self.pref_pipe = data[2][5]
        self.pref_res = data[2][6]
