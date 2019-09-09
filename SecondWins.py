from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import ezdxf

class Preferences(QDialog):
    def __init__(self, data):
        QDialog.__init__(self)
        self.setWindowTitle('Preferencias')
        self.setMinimumSize(QSize(300, 300))
        self.setMaximumSize(QSize(300, 300))
        self.data = data
        grid = QGridLayout(self)
        grid1 = QGridLayout()
        grid2 = QGridLayout()
        grid3 = QGridLayout()
        grid1.addWidget(QLabel('Número de Decimales: '), 0, 0)
        self.dec_box = QSpinBox(self)
        self.dec_box.setMinimum(1)
        self.dec_box.setMaximum(6)
        self.dec_box.setValue(self.data[0])
        grid1.addWidget(self.dec_box, 0, 1)
        grid2.addWidget(QLabel('Número de Interaciones Máximas: '), 0, 0)
        grid2.addWidget(QLabel('Error Máximo permitido: '), 1, 0)
        self.itr_box = QSpinBox(self)
        self.itr_box.setMinimum(5)
        self.itr_box.setMaximum(60)
        self.itr_box.setValue(self.data[1])
        self.error_box = QLineEdit(self)
        self.error_box.setText(self.data[2])
        grid2.addWidget(self.itr_box, 0, 1)
        grid2.addWidget(self.error_box, 1, 1)
        self.temp_box = QRadioButton('Temperatura')
        self.temp_box.setChecked(not self.data[3])
        self.vis_box = QRadioButton('Viscocidad')
        self.vis_box.setChecked(self.data[3])
        if self.data[3] == 0:
            self.temp_box.setChecked(self.data[3])
        elif self.data[3] == 1:
            self.vis_box.setChecked(True)
        grid3.addWidget(self.temp_box, 0, 0)
        grid3.addWidget(self.vis_box, 0, 1)
        group1 = QGroupBox('Redondeo')
        group1.setLayout(grid1)
        group2 = QGroupBox('Presición')
        group2.setLayout(grid2)
        group3 = QGroupBox('T o V')
        group3.setLayout(grid3)
        grid.addWidget(group1, 0, 0, 1, 2)
        grid.addWidget(group2, 1, 0, 1, 2)
        grid.addWidget(group3, 2, 0, 1, 2)
        self.acceptButton = QPushButton('Aceptar')
        self.acceptButton.clicked.connect(self.acceptFunction)
        self.cancelButton = QPushButton('Cancelar')
        self.cancelButton.clicked.connect(self.close)
        grid.addWidget(self.acceptButton, 3, 0)
        grid.addWidget(self.cancelButton, 3, 1)

    def acceptFunction(self):
        self.data[0] = self.dec_box.value()
        self.data[1] = self.itr_box.value()
        self.data[2] = self.error_box.text()
        if self.temp_box.isChecked():
            self.data[3] = 0
        elif self.vis_box.isChecked():
            self.data[3] = 1
        self.close()


