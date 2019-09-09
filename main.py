import sys
from WaterHID import water_net
from paint import Paint
from SecondWins import *


class Root(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('GraHID')
        self.mdiArea = QMdiArea(self)
        # self.setStyleSheet(dark_style)
        # ------- ICON CONFIGURATION ------- #
        self.setCentralWidget(self.mdiArea)
        self.setWindowIcon(QIcon('Images/main.ico'))
        # ------ INITIAL DATA ------ #
        self.preferences_data = [3, 25, '0.001', 1]
        self.viewData = [[8, [255, 0, 0]], [1, [0, 100, 0]],
                         [0, 0, 0, QFont('MS Shell Dlg 2', 8, 50, False), 'N', 'T', 'R'], [0, 1, 0], [250, 250, 205]]
        self.default_data = [['0', '200', '254', '0.00006'], [0, 0, [0, '1.14e-06'], [1, '15'], [1, '100']]]
        self.summary_data = [0, 0, 0, 0, 0, 0, '', '']  # #nodos  # tubs  #Bombas  # Res  # Flow units
        # ------ CURSOR ---------#
        self.bar_cursor = QCursor(QPixmap('Images/index.png'))
        self.nod_cursor = QCursor(QPixmap('Images/nod_cursor.png'))
        self.bomb_cursor = QCursor(QPixmap('Images/bomb_cursor.png'))
        # ------ STATUS BAR --------#
        self.statusBar()
        # ------ ACTIONS IN MENU BAR -------#
        self.menu_bar = self.menuBar()
        self.fileMenu = self.menu_bar.addMenu('&Archivo')
        self.newAction = QAction(QIcon('Images/new.png'), 'Nuevo', self)
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.triggered.connect(self.new_project)
        self.newAction.setStatusTip('Crea un nuevo proyecto.')
        self.openAction = QAction(QIcon('Images/open.png'), 'Abrir', self)
        self.openAction.triggered.connect(self.open_project)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Abre un proyecto existente.')
        self.saveAction = QAction(QIcon('Images/save.png'), 'Guardar', self)
        self.saveAction.triggered.connect(self.save_project)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Guarda el proyecto actual.')
        self.importAction = QAction('Importar', self)
        self.importAction.setShortcut('Ctrl+I')
        self.importAction.setStatusTip('Importa data externa al programa.')
        self.importAction.triggered.connect(self.import_project)
        self.exportAction = QAction('Exportar', self)
        self.exportAction.setShortcut('Ctrl+E')
        self.exportAction.setStatusTip('Exporta data a programas externos.')
        self.exportAction.triggered.connect(self.export_project)
        self.preferencesAction = QAction('Preferencias', self)
        self.preferencesAction.triggered.connect(self.preferencesFunction)
        self.preferencesAction.setStatusTip('Configura las propiedades iniciales del proyecto.')
        self.closeAction = QAction('Salir', self)
        self.closeAction.setShortcut('Alt+X')
        self.closeAction.triggered.connect(self.close)
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.importAction)
        self.fileMenu.addAction(self.exportAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.preferencesAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.closeAction)
        self.viewMenu = self.menu_bar.addMenu('&Ver')
        self.optionsAction = QAction('Opciones', self)
        self.optionsAction.setStatusTip('Configura las opciones de visualización del ventana del proyecto.')
        self.optionsAction.triggered.connect(self.viewOptions)
        self.viewMenu.addAction(self.optionsAction)
        self.projectMenu = self.menu_bar.addMenu('&Proyecto')
        self.summaryAction = QAction(QIcon('Images/resumen.png'), 'Resumen', self)
        self.summaryAction.triggered.connect(self.summary_win)
        self.summaryAction.setStatusTip('Visualiza los valores iniciales para el análisis.')
        self.defaultAction = QAction('Valores por defecto', self)
        self.defaultAction.setStatusTip('Configura las opciones hidráulicas del proyecto.')
        self.defaultAction.triggered.connect(self.defaultOptions)
        self.calculateAction = QAction(QIcon('Images/run3.png'), 'Iniciar Análisis', self)
        self.calculateAction.triggered.connect(self.calculate_all)
        self.calculateAction.setStatusTip('Inicia con el análisis y/o cálculo del proyecto.')
        self.dataAction = QAction(QIcon('Images/tables.png'), 'Datos', self)
        self.dataAction.setStatusTip('Visualiza y configura los datos iniciales del proyecto.')
        self.dataAction.triggered.connect(self.properties_win)
        self.projectMenu.addAction(self.dataAction)
        self.projectMenu.addAction(self.summaryAction)
        self.projectMenu.addAction(self.defaultAction)
        self.projectMenu.addSeparator()
        self.projectMenu.addAction(self.calculateAction)
        self.informMenu = self.menu_bar.addMenu('&Informe')
        self.completeAction = QAction('Completo', self)
        self.completeAction.setStatusTip('Visualiza los resultados generales del analisis del proyecto.')
        self.iterationsAction = QAction(QIcon('Images/iter.png'), 'Iteraciones', self)
        self.iterationsAction.setStatusTip('Visualiza todas las iteraciones realizadas por el programa.')
        self.graphActions = QAction(QIcon('Images/graph.png'), 'Gráficas', self)
        self.graphActions.setStatusTip('Visualiza los gráficos resultantes del proyecto.')
        self.tablesMenu = QMenu('Tablas', self)
        self.resultsAction = QAction(QIcon('Images/tables.png'), 'Resultados', self)
        self.resultsAction.setStatusTip('Visualiza las tablas resultantes del proyecto.')
        self.resultsAction.triggered.connect(self.viewResults)
        self.tablesMenu.addAction(self.resultsAction)
        self.informMenu.addAction(self.completeAction)
        self.informMenu.addAction(self.iterationsAction)
        self.informMenu.addSeparator()
        self.informMenu.addAction(self.graphActions)
        self.informMenu.addMenu(self.tablesMenu)
        self.helpMenu = self.menu_bar.addMenu('A&yuda')
        self.helpAction = QAction(QIcon('Images/help.png'), r'Acerca de...', self)
        self.helpAction.setStatusTip('Visualiza el contenido de ayuda y datos del programador.')
        self.helpMenu.addAction(self.helpAction)
        # ------ ACTIONS IN TOOLBAR -------#
        self.tool_bar_1 = self.addToolBar('Estandar')
        self.tool_bar_1.addAction(self.newAction)
        self.tool_bar_1.addAction(self.openAction)
        self.tool_bar_1.addAction(self.saveAction)
        self.tool_bar_1.addSeparator()
        self.tool_bar_1.addAction(self.calculateAction)
        self.tool_bar_1.addSeparator()
        self.tool_bar_1.addAction(self.summaryAction)
        self.tool_bar_1.addAction(self.iterationsAction)
        self.tool_bar_1.addAction(self.graphActions)
        self.tool_bar_1.addAction(self.resultsAction)
        self.tool_bar_1.addSeparator()
        self.tool_bar_1.addAction(self.helpAction)
        #self.tool_bar_1.addAction(self.reAction)
        # ------ BUTTONS IN TOOLBAR -------#
        self.nod_button = QToolButton(self)
        self.nod_button.setIcon(QIcon('Images/nod.png'))
        self.nod_button.setCheckable(True)
        self.nod_button.clicked.connect(self.is_node)
        self.nod_button.setStatusTip('Dibuja un nodo.')
        self.pipe_button = QToolButton(self)
        self.pipe_button.setIcon(QIcon('Images/bar.png'))
        self.pipe_button.setCheckable(True)
        self.pipe_button.clicked.connect(self.is_pipe)
        self.pipe_button.setStatusTip('Dibuja una conexion o Tubería entre Nodos.')
        self.sel_button = QToolButton(self)
        self.sel_button.setIcon(QIcon('Images/cursor.png'))
        self.sel_button.setCheckable(True)
        self.sel_button.clicked.connect(self.is_select)
        self.sel_button.setStatusTip('Selecciona  un elemento para ver y/o modificar sus propiedades')
        self.sel_area_button = QToolButton(self)
        self.sel_area_button.setIcon(QIcon('Images/area_s.png'))
        self.sel_area_button.setCheckable(True)
        self.sel_area_button.clicked.connect(self.is_select_area)
        self.sel_area_button.setStatusTip('Selecciona  varios elementos para eliminar o mover')
        self.bomb_button = QToolButton(self)
        self.bomb_button.setIcon(QIcon('Images/bomb.png'))
        self.bomb_button.clicked.connect(self.is_bomb)
        self.bomb_button.setCheckable(True)
        self.bomb_button.setStatusTip('Agrega una bomba seleccionando una tubería')
        self.res_button = QToolButton(self)
        self.res_button.setIcon(QIcon('Images/reser.png'))
        self.res_button.setCheckable(True)
        self.res_button.clicked.connect(self.is_reservoir)
        self.move_button = QToolButton(self)
        self.move_button.setIcon(QIcon('Images/move_el.png'))
        self.move_button.setStatusTip('Mueva un item manteniedo pulsado sobre ella y moviendo el cursor.')
        self.move_button.setCheckable(True)
        #self.move_button.clicked.connect(self.isMove)
        self.b_toolbar = QToolBar(self)
        self.b_toolbar.setWindowTitle('Elementos')
        self.b_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(Qt.LeftToolBarArea, self.b_toolbar)
        self.b_toolbar.addWidget(self.sel_button)
        self.b_toolbar.addWidget(self.move_button)
        self.b_toolbar.addWidget(self.sel_area_button)
        self.b_toolbar.addSeparator()
        self.b_toolbar.addWidget(self.nod_button)
        self.b_toolbar.addWidget(self.pipe_button)
        self.b_toolbar.addWidget(self.res_button)
        self.b_toolbar.addWidget(self.bomb_button)
        self.paint = None
        self.new_project()
        self.win_show_results = WinResults(self, self.paint)
        self.mdiArea.tileSubWindows()
        self.routeFile = ""

    def is_node(self):
        if not self.paint.is_node:
            self.paint.is_node = True
        else:
            self.paint.is_node = False
        self.paint.is_pipe = False
        self.pipe_button.setChecked(False)
        self.paint.is_select = False
        self.sel_button.setChecked(False)
        self.paint.is_move = False
        self.move_button.setChecked(False)
        self.paint.is_area_select = False
        self.sel_area_button.setChecked(False)
        self.paint.is_reservoir = False
        self.res_button.setChecked(False)
        self.paint.is_bomb = False
        self.bomb_button.setChecked(False)

    def is_pipe(self):
        if not self.paint.is_pipe:
            self.paint.is_pipe = True
        else:
            self.paint.is_pipe = False
        self.paint.is_node = False
        self.nod_button.setChecked(False)
        self.paint.is_select = False
        self.sel_button.setChecked(False)
        self.paint.is_move = False
        self.move_button.setChecked(False)
        self.paint.is_area_select = False
        self.sel_area_button.setChecked(False)
        self.paint.is_reservoir = False
        self.res_button.setChecked(False)
        self.paint.is_bomb = False
        self.bomb_button.setChecked(False)

    def is_select(self):
        if not self.paint.is_select:
            self.paint.is_select = True
            self.sel_button.setChecked(True)
        else:
            self.paint.is_select = False
        self.paint.is_node = False
        self.nod_button.setChecked(False)
        self.paint.is_pipe = False
        self.pipe_button.setChecked(False)
        self.paint.is_move = False
        self.move_button.setChecked(False)
        self.paint.is_area_select = False
        self.sel_area_button.setChecked(False)
        self.paint.is_reservoir = False
        self.res_button.setChecked(False)
        self.paint.is_bomb = False
        self.bomb_button.setChecked(False)

    def is_select_area(self):
        if not self.paint.is_area_select:
            self.paint.is_area_select = True
        else:
            self.paint.is_area_select = False
        self.paint.is_node = False
        self.nod_button.setChecked(False)
        self.paint.is_pipe = False
        self.pipe_button.setChecked(False)
        self.paint.is_move = False
        self.move_button.setChecked(False)
        self.paint.is_select = False
        self.sel_button.setChecked(False)
        self.paint.is_reservoir = False
        self.res_button.setChecked(False)
        self.paint.is_bomb = False
        self.bomb_button.setChecked(False)

    def is_reservoir(self):
        if not self.paint.is_reservoir:
            self.paint.is_reservoir = True
        else:
            self.paint.is_reservoir = False
        self.paint.is_node = False
        self.nod_button.setChecked(False)
        self.paint.is_pipe = False
        self.pipe_button.setChecked(False)
        self.paint.is_move = False
        self.move_button.setChecked(False)
        self.paint.is_select = False
        self.sel_button.setChecked(False)
        self.paint.is_area_select = False
        self.sel_area_button.setChecked(False)
        self.paint.is_bomb = False
        self.bomb_button.setChecked(False)

    def is_bomb(self):
        if not self.paint.is_bomb:
            self.paint.is_bomb = True
        else:
            self.paint.is_bomb = False
        self.paint.is_node = False
        self.nod_button.setChecked(False)
        self.paint.is_pipe = False
        self.pipe_button.setChecked(False)
        self.paint.is_move = False
        self.move_button.setChecked(False)
        self.paint.is_select = False
        self.sel_button.setChecked(False)
        self.paint.is_area_select = False
        self.sel_area_button.setChecked(False)
        self.paint.is_reservoir = False
        self.res_button.setChecked(False)

    def new_project(self):


        self.paint = Paint(self.viewData, self)
        self.mdiArea.addSubWindow(self.paint)
        self.changedViewOptions()
        self.paint.show()

    def save_project(self):
        file, cond = QFileDialog.getSaveFileName(self, "Guardar", self.routeFile, "All Files (*);;Archivo WaterHID (*.wh)")
        if cond:
            self.routeFile = file
            l_all = graphToStr(self.paint)
            file_p = open(self.routeFile, "w")
            file_p.write(l_all)
            file_p.close()

    def import_project(self):
        file, cond = QFileDialog.getOpenFileName(self, "Abrir", self.routeFile, "All Files (*);;AutoCAD (*.dxf)")
        if cond:
            self.routeFile = file
            file_to_import = EasyDXF(file)
            l_res, l_nodes, l_pipes = file_to_import.read()
            paint_All(l_res, l_nodes, l_pipes, self.paint)

    def export_project(self):
        file, cond = QFileDialog.getSaveFileName(self, "Exportar...", self.routeFile, "All Files (*);;AutoCAD (*.dxf)")
        if cond:
            self.routeFile = file
            l_all = graphToStr(self.paint)
            file_to_export = EasyDXF(file)
            file_to_export.write(l_all)

    def open_project(self):
        file, cond = QFileDialog.getOpenFileName(self, "Abrir", self.routeFile, "All Files (*);; Archivo WaterHID (*wh)")
        if cond:
            self.routeFile = file
            file_o = open(self.routeFile, "r")
            a = file_o.readlines()
            l_res = eval(a[0])
            l_nodes = eval(a[1])
            l_pipes = eval(a[2])
            paint_All(l_res, l_nodes, l_pipes, self.paint)

    def calculate_all(self):
        show_text_default(self.paint)
        self.changedViewOptions()
        if len(self.paint.l_pipes):
            n_i = [i.n_i for i in self.paint.l_pipes]
            n_f = [i.n_f for i in self.paint.l_pipes]
            for i in self.paint.l_nodes:
                if i not in n_i and i not in n_f:
                    return QMessageBox.warning(self, 'Error', 'There are untied knots.\nExisten nudos sin unir.')
            eq = ['D-W', 'H-W', 'C-M'][self.default_data[1][1]]
            error, i_max = float(self.preferences_data[2]), float(self.preferences_data[1])
            if self.default_data[1][4][0]:
                flow_i = float(self.default_data[1][4][1])/1000
            else:
                flow_i = sum([i.demand for i in self.paint.l_nodes])/len(self.paint.l_nodes)
            for i in self.paint.l_pipes:
                i.flow = flow_i
            try:
                cond, res = water_net(self.paint.l_pipes, self.paint.l_nodes, self.paint.l_reservoir, self.statusBar(), eq=eq, error=error, i_max=i_max)
                if cond:
                    QMessageBox.information(self, 'Success', ' It was executed successfully')
                    put_text(self.paint.l_pipes, self.paint.l_nodes, self.paint.l_reservoir, eq.lower(), self.preferences_data[0])
                    self.win_show_results.show()
                else:
                    QMessageBox.information(self, 'Error', 'There was an error during the execution')
                    show_text_default(self.paint)
                    #self.win_show_results.hide()
            except ZeroDivisionError:
                show_text_default(self.paint)
        else:
            #self.win_show_results.hide()
            QMessageBox.warning(self, 'Error', "Don't exist any pipe")

    def preferencesFunction(self):
        win_preferences = Preferences(self.preferences_data)
        win_preferences.exec_()
        self.preferences_data = win_preferences.data
        if self.preferences_data[3]:
            self.default_data[1][2][0] = 1
            self.default_data[1][3][0] = 0
        else:
            self.default_data[1][2][0] = 0
            self.default_data[1][3][0] = 1

    def viewOptions(self):
        winViewOptions = ViewOptions(self.viewData)
        winViewOptions.exec_()
        self.viewData = winViewOptions.data
        self.changedViewOptions()
        show_text_default(self.paint)

    def viewResults(self):
        self.win_show_results.hide()
        win = ResultsView(self, self.paint)
        win.exec_()
        self.win_show_results.show()

    def changedViewOptions(self):
        self.paint.setStyleSheet('QGraphicsView {background-color: %s }' % QColor(self.viewData[4][0],
                                                                                  self.viewData[4][1],
                                                                                  self.viewData[4][2]).name())
        self.paint.node_color = QColor(self.viewData[0][1][0], self.viewData[0][1][1], self.viewData[0][1][2])
        self.paint.node_size = self.viewData[0][0]
        self.paint.pipe_color = QColor(self.viewData[1][1][0], self.viewData[1][1][1], self.viewData[1][1][2])
        self.paint.pipe_width = self.viewData[1][0]
        self.paint.text_font = self.viewData[2][3]
        self.paint.text_visible_node = bool(self.viewData[2][0])
        self.paint.text_visible_pipe = bool(self.viewData[2][1])
        self.paint.text_visible_res = bool(self.viewData[2][2])
        old_text_node = self.paint.pref_node
        old_text_pipe = self.paint.pref_pipe
        old_text_res = self.paint.pref_res
        self.paint.pref_node = self.viewData[2][4]
        self.paint.pref_pipe = self.viewData[2][5]
        self.paint.pref_res = self.viewData[2][6]
        for item in self.paint.scene_v.items():
            if item.type() == 4:
                item.setPen(self.paint.node_color)
                item.setBrush(QBrush(self.paint.node_color, Qt.SolidPattern))
                #QGraphicsEllipseItem.rect()
                e = QPointF(self.paint.l_nodes[self.paint.l_i_nodes.index(item)].x,
                            self.paint.l_nodes[self.paint.l_i_nodes.index(item)].y)
                item.setRect(e.x()-self.paint.node_size/2, e.y()-self.paint.node_size/2, self.paint.node_size,
                             self.paint.node_size)
            if item.type() == 6:
                pen = QPen(self.paint.pipe_color)
                pen.setWidth(self.paint.pipe_width)
                item.setPen(pen)
            if item.type() == 8:
                item.setFont(self.paint.text_font)
                if self.paint.text_visible_node and item in self.paint.text_node:
                    text = item.toPlainText().replace(old_text_node, self.paint.pref_node)
                    item.setPlainText(text)
                    item.show()
                elif self.paint.text_visible_pipe and item in self.paint.text_pipe:
                    text = item.toPlainText()
                    text = text.replace(old_text_pipe, self.paint.pref_pipe)
                    item.setPlainText(text)
                    item.show()
                elif self.paint.text_visible_res and item in self.paint.text_res:
                    text = item.toPlainText()
                    text = text.replace(old_text_res, self.paint.pref_res)
                    item.setPlainText(text)
                    item.show()
                else:
                    item.hide()

    def defaultOptions(self):
        win_default = DefaultValues(self.default_data)
        win_default.exec_()
        self.default_data = win_default.data
        self.preferences_data[3] = self.default_data[1][2][0]
        for i in self.paint.l_pipes:
            if self.default_data[1][1] == 0:
                i.ks = float(self.default_data[0][3])
            elif self.default_data[1][1] == 1:
                i.C = float(self.default_data[0][3])
            elif self.default_data[1][1] == 2:
                i.n_m = float(self.default_data[0][3])

    def properties_win(self):
        win_properties = PropertiesData(self, self.paint, self.default_data[1][1])
        win_properties.exec_()

    def summary_win(self):
        self.summary_data[0] = len(self.paint.l_nodes)
        self.summary_data[1] = len(self.paint.l_pipes)
        self.summary_data[2] = 0
        self.summary_data[3] = len(self.paint.l_reservoir)
        self.summary_data[4] = 'm3s'
        self.summary_data[5] = 'd-w'
        win_summary = SummaryWindow(self.summary_data, self.paint)

        win_summary.exec_()
        self.summary_data = win_summary.data


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Root()
    win.show()
    app.setStyle(QStyleFactory.create("Fusion"))
    app.exec_()
