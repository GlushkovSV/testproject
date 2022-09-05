import sys
import math
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtSql
from pyqtgraph import PlotWidget
from myform import Ui_MainWindow


def theor_calc(param):
    Gravitation_Param = 398_600_000_000_000

    Fly_Time = param['Fly_Time']
    Start_Orbit_Height = param['Start_Orbit_Height']
    Start_Orbit_Inclination = param['Start_Orbit_Inclination']
    Finally_Orbit_Height = param['Finally_Orbit_Height']
    Finally_Orbit_Inclination = param['Finally_Orbit_Inclination']
    Start_SC_Mass = param['Start_SC_Mass']
    Realitive_Construct_Mass = param['Realitive_Construct_Mass']
    SSS_Realitive_Mass = param['SSS_Realitive_Mass']
    Gas_Flow_Speed = param['Gas_Flow_Speed']
    Engine_Specific_Mass = param['Engine_Specific_Mass']
    Electro_Specific_Mass = param['Electro_Specific_Mass']
    EFFICIENCY = param['EFFICIENCY'] 

    Start_Orbit_Radius = (6371 + Start_Orbit_Height) * 1000
    Finnaly_Orbit_Radius = (6371 + Finally_Orbit_Height) * 1000
    Initial_Speed = math.sqrt(Gravitation_Param / Start_Orbit_Radius)
    Delta_velocity = Initial_Speed * math.sqrt(
        1 - 2 * math.sqrt(Start_Orbit_Radius / Finnaly_Orbit_Radius) *
        math.cos((math.pi / 2) * (Finally_Orbit_Inclination - Start_Orbit_Inclination)) +
        (Start_Orbit_Radius / Finnaly_Orbit_Radius)
    )
    Gas_Mass = Start_SC_Mass * (
            1 - math.exp((-Delta_velocity) / Gas_Flow_Speed)
    )
    Engines_Thrust = (Gas_Flow_Speed * Gas_Mass) / Fly_Time
    Engines_Power = (Engines_Thrust * Gas_Flow_Speed) / (2 * EFFICIENCY)
    Construct_Mass = Realitive_Construct_Mass * Start_SC_Mass
    Engines_Mass = Engine_Specific_Mass * Engines_Thrust
    Electro_Mass = Electro_Specific_Mass * Engines_Power
    SSS_Mass = SSS_Realitive_Mass * Gas_Mass
    Payload_Mass = (Start_SC_Mass
                         - Gas_Mass
                         - Construct_Mass
                         - SSS_Mass
                         - Engines_Mass
                         - Electro_Mass)
    foo = Gas_Mass / (3 * math.pi)
    Tank_Radius = 100 * round(pow(foo, 1 / 3))
    Tank_CTR = round(Tank_Radius * 1.5)
    Body_lenght = round(500 * pow(Construct_Mass, 1 / 3))
    SP_Square = 0.5 * Engines_Power / (1.3 * 0.29 * 0.866)
    Payload_R = round(math.sqrt(Payload_Mass / (0.02 * 1.5 * math.pi)))
    EnginesCount = round(Engines_Thrust)

    res = dict()
    res['Initial_Speed'] = Initial_Speed
    res['Gas_Flow_Speed'] = Gas_Flow_Speed
    res['Electro_Mass'] = Electro_Mass
    res['Payload_Mass'] = Payload_Mass
    res['SSS_Mass'] = SSS_Mass
    res['Engines_Mass'] = Engines_Mass
    res['Construct_Mass'] = Construct_Mass
    res['Engines_Power'] = Engines_Power
    res['Gas_Mass'] = Gas_Mass
    res['Engines_Thrust'] = Engines_Thrust
    res['Delta_velocity'] = Delta_velocity
    res['EFFICIENCY'] = EFFICIENCY
    return res