class ViewOptions(QDialog):
    def __init__(self, data):
        QDialog.__init__(self)
        self.setWindowTitle('Opciones de Visualización')
        self.data = data
        self.setMinimumSize(QSize(300, 400))
        self.setMaximumSize(QSize(400, 400))
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setTabPosition(QTabWidget.West)
        tab1 = QWidget(self)
        tab2 = QWidget(self)
        tab3 = QWidget(self)
        tab4 = QWidget(self)
        tab5 = QWidget(self)
        self.tabWidget.addTab(tab1, 'Nudo')
        self.tabWidget.addTab(tab2, 'Linea')
        self.tabWidget.addTab(tab3, 'Etiquetas')
        self.tabWidget.addTab(tab4, 'Flecha de Caudal')
        self.tabWidget.addTab(tab5, 'Color de Fondo')
        grid = QGridLayout(self)
        grid.addWidget(self.tabWidget)
        grid1 = QGridLayout()
        grid1_1 = QGridLayout()
        grid1_2 = QGridLayout()
        self.size_nod = QSpinBox()
        self.size_nod.setMinimum(5)
        self.size_nod.setMaximum(15)
        self.size_nod.setValue(self.data[0][0])
        btn1 = QPushButton('Cambiar Color')
        btn1.clicked.connect(self.changeColorNod)
        self.nod_color = QFrame()
        self.nod_color.setStyleSheet("QWidget { background-color: %s }" %
                                     QColor(self.data[0][1][0], self.data[0][1][1], self.data[0][1][2]).name())
        grid1_1.addWidget(self.size_nod, 0, 0)
        grid1_2.addWidget(btn1, 0, 0)
        grid1_2.addWidget(self.nod_color, 0, 1)
        group1_1 = QGroupBox('Tamaño de Nodo')
        group1_1.setLayout(grid1_1)
        group1_2 = QGroupBox('Color de Nodo')
        group1_2.setLayout(grid1_2)
        grid1.addWidget(group1_1)
        grid1.addWidget(group1_2)
        grid2 = QGridLayout()

        grid2_1 = QGridLayout()
        grid2_2 = QGridLayout()
        self.size_line = QSpinBox()
        self.size_line.setMinimum(1)
        self.size_line.setMaximum(5)
        self.size_line.setValue(self.data[1][0])
        btn2 = QPushButton('Cambiar Color')
        btn2.clicked.connect(self.changeColorLine)
        self.line_color = QFrame()
        self.line_color.setStyleSheet("QWidget { background-color: %s }" %
                                     QColor(self.data[1][1][0], self.data[1][1][1], self.data[1][1][2]).name())
        grid2_1.addWidget(self.size_line, 0, 0)
        grid2_2.addWidget(btn2, 0, 0)
        grid2_2.addWidget(self.line_color, 0, 1)
        group2_1 = QGroupBox('Grosor de Linea')
        group2_1.setLayout(grid2_1)
        group2_2 = QGroupBox('Color de Linea')
        group2_2.setLayout(grid2_2)
        grid2.addWidget(group2_1)
        grid2.addWidget(group2_2)

        grid3 = QGridLayout()
        grid3_1 = QGridLayout()
        self.nod_tag = QCheckBox('ID de Nodo')
        self.line_tag = QCheckBox('ID de Tubería')
        self.items_tag = QCheckBox('ID de los Elementos')
        self.nod_tag.setChecked(self.data[2][0])
        self.line_tag.setChecked(self.data[2][1])
        self.items_tag.setChecked(self.data[2][2])
        self.pref_nud = QLineEdit(self)
        self.pref_nud.setText(self.data[2][4])
        self.pref_bar = QLineEdit(self)
        self.pref_bar.setText(self.data[2][5])
        self.pref_el = QLineEdit(self)
        self.pref_el.setText(self.data[2][6])
        grid3_1.addWidget(QLabel('Prefijos'), 0, 1)
        grid3_1.addWidget(self.nod_tag, 1, 0)
        grid3_1.addWidget(self.line_tag, 2, 0)
        grid3_1.addWidget(self.items_tag, 3, 0)
        grid3_1.addWidget(self.pref_nud, 1, 1)
        grid3_1.addWidget(self.pref_bar, 2, 1)
        grid3_1.addWidget(self.pref_el, 3, 1)
        grid3_2 = QGridLayout()
        font_btn = QPushButton('Cambiar Fuente')
        font_btn.clicked.connect(self.changeFontTag)
        self.exampleFont = QLabel('Example')
        self.exampleFont.setFont(self.data[2][3])
        grid3_2.addWidget(font_btn, 0, 0)
        grid3_2.addWidget(self.exampleFont, 0, 1)
        group3_1 = QGroupBox('Mostrar Etiquetas')
        group3_2 = QGroupBox('Fuente de Etiquetas')
        group3_1.setLayout(grid3_1)
        group3_2.setLayout(grid3_2)
        grid3.addWidget(group3_1)
        grid3.addWidget(group3_2)
        grid4 = QGridLayout()
        self.flecha = QCheckBox('Mostrar la flecha de dirección del daudal.')
        self.flecha.setChecked(self.data[3][0])
        self.flecha.clicked.connect(self.changeFlowState)
        self.open_flow = QRadioButton('Abierta')
        self.open_flow.clicked.connect(self.changeFlowState)
        self.close_flow = QRadioButton('Cerrada')
        self.close_flow.clicked.connect(self.changeFlowState)
        self.open_flow.setChecked(True)
        if self.flecha.isChecked():
            self.open_flow.setEnabled(True)
            self.close_flow.setEnabled(True)
        else:
            self.open_flow.setEnabled(False)
            self.close_flow.setEnabled(False)
        grid4.addWidget(self.flecha, 0, 0, 1, 2)
        grid4.addWidget(self.open_flow, 1, 1)
        grid4.addWidget(self.close_flow, 2, 1)
        grid5 = QGridLayout()
        root_btn = QPushButton('Cambiar Color')
        root_btn.clicked.connect(self.changeColorRoot)
        self.root_color = QFrame()
        self.root_color.setStyleSheet("QWidget { background-color: %s }" %
                                      QColor(self.data[4][0], self.data[4][1], self.data[4][2]).name())
        grid5.addWidget(root_btn)
        grid5.addWidget(self.root_color)
        tab1.setLayout(grid1)
        tab2.setLayout(grid2)
        tab3.setLayout(grid3)
        tab4.setLayout(grid4)
        tab5.setLayout(grid5)

    def changeColorNod(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.nod_color.setStyleSheet("QWidget { background-color: %s }"% col.name())
            self.data[0][1][0] = col.getRgb()[0]
            self.data[0][1][1] = col.getRgb()[1]
            self.data[0][1][2] = col.getRgb()[2]

    def changeColorLine(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.line_color.setStyleSheet("QWidget { background-color: %s }"% col.name())
            self.data[1][1][0] = col.getRgb()[0]
            self.data[1][1][1] = col.getRgb()[1]
            self.data[1][1][2] = col.getRgb()[2]

    def changeColorRoot(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.root_color.setStyleSheet("QWidget { background-color: %s }" % col.name())
            self.data[4][0] = col.getRgb()[0]
            self.data[4][1] = col.getRgb()[1]
            self.data[4][2] = col.getRgb()[2]

    def changeFontTag(self):
        font, ok = QFontDialog.getFont(self.data[2][3])
        if ok:
            self.data[2][3] = font
            self.exampleFont.setFont(self.data[2][3])

    def changeFlowState(self):
        if self.flecha.isChecked():
            self.data[3][0] = 1
            self.open_flow.setEnabled(True)
            self.close_flow.setEnabled(True)
            if self.open_flow.isChecked():
                self.data[3][1] = 1
                self.data[3][2] = 0
            elif self.close_flow.isChecked():
                self.data[3][1] = 0
                self.data[3][2] = 1
        else:
            self.data[3][0] = 0
            self.open_flow.setEnabled(False)
            self.close_flow.setEnabled(False)

    def closeEvent(self, event):
        self.data[0][0] = self.size_nod.value()
        self.data[1][0] = self.size_line.value()
        self.data[2][0] = int(self.nod_tag.isChecked())
        self.data[2][1] = int(self.line_tag.isChecked())
        self.data[2][2] = int(self.items_tag.isChecked())
        self.data[2][4] = self.pref_nud.text()
        self.data[2][5] = self.pref_bar.text()
        self.data[2][6] = self.pref_el.text()


class DefaultValues(QDialog):
    def __init__(self, data):
        QDialog.__init__(self)
        self.setWindowTitle('Valores por Defecto')
        self.setMinimumSize(QSize(250, 250))
        self.setMaximumSize(QSize(250, 250))
        self.data = data
        grid = QGridLayout(self)
        tabWidget = QTabWidget()
        tabWidget.setTabShape(QTabWidget.Triangular)
        tab1 = QWidget()
        grid1 = QGridLayout()
        # TAB1: PROPERTIES
        grid1.addWidget(QLabel('Cota Nudo: '), 0, 0)
        grid1.addWidget(QLabel('Longitud de Tuberia: '), 1, 0)
        grid1.addWidget(QLabel('Diámetro de Tuberia: '), 2, 0)
        self.labels = ['Rugosidad Relativa ks', 'Coeficiente Hazen', 'Coeficiente Manning']
        self.coefs = ['6e-5', '150', '0.01']
        self.d_c_m = QLabel(self.labels[self.data[1][1]])
        grid1.addWidget(self.d_c_m, 3, 0)
        self.cota = QLineEdit()
        self.cota.setText(self.data[0][0])
        self.long = QLineEdit()
        self.long.setText(self.data[0][1])
        self.diam = QLineEdit()
        self.diam.setText(self.data[0][2])
        self.rug = QLineEdit()
        self.rug.setText(self.data[0][3])
        grid1.addWidget(self.cota, 0, 1)
        grid1.addWidget(self.long, 1, 1)
        grid1.addWidget(self.diam, 2, 1)
        grid1.addWidget(self.rug, 3, 1)
        tab1.setLayout(grid1)
        # TAB2: HYDRAULIC PROP.
        tab2 = QWidget()
        grid2 = QGridLayout()
        grid2.addWidget(QLabel('Unidades Caudal'), 0, 0)
        grid2.addWidget(QLabel('Ecuación'), 1, 0)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        grid2.addWidget(line, 2, 0, 1, 2)
        self.visc = QRadioButton('Viscocidad Relativa')
        self.visc.setChecked(self.data[1][2][0])
        self.visc.clicked.connect(self.changeVisc_Temp)
        grid2.addWidget(self.visc, 3, 0)
        self.temp = QRadioButton('Temperatura')
        self.temp.setChecked(self.data[1][3][0])
        self.temp.clicked.connect(self.changeVisc_Temp)
        grid2.addWidget(self.temp, 4, 0)
        grid2.addWidget(line1, 5, 0, 1, 2)
        self.caudal_sem = QCheckBox('Caudal Semilla')
        self.caudal_sem.setChecked(self.data[1][4][0])
        self.caudal_sem.clicked.connect(lambda: self.caudal_sem_t.setEnabled(self.caudal_sem.isChecked()))
        grid2.addWidget(self.caudal_sem, 6, 0)
        self.units_flow = QComboBox()
        self.units_flow.addItems(['LPS', 'M3S'])
        self.units_flow.setCurrentIndex(self.data[1][0])
        grid2.addWidget(self.units_flow, 0, 1)
        self.equations = QComboBox()
        self.equations.addItems(['D_W', 'H-W', 'C-M'])
        self.equations.currentIndexChanged.connect(self.change_equations)
        self.equations.setCurrentIndex(self.data[1][1])
        grid2.addWidget(self.equations, 1, 1)
        self.visc_t = QLineEdit()
        self.visc_t.setText(self.data[1][2][1])
        self.visc_t.setEnabled(self.visc.isChecked())
        grid2.addWidget(self.visc_t, 3, 1)
        self.temp_t = QLineEdit()
        self.temp_t.setText(self.data[1][3][1])
        self.temp_t.setEnabled(self.temp.isChecked())
        grid2.addWidget(self.temp_t, 4, 1)
        self.caudal_sem_t = QLineEdit()
        self.caudal_sem_t.setText(self.data[1][4][1])
        self.caudal_sem_t.setEnabled(self.caudal_sem.isChecked())
        grid2.addWidget(self.caudal_sem_t, 6, 1)
        tab2.setLayout(grid2)
        tabWidget.addTab(tab1, 'Propiedades')
        tabWidget.addTab(tab2, 'Opciones Hidráulicas')
        grid.addWidget(tabWidget)

    def changeVisc_Temp(self):
        if self.visc.isChecked():
            self.visc_t.setEnabled(True)
            self.temp_t.setEnabled(False)
        elif self.temp.isChecked():
            self.temp_t.setEnabled(True)
            self.visc_t.setEnabled(False)

    def checkEntry(self, entry):
        if entry.text() == '':
            return False
        else:
            try:
                float(entry.text())
                return True
            except ValueError:
                return False

    def checkTab1(self):
        if self.checkEntry(self.cota) and self.checkEntry(self.long) and self.checkEntry(
                self.diam) and self.checkEntry(self.rug):
            return True
        else:
            return False

    def checkTab2(self):
        cond1 = True
        cond2 = True
        cond3 = True
        if self.visc.isChecked():
            if self.checkEntry(self.visc_t):
                cond1 = True
            else:
                cond1 = False
        elif self.temp.isChecked():
            if self.checkEntry(self.temp_t):
                cond2 = True
            else:
                cond2 = False
        if self.caudal_sem.isChecked():
            if self.checkEntry(self.caudal_sem_t):
                cond3 = True
            else:
                cond3 = False
        return cond1 and cond2 and cond3

    def change_equations(self):
        self.rug.setText(self.coefs[self.equations.currentIndex()])
        self.d_c_m.setText(self.labels[self.equations.currentIndex()])

    def closeEvent(self, event):
        if self.checkTab1() and self.checkTab2():
            self.data[0][0] = self.cota.text()
            self.data[0][1] = self.long.text()
            self.data[0][2] = self.diam.text()
            self.data[0][3] = self.rug.text()
            self.data[1][0] = self.units_flow.currentIndex()
            self.data[1][1] = self.equations.currentIndex()
            self.data[1][2][0] = int(self.visc.isChecked())
            self.data[1][2][1] = self.visc_t.text()
            self.data[1][3][0] = int(self.temp.isChecked())
            self.data[1][3][1] = self.temp_t.text()
            self.data[1][4][0] = int(self.caudal_sem.isChecked())
            self.data[1][4][1] = self.caudal_sem_t.text()
            event.accept()
        else:
            event.ignore()


class PropertiesData(QDialog):
    def __init__(self, parent, graphic, eq):
        QDialog.__init__(self)
        self.setWindowTitle(r'Datos')
        self.parent = parent
        self.graphics = graphic
        self.setMinimumSize(QSize(800, 300))
        self.setMaximumSize(QSize(800, 600))
        layout = QGridLayout(self)
        tab = QTabWidget(self)
        widget1 = QWidget(self)
        layout1 = QGridLayout()
        # --- LAYOUT1 --- #
        self.table_nods = QTableWidget()
        self.table_nods.setColumnCount(3)
        self.table_nods.setHorizontalHeaderLabels(['ID', 'Caudal\nDemanda', 'Cota\n(m)'])
        l_nods = self.graphics.l_reservoir + self.graphics.l_nodes
        self.table_nods.setRowCount(len(l_nods))
        for i, j in enumerate(l_nods):
            name_item = QTableWidgetItem(j.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table_nods.setItem(i, 0, name_item)
            self.table_nods.setItem(i, 2, QTableWidgetItem(str(j.level)))
        for i in range(len(self.graphics.l_reservoir)):
            item = QTableWidgetItem("")
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table_nods.setItem(i, 1, item)
        for i, j in enumerate(self.graphics.l_nodes):
            self.table_nods.setItem(i+len(self.graphics.l_reservoir), 1, QTableWidgetItem(str(j.demand)))
        layout1.addWidget(self.table_nods)
        widget1.setLayout(layout1)
        widget2 = QWidget(self)
        layout2 = QGridLayout()
        # --- LAYOUT2 --- #
        self.table_tubs = QTableWidget()
        self.table_tubs.setColumnCount(7)
        header_pipe = ['ID', 'Ni', 'Nf', 'Longitud\n(m)', 'Diámetro\n(mm)', 'ks\n(mm)', 'kl']
        if eq == 0:
            header_pipe[5] = 'ks\n(mm)'
        elif eq == 1:
            header_pipe[5] = 'C'
        elif eq == 2:
            header_pipe[5] = 'n'
        self.table_tubs.setHorizontalHeaderLabels(header_pipe)
        self.table_tubs.setRowCount(len(self.graphics.l_pipes))
        for i, j in enumerate(self.graphics.l_pipes):
            name_item = QTableWidgetItem(j.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table_tubs.setItem(i, 0, name_item)
            item_ni = QTableWidgetItem(j.n_i.name)
            item_ni.setFlags(item_ni.flags() & ~Qt.ItemIsEditable)
            self.table_tubs.setItem(i, 1, item_ni)
            item_nf = QTableWidgetItem(j.n_f.name)
            item_nf.setFlags(item_ni.flags() & ~Qt.ItemIsEditable)
            self.table_tubs.setItem(i, 2, item_nf)
            self.table_tubs.setItem(i, 3, QTableWidgetItem(str(j.long)))
            self.table_tubs.setItem(i, 4, QTableWidgetItem(str(j.diam)))
            self.table_tubs.setItem(i, 6, QTableWidgetItem(str(j.kl)))
            if eq == 0:
                self.table_tubs.setItem(i, 5, QTableWidgetItem(str(j.ks)))
            elif eq == 1:
                self.table_tubs.setItem(i, 5, QTableWidgetItem(str(j.C)))
            if eq == 2:
                self.table_tubs.setItem(i, 5, QTableWidgetItem(str(j.n_m)))
        layout2.addWidget(self.table_tubs)
        widget2.setLayout(layout2)
        widget3 = QWidget(self)
        layout3 = QGridLayout()
        # --- LAYOUT3 --- #
        self.bomb_table = QTableWidget()
        self.bomb_table.setColumnCount(4)
        self.bomb_table.setHorizontalHeaderLabels(['Tubería', 'a', 'b', 'c'])
        self.bomb_table.setRowCount(len(self.graphics.l_bombs))
        for j, i in enumerate(self.graphics.l_i_bombs):
            index = self.graphics.l_i_pipes.index(i)
            pipe = self.graphics.l_pipes[index]
            item = QTableWidgetItem(pipe.name)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.bomb_table.setItem(j, 0, item)
            self.bomb_table.setItem(j, 1, QTableWidgetItem(str(pipe.bomb_a)))
            self.bomb_table.setItem(j, 2, QTableWidgetItem(str(pipe.bomb_b)))
            self.bomb_table.setItem(j, 3, QTableWidgetItem(str(pipe.bomb_c)))

        layout3.addWidget(self.bomb_table)
        widget3.setLayout(layout3)
        tab.addTab(widget1, QIcon('Images/nod.png'), 'Conexiones')
        tab.addTab(widget2, QIcon('Images/bar.png'), 'Tuberias')
        tab.addTab(widget3, QIcon('Images/bomb.png'), 'Bombas')
        layout.addWidget(tab)

    def closeEvent(self, event):
        for i, j in enumerate(self.graphics.l_reservoir):
            j.level = float(self.table_nods.item(i, 2).text())
        n_r = len(self.graphics.l_reservoir)
        for i, j in enumerate(self.graphics.l_nodes):
            j.demand = float(self.table_nods.item(i+n_r, 1).text())
            j.level = float(self.table_nods.item(i+n_r, 2).text())

        for i, j in enumerate(self.graphics.l_pipes):
            j.long = float(self.table_tubs.item(i, 3).text())
            j.diam = float(self.table_tubs.item(i, 4).text())
            j.ks = float(self.table_tubs.item(i, 5).text())
            j.kl = float(self.table_tubs.item(i, 6).text())
        for i, j in enumerate(self.graphics.l_i_bombs):
            index = self.graphics.l_i_pipes.index(j)
            pipe = self.graphics.l_pipes[index]
            pipe.bomb_a = float(self.bomb_table.item(i, 1).text())
            pipe.bomb_b = float(self.bomb_table.item(i, 2).text())
            pipe.bomb_c = float(self.bomb_table.item(i, 3).text())


class SummaryWindow(QDialog):
    def __init__(self, data, graphics):
        QDialog.__init__(self)
        self.setWindowTitle('Resumen')
        self.setMaximumSize(QSize(350, 500))
        self.data = data
        self.paint = graphics
        summary = 'Número de Conexiones: \t'+str(data[0]) + \
                  ' \nNúmero de Tuberías: \t'+str(data[1]) + \
                  ' \nNúmero de Bombas: \t'+str(data[2]) + \
                  '\nNúmero de Embalses: \t'+str(data[3]) + \
                  '\nUnidades de Caudal: \t'+data[4] + \
                  '\nEcuación de Pérdidas: \t'+data[5]
        layout = QGridLayout(self)
        layout1 = QGridLayout()
        self.titleName = QLineEdit()
        self.titleName.setText(self.data[6])
        self.if_titleName = QCheckBox("Usar como cabecera en la impresión")
        layout1.addWidget(self.titleName)
        layout1.addWidget(self.if_titleName)
        layout2 = QGridLayout()
        self.notes_text = QTextEdit()
        self.notes_text.setText(self.data[7])
        layout2.addWidget(self.notes_text)
        layout3 = QGridLayout()
        self.summary_text = QTextEdit()
        self.summary_text.setText(summary)
        self.summary_text.setReadOnly(True)
        layout3.addWidget(self.summary_text)
        layout4 = QGridLayout()
        self.accept_button = QPushButton("Aceptar")
        self.accept_button.clicked.connect(self.close)
        layout4.addWidget(self.accept_button)
        group1 = QGroupBox("Título: ")
        group1.setLayout(layout1)
        group2 = QGroupBox("Notas: ")
        group2.setLayout(layout2)
        group3 = QGroupBox("Resumen: ")
        group3.setLayout(layout3)
        group4 = QGroupBox("")
        group4.setLayout(layout4)
        layout.addWidget(group1, 0, 0, 1, 2)
        layout.addWidget(group2, 1, 0, 1, 2)
        layout.addWidget(group3, 2, 0, 2, 1)
        layout.addWidget(group4, 2, 1)

    def closeEvent(self, event):
        self.data[6] = self.titleName.text()
        self.data[7] = self.notes_text.toPlainText()


class ResultsView(QDialog):
    def __init__(self, parent=None, paint=None):
        QDialog.__init__(self)
        self.setWindowTitle('Resultados')
        self.setMinimumSize(QSize(750, 600))
        self.setMaximumSize(QSize(1700, 1700))
        self.parent = parent
        self.paint = paint
        self.data_nodes = []
        name_nodes = []
        for i in self.paint.l_nodes:
            self.data_nodes.append([str(i.level), str(i.demand*1000), str(i.pressure()), str(i.demand*1000), str(i.height)])
            name_nodes.append(i.name)
        self.data_nodes2 = [[0 for i in range(len(self.data_nodes))] for j in range(5)]
        for i, j in enumerate(self.data_nodes):
            for k, l in enumerate(j):
                self.data_nodes2[k][i] = l
        layout = QGridLayout(self)
        self.tabWidget = QTabWidget()
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tab1 = QWidget(self)
        layout1 = QGridLayout()
        # ------- WIDGETS IN LAYOUT 1 ------- #
        group1 = QGroupBox("")
        layout1_1 = QGridLayout()  # Checkbox
        self.dim_check = QCheckBox("Cotas")
        self.dim_check.clicked.connect(self.change_labels_nod)
        self.demand_check = QCheckBox("Demanda")
        self.demand_check.clicked.connect(self.change_labels_nod)
        self.pressure_check = QCheckBox("Presión")
        self.pressure_check.setChecked(True)
        self.pressure_check.clicked.connect(self.change_labels_nod)
        self.demand_base_check = QCheckBox("Demanda Base")
        self.demand_base_check.setChecked(True)
        self.demand_base_check.clicked.connect(self.change_labels_nod)
        self.height_check = QCheckBox("Altura")
        self.height_check.setChecked(True)
        self.height_check.clicked.connect(self.change_labels_nod)
        self.data_init_nod = [0, 0, 1, 1, 1]
        self.labels_nods = ['Cotas\n(m)', 'Demanda\n(lts/s)', 'Presión\n(m)', 'Demanda Base\n(lts/s)', 'Altura\n(m)']
        layout1_1.addWidget(self.dim_check, 0, 0)
        layout1_1.addWidget(self.demand_check, 0, 1)
        layout1_1.addWidget(self.pressure_check, 0, 2)
        layout1_1.addWidget(self.demand_base_check, 1, 0)
        layout1_1.addWidget(self.height_check, 1, 1)
        group1.setLayout(layout1_1)
        layout1.addWidget(group1)
        self.table_nod = QTableWidget()
        layout1.addWidget(self.table_nod)
        self.tab1.setLayout(layout1)
        self.tab2 = QWidget(self)
        layout2 = QGridLayout()
        # ------- WIDGETS IN LAYOUT 2 ------- #
        group2 = QGroupBox("")
        layout2_1 = QGridLayout()  # Checkbox
        self.long_check = QCheckBox("Longitud")
        self.long_check.clicked.connect(self.change_labels_tub)
        self.diam_check = QCheckBox("Diámetro")
        self.diam_check.clicked.connect(self.change_labels_tub)
        self.ks_check = QCheckBox("Rugosidad")
        self.ks_check.clicked.connect(self.change_labels_tub)
        self.f_f_check = QCheckBox("Factor de Fricción")
        self.f_f_check.clicked.connect(self.change_labels_tub)
        self.f_f_check.setChecked(True)
        self.flow_check = QCheckBox("Caudal")
        self.flow_check.clicked.connect(self.change_labels_tub)
        self.flow_check.setChecked(True)
        self.speed_check = QCheckBox("Velocidad")
        self.speed_check.clicked.connect(self.change_labels_tub)
        self.speed_check.setChecked(True)
        self.lost_unit_check = QCheckBox("Pérdida Unitaria")
        self.lost_unit_check.clicked.connect(self.change_labels_tub)
        self.lost_unit_check.setChecked(True)
        layout2_1.addWidget(self.long_check, 0, 0)
        layout2_1.addWidget(self.diam_check, 0, 1)
        layout2_1.addWidget(self.ks_check, 0, 2)
        layout2_1.addWidget(self.f_f_check, 0, 3)
        layout2_1.addWidget(self.flow_check, 1, 0)
        layout2_1.addWidget(self.speed_check, 1, 1)
        layout2_1.addWidget(self.lost_unit_check, 1, 2)
        group2.setLayout(layout2_1)
        layout2.addWidget(group2)
        self.table_tub = QTableWidget()
        layout2.addWidget(self.table_tub)
        self.tab2.setLayout(layout2)
        self.data_init_tubs = [0, 0, 0, 1, 1, 1, 1]
        self.labels_tubs = ['Longitud\n(m)', 'Diámetro\n(lts/s)', 'Rugosidad\n(m)', 'Factor de Fricción\n(lts/s)',
                            'Caudal\n(m)', 'Velocidad\n(m/s)', 'Périda Unitaria\n(m/km)']
        self.tabWidget.addTab(self.tab1, 'Conexiones')
        self.tabWidget.addTab(self.tab2, 'Tuberias')
        layout.addWidget(self.tabWidget)
        self.horizontal_labels(table=self.table_nod, data=self.data_init_nod, labels=self.labels_nods)
        self.horizontal_labels(table=self.table_tub, data=self.data_init_tubs, labels=self.labels_tubs)
        self.table_nod.setVerticalHeaderLabels(name_nodes)
        self.change_labels_nod()
        self.change_labels_tub()

    @staticmethod
    def horizontal_labels(table:QTableWidget, data:list, labels:list):
        table.setColumnCount(sum(data))
        labels1 = [labels[i] for i in range(len(labels)) if data[i] != 0]
        table.setHorizontalHeaderLabels(labels1)
        return

    @staticmethod
    def put_data(table: QTableWidget, data_header: list, data: list):
        data1 = [data[i] for i in range(len(data)) if data_header[i] != 0]
        table.setRowCount(len(data1[0]))
        for i in range(len(data1)):  # Columns
            for j in range(len(data1[i])):
                table.setItem(j, i, QTableWidgetItem(data1[i][j]))
        return

    @staticmethod
    def check_to_data(*args):
        return [int(i.isChecked()) for i in args]

    def change_labels_nod(self):
        data = self.check_to_data(self.dim_check, self.demand_check, self.pressure_check, self.demand_base_check,
                                  self.height_check)
        self.horizontal_labels(self.table_nod, data, self.labels_nods)
        self.put_data(self.table_nod, data, self.data_nodes2)

    def change_labels_tub(self):
        data = self.check_to_data(self.long_check, self.diam_check, self.ks_check, self.f_f_check, self.flow_check,
                                  self.speed_check, self.lost_unit_check)

        self.horizontal_labels(self.table_tub, data, self.labels_tubs)


class WinResults(QDialog):
    def __init__(self, parent=None, paint=None):
        super(WinResults, self).__init__(parent)
        self.setMinimumSize(200, 500)
        self.setMaximumSize(200, 500)
        self.parent = parent
        self.paint = paint
        self.object_w = QComboBox()
        self.list_w = QListWidget()
        self.list_p = {'Pipe': ['Flow', 'Speed', 'Long', 'Hf'], 'Node': ['Pressure', 'Level', 'Height']}
        self.object_w.addItems(self.list_p.keys())
        self.n_colors = QLineEdit()
        self.n_colors.textChanged.connect(lambda: self.check_entry(self.n_colors))
        self.n_colors.textChanged.connect(self.calc_colors)
        self.i_color = QWidget()
        self.color_initial = QColor(255, 0, 0)
        self.i_color.setStyleSheet("background-color: %s" %self.color_initial.name())
        self.f_color = QWidget()
        self.color_final = QColor(0, 0, 255)
        self.f_color.setStyleSheet("background-color: %s" %self.color_final.name())
        self.m_color = QGraphicsView()
        self.scene_v = QGraphicsScene()
        self.rect_F = QRectF()
        self.rect_F.setCoords(0, 0, 155, 45)
        self.m_color.setSceneRect(self.rect_F)
        self.m_color.setScene(self.scene_v)
        self.m_color.setMinimumHeight(50)
        self.m_color.setMaximumHeight(50)
        self.object_w.currentIndexChanged.connect(self.changed_list)
        self.object_w.currentIndexChanged.connect(self.calc_colors)
        self.label1 = QLabel("0")
        self.label1.setAlignment(Qt.AlignLeft)
        self.label2 = QLabel("1")
        self.label2.setAlignment(Qt.AlignHCenter)
        self.label3 = QLabel("2")
        self.label3.setAlignment(Qt.AlignHCenter)
        self.label4 = QLabel("3")
        self.label4.setAlignment(Qt.AlignRight)
        self.init_ui()
        self.changed_list()

    def check_entry(self, entry:QLineEdit):
        if entry.text() != "" or len(entry.text()) < 4:
            try:
                int(entry.text())
                entry.setStyleSheet("background: white")
                return True
            except ValueError:
                entry.setStyleSheet("background: red")
                return False
        else:
            entry.setStyleSheet("background: red")
            return False




    def init_ui(self):
        layout_g = QVBoxLayout(self)
        layout_1 = QVBoxLayout()
        layout_1.addWidget(self.object_w)
        layout_1.addWidget(self.list_w)
        layout_2 = QGridLayout()
        layout_2.addWidget(QLabel('Nª colors :'), 0, 0, 1, 2)
        layout_2.addWidget(self.n_colors, 0, 2, 1, 2)
        btn_i = QPushButton('Initial color: ')
        btn_i.clicked.connect(self.change_i_color)
        layout_2.addWidget(btn_i, 1, 0, 1, 2)
        layout_2.addWidget(self.i_color, 1, 2, 1, 2)
        btn_f = QPushButton('Final color: ')
        btn_f.clicked.connect(self.change_f_color)
        layout_2.addWidget(btn_f, 2, 0, 1, 2)
        layout_2.addWidget(self.f_color, 2, 2, 1, 2)
        layout_2.addWidget(self.m_color, 3, 0, 1, 4)
        layout_2.addWidget(self.label1, 4, 0)
        layout_2.addWidget(self.label2, 4, 1)
        layout_2.addWidget(self.label3, 4, 2)
        layout_2.addWidget(self.label4, 4, 3)
        group_1 = QGroupBox('Object and property')
        group_1.setLayout(layout_1)
        group_2 = QGroupBox('colors')
        group_2.setLayout(layout_2)
        layout_g.addWidget(group_1)
        layout_g.addWidget(group_2)
        btn_accept = QPushButton('Accept')
        btn_accept.clicked.connect(self.accept_color)
        layout_g.addWidget(btn_accept)

    def change_i_color(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.i_color.setStyleSheet("QWidget { background-color: %s }" % col.name())
            self.color_initial = col
            self.calc_colors()

    def change_f_color(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.f_color.setStyleSheet("QWidget { background-color: %s }" % col.name())
            self.color_final = col
            self.calc_colors()

    def changed_list(self):
        self.list_w.clear()
        for i in self.list_p[self.object_w.currentText()]:
            item = QListWidgetItem(i)
            self.list_w.addItem(item)
        self.list_w.setCurrentRow(0)

    def calc_colors(self):
        if self.check_entry(self.n_colors):
            self.scene_v.clear()
            n = int(self.n_colors.text())+1
            if n < 1000:
                width = self.rect_F.width()/(n+1)
                for i in range(n+1):
                    color = get_color(self.color_initial, self.color_final, n, i)
                    pen = QPen(color)
                    brush = QBrush(color, Qt.SolidPattern)
                    self.scene_v.addRect(i*width,  0, (i+1)*width, 30, pen, brush)

    def accept_color(self):
        if self.check_entry(self.n_colors):
            cond = (self.object_w.currentIndex(), self.list_w.currentRow())
            n = int(self.n_colors.text()) + 1
            show_color_default(self.paint)
            if cond == (0,0):  # pipe - flow
                hide_pipe_text(self.paint.text_node)
                l_flow = [round(abs(i.flow), 10) for i in self.paint.l_pipes]
                min_flow = min(l_flow)
                max_flow = max(l_flow)
                values = paint_color_item(l_flow, self.paint.l_i_pipes, min_flow, max_flow, n, self.color_initial, self.color_final)
                self.label1.setText(str(round(values[0], 1)))
                self.label2.setText(str(round(values[1], 1)))
                self.label3.setText(str(round(values[2], 1)))
                self.label4.setText(str(round(values[3], 1)))
                show_text_pipe(self.paint.text_pipe, self.paint.l_pipes, 0)
            elif cond == (0,1):  # pipe - speed
                hide_pipe_text(self.paint.text_node)
                l_speed = [round(abs(i.speed), 10) for i in self.paint.l_pipes]
                min_speed = min(l_speed)
                max_speed = max(l_speed)
                values = paint_color_item(l_speed, self.paint.l_i_pipes, min_speed, max_speed, n, self.color_initial, self.color_final)
                self.label1.setText(str(round(values[0], 1)))
                self.label2.setText(str(round(values[1], 1)))
                self.label3.setText(str(round(values[2], 1)))
                self.label4.setText(str(round(values[3], 1)))
                show_text_pipe(self.paint.text_pipe, self.paint.l_pipes, 1)
            elif cond == (0,2):  # pipe - long
                hide_pipe_text(self.paint.text_node)
                l_long = [round(abs(i.long), 10) for i in self.paint.l_pipes]
                min_long = min(l_long)
                max_long = max(l_long)
                values = paint_color_item(l_long, self.paint.l_i_pipes, min_long, max_long, n, self.color_initial, self.color_final)
                self.label1.setText(str(round(values[0], 1)))
                self.label2.setText(str(round(values[1], 1)))
                self.label3.setText(str(round(values[2], 1)))
                self.label4.setText(str(round(values[3], 1)))
                show_text_pipe(self.paint.text_pipe, self.paint.l_pipes, 2)
            elif cond == (0,3):  # pipe - Hf
                hide_pipe_text(self.paint.text_node)
                print('pipe, algo')
            elif cond == (1,0):  # Node - pressure
                hide_pipe_text(self.paint.text_pipe)
                l_pressure = [round(i.pressure(), 10) for i in self.paint.l_nodes]
                min_pressure = min(l_pressure)
                max_pressure = max(l_pressure)
                values = paint_color_item(l_pressure, self.paint.l_i_nodes, min_pressure, max_pressure, n, self.color_initial, self.color_final, 1)
                self.label1.setText(str(round(values[0], 1)))
                self.label2.setText(str(round(values[1], 1)))
                self.label3.setText(str(round(values[2], 1)))
                self.label4.setText(str(round(values[3], 1)))
                show_text_node(self.paint.text_node, self.paint.l_nodes, 0)
            elif cond == (1,1):  # Node - level
                hide_pipe_text(self.paint.text_pipe)
                l_level = [round(i.level, 10) for i in self.paint.l_nodes]
                min_level = min(l_level)
                max_level = max(l_level)
                values = paint_color_item(l_level, self.paint.l_i_nodes, min_level, max_level, n, self.color_initial, self.color_final, 1)
                self.label1.setText(str(round(values[0], 1)))
                self.label2.setText(str(round(values[1], 1)))
                self.label3.setText(str(round(values[2], 1)))
                self.label4.setText(str(round(values[3], 1)))
                show_text_node(self.paint.text_node, self.paint.l_nodes, 1)
            elif cond == (1,2):  # Node - height
                hide_pipe_text(self.paint.text_pipe)
                l_height = [round(i.height, 10) for i in self.paint.l_nodes]
                min_height = min(l_height)
                max_height = max(l_height)
                values = paint_color_item(l_height, self.paint.l_i_nodes, min_height, max_height, n, self.color_initial, self.color_final, 1)
                self.label1.setText(str(round(values[0], 1)))
                self.label2.setText(str(round(values[1], 1)))
                self.label3.setText(str(round(values[2], 1)))
                self.label4.setText(str(round(values[3], 1)))
                show_text_node(self.paint.text_node, self.paint.l_nodes, 2)

    def closeEvent(self, QCloseEvent):
        QCloseEvent.ignore()


def hide_pipe_text(text_item):
    for i in text_item:
        i.hide()


def paint_color_item(l_value, l_i, min_v, max_v, n, c_i, c_f, cond=0):
    d_v = (max_v - min_v)/(n)
    l_v = []
    v_i = min_v - d_v
    for i in range(n+3):
        l_v.append(round(v_i, 8))
        v_i += d_v
    index = 0
    for i, j in enumerate(l_i):
        value = l_value[i]
        for k, l in enumerate(l_v):
            if value > l:
                continue
            else:
                index = k
                break
        color = get_color(c_i, c_f, n+2, index)
        j.setPen(QPen(color))
        if cond:
            j.setBrush(QBrush(color, Qt.SolidPattern))
    return l_v[0], (2 * l_v[0] + l_v[-1])/3, (l_v[0] + 2*l_v[-1])/3, l_v[-1]

def put_text(l_p, l_n, l_r, eq, n_d):
    for j in l_p:
        j.t_flow = str(round(j.flow, n_d))
        j.t_speed = str(round(j.speed, n_d))
        j.t_long = str(round(j.long, n_d))
        j.t_hf = str(round(j.alpha(eq), n_d))
    for j in l_n:
        j.t_pressure = str(round(j.pressure(), n_d))
        j.t_level = str(round(j.level, n_d))
        j.t_height = str(round(j.height, n_d))
    for i in l_r:
        i.t_level = str(round(i.level, n_d))


def get_color(c_i, c_f, n, x):
    delta_r = (c_f.red() - c_i.red())/n
    delta_g = (c_f.green() - c_i.green())/n
    delta_b = (c_f.blue() - c_i.blue())/n
    return QColor(c_i.red() + delta_r*x, c_i.green() + delta_g*x, c_i.blue() + delta_b*x)


def show_text_pipe(l_tp, l_p, cond):
    for i, j in enumerate(l_tp):
        if cond == 0:
            j.setPlainText(l_p[i].t_flow)
        elif cond == 1:
            j.setPlainText(l_p[i].t_speed)
        elif cond == 2:
            j.setPlainText(l_p[i].t_long)
        elif cond == 3:
            j.setPlainText('0')
        j.show()


def show_text_node(l_tn, l_n, cond):
    for i, j in enumerate(l_tn):
        if cond == 0:
            j.setPlainText(l_n[i].t_pressure)
        elif cond == 1:
            j.setPlainText(l_n[i].t_level)
        elif cond == 2:
            j.setPlainText(l_n[i].t_height)
        j.show()


def show_color_default(paint):
    for i in paint.l_i_pipes:
        i.setPen(QPen(paint.pipe_color))
    for i in paint.l_i_nodes:
        i.setPen(QPen(paint.node_color))
        i.setBrush(QBrush(paint.node_color))


def show_text_default(paint):
    for i, j in enumerate(paint.l_pipes):
        text = paint.text_pipe[i]
        text.setPlainText(j.name)
        if not paint.text_visible_pipe:
            text.hide()
    for i, j in enumerate(paint.l_nodes):
        text = paint.text_node[i]
        text.setPlainText(j.name)
        if not paint.text_visible_node:
            text.hide()
    for i, j in enumerate(paint.l_reservoir):
        text = paint.text_res[i]
        text.setPlainText(j.name)
        if not paint.text_visible_res:
            text.hide()

def graphToStr(paint):
    l_res = []
    l_nodes = []
    l_pipes = []
    for i in paint.l_reservoir:
        l_pro = [i.name, i.level, i.x, i.y]
        l_names = ["name", "level", "x", "y"]
        l_res.append(dict(zip(l_names, l_pro)))
    for i in paint.l_nodes:
        l_pro = [i.name, i.demand, i.level, i.height, i.x, i.y]
        l_names = ["name", "demand", "level", "height", "x", "y"]
        l_nodes.append(dict(zip(l_names, l_pro)))
    for i in paint.l_pipes:
        l_pro = [i.name, i.n_i.name, i.n_f.name, i.diam, i.long, i.ks, i.C, i.n_m, i.kl, i.vis, i.t, i.v_t, i.bomb_a, i.bomb_b, i.bomb_c]
        l_names = ["name", "n_i", "n_f", "diam", "long", "ks", "C", "n_m", "kl", "vis", "t", "v_t", "bomb_a", "bomb_b", "bomb_c"]
        l_pipes.append(dict(zip(l_names, l_pro)))
    l_all = str(l_res) + "\n" + str(l_nodes) + "\n" + str(l_pipes)
    return l_all

class EasyDXF:
    def __init__(self, path):
        self.path = path

    def type_all(self, map):
        return [i.dxftype() for i in map]

    def read(self):
        draw = ezdxf.readfile(self.path)
        map = draw.modelspace()
        p_i = [i.dxf.start for i in map if i.dxftype() == 'LINE']
        p_f = [i.dxf.end for i in map if i.dxftype() == 'LINE']
        l_f = [list(i.get_points()) for i in map if i.dxftype() == 'LWPOLYLINE']
        z_r = [i.dxf.elevation for i in map if i.dxftype() == 'LWPOLYLINE']
        l_p = []
        for i in (p_i + p_f):
            if i not in l_p:
                l_p.append(i)
        print(l_p)
        index_r = []
        c_r = []
        l_res = []
        for k, i in enumerate(l_f):
            index = 0
            p_r = (min([j[0] for j in i]), min([j[1] for j in i]), z_r[k])
            l_p.remove(p_r)
            c_r.append(p_r)
            index_r.append(index)
            l_pro = ['R-'+str(k+1), z_r[k], p_r[0], p_r[1]]
            l_names = ["name", "level", "x", "y"]
            l_res.append(dict(zip(l_names, l_pro)))
        l_nodes = []
        for i, j in enumerate(l_p):
            l_pro = ['N-'+str(i+1), 0, j[2], 0, j[0], j[1]]
            l_names = ["name", "demand", "level", "height", "x", "y"]
            l_nodes.append(dict(zip(l_names, l_pro)))
        l_pipes = []
        l_points = l_res + l_nodes
        for k, (i, j) in enumerate(zip(p_i, p_f)):
            index_i = (c_r + l_p).index(i)
            index_f = (c_r + l_p).index(j)
            long = abs(complex(l_points[index_f]['x']-l_points[index_i]['x'],
                               l_points[index_f]['y'] - l_points[index_i]['y']))
            l_pro = ['T-'+str(k+1), l_points[index_i]['name'], l_points[index_f]['name'],
                     0, long, 0, 0, 0, 0, 0, 0, True,
                     0, 0, 0]
            l_names = ["name", "n_i", "n_f", "diam", "long", "ks", "C", "n_m", "kl", "vis", "t", "v_t", "bomb_a",
                       "bomb_b", "bomb_c"]
            l_pipes.append(dict(zip(l_names, l_pro)))
        return l_res, l_nodes, l_pipes

    def write(self, data: str):
        draw = ezdxf.new(dxfversion='AC1024')  # or use the AutoCAD release name ezdxf.new(dxfversion='R2010')
        modelS = draw.modelspace()
        data_l = data.split('\n')
        res = eval(data_l[0])
        node = eval(data_l[1])
        pipe = eval(data_l[2])
        for i in res:
            points = [(i['x'], i['y']),
                      (i['x'] + 10, i['y']),
                      (i['x']+10, i['y']+5),
                      (i['x'], i['y']+5)]
            modelS.add_lwpolyline(points, dxfattribs={'elevation':i['level']})
        c_points = [(i['x'], i['y'], i['level']) for i in (res + node)]
        l_name = [i['name'] for i in (res + node)]
        for i in pipe:
            index_i = l_name.index(i['n_i'])
            index_f = l_name.index(i['n_f'])
            p_i = c_points[index_i]
            p_f = c_points[index_f]
            modelS.add_line(p_i, p_f)
        draw.saveas(self.path)
def paint_All(l_res, l_nodes, l_pipes, paint):
    paint.scene_v.clear()
    for i in l_nodes:
        paint.paint_node(QPointF(i["x"], i["y"]))
    for i, j in zip(paint.l_nodes, l_nodes):
        i.name = j["name"]
        i.demand = j["demand"]
        i.level = j["level"]
        i.height = j["height"]
    for i in l_res:
        paint.paint_reservoir(QPointF(i["x"], i["y"]))
    for i, j in zip(paint.l_reservoir, l_res):
        i.name = j["name"]
        i.level = j["level"]
    l_names = [i["name"] for i in l_res + l_nodes]
    for i in l_pipes:
        index_i = l_names.index(i["n_i"])
        index_f = l_names.index(i["n_f"])
        points = paint.l_reservoir + paint.l_nodes
        p1 = QPointF(points[index_i].x, points[index_i].y)
        p2 = QPointF(points[index_f].x, points[index_f].y)
        paint.paint_pipe(p1, p2, points[index_i], points[index_f])
    for i, j in zip(paint.l_pipes, l_pipes):
        i.name = j["name"]
        i.long = j["long"]
        i.ks = j["ks"]
        i.C = j["C"]
        i.n_m = j["n_m"]
        i.kl = j["kl"]
        i.vis = j["vis"]
        i.t = j["t"]
        i.v_t = j["v_t"]
        i.bomb_a = j["bomb_a"]
        i.bomb_b = j["bomb_b"]
        i.bomb_c = j["bomb_c"]