class mywindow(QtWidgets.QMainWindow):
    def __init__(self, model):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableView.setModel(model)
        self.ui.pushButton.clicked.connect(self.calc)
        self.ui.pushButton_2.clicked.connect(self.MSG)

    def MSG(self):
        messg = QtWidgets.QMessageBox()
        messg.setWindowTitle("О Программе")
        messg.setText("Хайруллин И.И.")
        x = messg.exec_()

    def read_data_field(self):
        Fly_Time = float(self.ui.lineEdit.text()) * 86400
        Start_Orbit_Height = float(self.ui.lineEdit_4.text())
        Start_Orbit_Inclination = float(self.ui.lineEdit_6.text()) * math.pi / 180
        Finally_Orbit_Height = float(self.ui.lineEdit_5.text())
        Finally_Orbit_Inclination = float(self.ui.lineEdit_7.text()) * math.pi / 180
        Start_SC_Mass = float(self.ui.lineEdit_2.text())
        Realitive_Construct_Mass = float(self.ui.lineEdit_12.text())
        SSS_Realitive_Mass = float(self.ui.lineEdit_11.text())
        Gas_Flow_Speed = float(self.ui.lineEdit_8.text())
        Engine_Specific_Mass = float(self.ui.lineEdit_9.text())
        Electro_Specific_Mass = float(self.ui.lineEdit_10.text())
        EFFICIENCY = float(self.ui.lineEdit_3.text())
        EFFICIENCY *= 0.01

        res = dict()

        res['Fly_Time'] = Fly_Time
        res['Start_Orbit_Height'] = Start_Orbit_Height
        res['Start_Orbit_Inclination'] = Start_Orbit_Inclination
        res['Finally_Orbit_Height'] = Finally_Orbit_Height
        res['Finally_Orbit_Inclination'] = Finally_Orbit_Inclination
        res['Start_SC_Mass'] = Start_SC_Mass
        res['Realitive_Construct_Mass'] = Realitive_Construct_Mass
        res['SSS_Realitive_Mass'] = SSS_Realitive_Mass
        res['Gas_Flow_Speed'] = Gas_Flow_Speed
        res['Engine_Specific_Mass'] = Engine_Specific_Mass
        res['Electro_Specific_Mass'] = Electro_Specific_Mass
        res['EFFICIENCY'] = EFFICIENCY
        return res

    def outres(self, res):
        self.ui.lineEdit_3.setText(str(res['EFFICIENCY'] * 100))
        self.ui.lineEdit_8.setText(str(round(res['Gas_Flow_Speed'], 3)))
        self.ui.lineEdit_18.setText(str(round(res['Electro_Mass'], 3)))
        self.ui.lineEdit_22.setText(str(round(res['Payload_Mass'], 3)))
        self.ui.lineEdit_21.setText(str(round(res['SSS_Mass'], 3)))
        self.ui.lineEdit_19.setText(str(round(res['Engines_Mass'], 3)))
        self.ui.lineEdit_20.setText(str(round(res['Construct_Mass'], 3)))
        self.ui.lineEdit_17.setText(str(round(res['Engines_Power']) / 1000))
        self.ui.lineEdit_16.setText(str(round(1000 * res['Engines_Thrust'] / 9.81, 3)))
        self.ui.lineEdit_15.setText(str(round(res['Gas_Mass'])))
        self.ui.lineEdit_14.setText(str(round(res['Delta_velocity']) / 1000))
        self.ui.lineEdit_13.setText(str(round(res['Initial_Speed'], 3) / 1000))

    def calc(self):
        par = self.read_data_field()
        res = theor_calc(par)
        self.outres(res)


def main():
    app = QtWidgets.QApplication([])
    db = QtSql.QSqlDatabase.addDatabase("QODBC")
    db.setDatabaseName(
        "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};FIL={MS Access};DSN='';DBQ=./engine.mdb")
    if not db.open():
        print('error db open')
        messg = QtWidgets.QMessageBox()
        messg.setWindowTitle("Ошибка открытия Базы Данных")
        messg.setText(str(db.lastError))
        x = messg.exec_()
        sys.exit(-1)
    model = QtSql.QSqlTableModel()
    model.setTable("engine")
    model.select()

    application = mywindow(model)
    application.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()



