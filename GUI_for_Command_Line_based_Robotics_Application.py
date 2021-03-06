from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtCore import Qt
import subprocess
import rospy
import actionlib
from turtle_actionlib.msg import ShapeAction,ShapeGoal,ShapeResult
import time

class Ui_Form(object):
    
    count = 0
    trigger = 0
            
    def listview_clicked(self):
        item = self.listWidget.currentItem().text()
        self.kill_turtle.setEnabled(True)
        return item

    
    def list_preview_clicked(self):
        item = self.preview.currentItem().text()
        if(self.r1.isChecked()):
            nodes=subprocess.run(["rosnode","info",item],stdout=subprocess.PIPE)
            msg = QtWidgets.QMessageBox(Form)
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText(nodes.stdout.decode())
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
        elif(self.r2.isChecked()):
            nodes=subprocess.run(["rostopic","info",item],stdout=subprocess.PIPE)
            msg = QtWidgets.QMessageBox(Form)
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText(nodes.stdout.decode())
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
        elif(self.r3.isChecked()):
            nodes=subprocess.run(["rosservice","info",item],stdout=subprocess.PIPE)
            msg = QtWidgets.QMessageBox(Form)
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText(nodes.stdout.decode())
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
        elif(self.r4.isChecked()):
            nodes=subprocess.run(["rosmsg","info",item],stdout=subprocess.PIPE)
            msg = QtWidgets.QMessageBox(Form)
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            
            lineCnt = len(nodes.stdout.decode().split('\n'))
            if lineCnt > 15:
                scroll = QtWidgets.QScrollArea()
                scroll.setWidgetResizable(1)
                content = QtWidgets.QWidget()
                scroll.setWidget(content)
                
                layout = QtWidgets.QVBoxLayout(content)
                tmpLabel = QtWidgets.QLabel(nodes.stdout.decode())
                tmpLabel.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
                layout.addWidget(tmpLabel)
                msg.layout().addWidget(scroll, 0, 0,1, msg.layout().columnCount())
                scroll.setStyleSheet("QScrollArea{min-width:500 px; min-height: 400px}")
            else:
                msg.setText(nodes.stdout.decode())
                msg.setIcon(QtWidgets.QMessageBox.Information)
                
            
            msg.exec_()
    
    def roscore_pressed(self):
        subprocess.run(["gnome-terminal", "-x", "roscore"],shell=False)
        ros = QPixmap('roscore.jpg')
        self.animation.setPixmap(ros)
        self.animation.setAlignment(Qt.AlignCenter)
        self.kill.setEnabled(True)
        self.turtlesim.setEnabled(True)
        self.r1.setEnabled(True)
        self.r2.setEnabled(True)
        self.r3.setEnabled(True)
        self.r4.setEnabled(True)
        
    def killall_pressed(self):
        subprocess.run(["gnome-terminal", "-e", "killall -9 rosmaster"])
        self.kill.setEnabled(False)
        self.turtlesim.setEnabled(False)
        self.teleopt.setEnabled(False)
        self.spawn.setEnabled(False)
        self.clear.setEnabled(False)
        self.Toggle_Pen.setEnabled(False)
        self.kill_turtle.setEnabled(False)
        self.reset.setEnabled(False)
        self.teleport_absolute.setEnabled(False)
        self.teleport_relative.setEnabled(False)
        self.listWidget.setEnabled(False)
        self.Shape_server.setEnabled(False)
        self.client.setEnabled(False)
        self.left_change.setEnabled(False)
        self.right_change.setEnabled(False)
        self.shape_preview.setEnabled(False)
        self.textbox.setEnabled(False)
        self.text_shape.setEnabled(False)
        self.default.setEnabled(False)
        self.textbox_1.setEnabled(False)
        self.text_radius.setEnabled(False)
        self.r1.setEnabled(False)
        self.r2.setEnabled(False)
        self.r3.setEnabled(False)
        self.r4.setEnabled(False)
        blank = QPixmap('Blank.png')
        self.animation.setPixmap(blank)
        
    def turtlesim_node_pressed(self):
        turtlesim_node=False
        turtlesim_node = !turtlesim_node;
        if(turtlesim_node):
            subprocess.run(["gnome-terminal", "--tab","-e", "rosrun turtlesim turtlesim_node"])
            QtWidgets.QListWidgetItem('turtle1\t5.5\t5.5\t0', self.listWidget)
            self.teleopt.setEnabled(True)
            self.spawn.setEnabled(True)
            self.Toggle_Pen.setEnabled(True)
            self.reset.setEnabled(True)
            self.teleport_relative.setEnabled(True)
            self.teleport_absolute.setEnabled(True)
            self.clear.setEnabled(True)
            self.listWidget.setEnabled(True)
            self.Shape_server.setEnabled(True)
            self.client.setEnabled(True)
            #self.left_change.setEnabled(True)
            #self.right_change.setEnabled(True)
            self.default.setEnabled(True)
            self.shape_preview.setEnabled(True)
            self.textbox.setEnabled(True)
            self.text_shape.setEnabled(True)
            self.textbox_1.setEnabled(True)
            self.text_radius.setEnabled(True)
            subprocess.run(["gnome-terminal", "-x", "roscore"],shell=False)
            tur = QPixmap('turtlesim (4).jpg')
            self.animation.setPixmap(tur)
            self.animation.setAlignment(Qt.AlignCenter)
            turtlesim_node=False
            
    def teleopt_pressed(self):
        subprocess.run(["gnome-terminal", "-e", "rosrun turtlesim turtle_teleop_key"])
        self.movie = QMovie("gif_teleop.gif")
        self.animation.setMovie(self.movie)
        self.movie.start()
        
    def shapeserver_pressed(self):
        if self.Shape_server.isChecked() & self.trigger==0:
            subprocess.run(["gnome-terminal",'--tab', "-e", "rosrun turtle_actionlib shape_server"])
            self.defualt_pressed()
        if self.trigger==1 & self.Shape_server.isChecked() | self.Shape_server.isChecked() == False:
            time.sleep(2)
            self.Shape_server.isChecked()
        if self.Shape_server.isChecked()==False:
            subprocess.run(["gnome-terminal",'--tab', "-e", "rosrun turtle_actionlib shape_server"])
            self.trigger = self.trigger - 1
        

    def shapeclient_pressed(self):
        subprocess.run(["gnome-terminal","--tab","-e", "rosrun turtle_actionlib shape_client"])
        self.trigger = self.trigger + 1
        
    def shapeclient_goal_pressed(self):
        #if(self.default.isChecked()==False):
        rospy.init_node('shape_action')
        client = actionlib.SimpleActionClient('turtle_shape', ShapeAction)
        client.wait_for_server()
        goal = ShapeGoal()
        if(self.default.isChecked()==True):
            goal.edges=self.count+2
        elif(self.default.isChecked()==False):
            goal.edges=int(self.textbox.text())
        if self.textbox_1.text() == "":
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Enter valid radius")
                msg.exec()
        else:
            goal.radius=int(self.textbox_1.text())
            client.send_goal(goal)
            client.wait_for_result()
    
    def spawn_pressed(self):
        name0,done0 = QtWidgets.QInputDialog.getText(Form, 'Input Dialog', 'Enter x y t and name with a space to spawn')
        if(done0):
            subprocess.run(["gnome-terminal","--tab", "-e", "rosservice call /spawn "+name0])
            listwrite=name0.split()
            QtWidgets.QListWidgetItem(listwrite[3]+'\t'+listwrite[0]+'\t'+listwrite[1]+'\t'+listwrite[2], self.listWidget)
        
    def clear_pressed(self):
        subprocess.run(["gnome-terminal","--tab", "-e", "rosservice call /clear "])
        
    def removeSel(self):
        listItems=self.listWidget.selectedItems()
        if 'Name\t(initial)x\t(initial)y\t(initial)t' != self.listWidget.currentItem().text():
            if not listItems: return
            for item in listItems:
                self.listWidget.takeItem(self.listWidget.row(item))
    
    def increment(self):
        self.count = self.count + 1
        self.image_change()
        
    def decrement(self):
        self.count = self.count - 1
        self.image_change()
        
    def image_change(self):
        if self.count < 1:
            self.count = 8
            self.image_change()
            
        elif self.count == 1:
            self.left_change.setEnabled(True)
            pixmap_1 = QPixmap('triangle.png')
            self.shape_preview.setPixmap(pixmap_1) 
            self.shape_preview.setAlignment(Qt.AlignCenter)
            
        elif self.count == 2:
            self.left_change.setEnabled(True)
            self.right_change.setEnabled(True)
            pixmap_2 = QPixmap('square.png')
            self.shape_preview.setPixmap(pixmap_2) 
            self.shape_preview.setAlignment(Qt.AlignCenter)
            
        elif self.count==3:
            self.left_change.setEnabled(True)
            self.right_change.setEnabled(True)
            pixmap_3 = QPixmap('pentagon.png')
            self.shape_preview.setPixmap(pixmap_3)
            self.shape_preview.setAlignment(Qt.AlignCenter)
            
        elif self.count==4:
            self.left_change.setEnabled(True)
            self.right_change.setEnabled(True)
            pixmap_3 = QPixmap('hexagon.png')
            self.shape_preview.setPixmap(pixmap_3)
            self.shape_preview.setAlignment(Qt.AlignCenter)
            
        elif self.count==5:
            self.left_change.setEnabled(True)
            self.right_change.setEnabled(True)
            pixmap_3 = QPixmap('heptagon.png')
            self.shape_preview.setPixmap(pixmap_3)
            self.shape_preview.setAlignment(Qt.AlignCenter)
            
        elif self.count==6:
            self.left_change.setEnabled(True)
            self.right_change.setEnabled(True)
            pixmap_3 = QPixmap('octagon.png')
            self.shape_preview.setPixmap(pixmap_3)
            self.shape_preview.setAlignment(Qt.AlignCenter)
            
        elif self.count==7:
            self.left_change.setEnabled(True)
            self.right_change.setEnabled(True)
            pixmap_3 = QPixmap('nonagon.png')
            self.shape_preview.setPixmap(pixmap_3)
            self.shape_preview.setAlignment(Qt.AlignCenter)
        
        elif self.count==8:
            self.left_change.setEnabled(True)
            self.right_change.setEnabled(True)
            pixmap_3 = QPixmap('decagon.png')
            self.shape_preview.setPixmap(pixmap_3)
            self.shape_preview.setAlignment(Qt.AlignCenter)
            
        elif self.count > 8:
            self.count = 1
            self.image_change()
            
    def kill_turtle_pressed(self):
        item_kill=self.listview_clicked().split()
        subprocess.run(["gnome-terminal","--tab", "-e", "rosservice call /kill "+item_kill[0]])
        self.removeSel()
        if self.listWidget.count() <= 1:
            self.kill_turtle.setEnabled(False)
        
    def Toggle_Pen_pressed(self):
        name1,done1 = QtWidgets.QInputDialog.getText(Form, 'Input Dialog', 'Enter  red to be o or 1')
        
        if done1:
            name2,done2 = QtWidgets.QInputDialog.getText(Form, 'Input Dialog', 'Enter  green to be o or 1')
            if done2:
                name3,done3 = QtWidgets.QInputDialog.getText(Form, 'Input Dialog', 'Enter  blue to be o or 1')
                if done3:
                    name4,done4 = QtWidgets.QInputDialog.getText(Form, 'Input Dialog', 'Enter  width of pen')
                    if done4:
                        name5,done5 = QtWidgets.QInputDialog.getText(Form, 'Input Dialog', 'Enter  pen to be o or 1')
        if done1 and done2 and done3 and done4 and done5:
            subprocess.run(["gnome-terminal","--tab", "-e", "rosservice call /turtle1/set_pen "+name1+" "+name2+" "+name3+" "+name4+" "+name5])
    
    def teleport_absolute_pressed(self):
        name1,done1 = QtWidgets.QInputDialog.getText(Form, 'Input Dialog', 'Enter name of the turtle')
        x,done2 = QtWidgets.QInputDialog.getText(Form, 'Input Dialog', 'Enter  x')
        y,done3 = QtWidgets.QInputDialog.getText(Form, 'Input Dialog', 'Enter  y')
        theta,done4 = QtWidgets.QInputDialog.getText(Form, 'Input Dialog', 'Enter theta')
        if done1 and done2 and done3 and done4:
            subprocess.run(["gnome-terminal","--tab", "-e", "rosservice call /"+name1+"/teleport_absolute "+x+" "+y+" "+theta])

    def teleport_relative_pressed(self):
        name1,done1 = QtWidgets.QInputDialog.getText(Form, 'Input Dialog', 'Enter name of the turtle')
        linear,done2 = QtWidgets.QInputDialog.getText(Form, 'Input Dialog', 'Enter  linear')
        relative,done3 = QtWidgets.QInputDialog.getText(Form, 'Input Dialog', 'Enter  relative')
        if done1 and done2 and done3:
            subprocess.run(["gnome-terminal","--tab", "-e", "rosservice call /"+name1+"/teleport_relative "+linear+" "+relative])
    
    def reset_pressed(self):
        
        subprocess.run(["gnome-terminal","--tab", "-e", "rosservice call /reset "])
        self.listWidget.clear()
        QtWidgets.QListWidgetItem('Name\t(initial)x\t(initial)y\t(initial)t', self.listWidget)
        QtWidgets.QListWidgetItem('turtle1\t5.5\t5.5\t0', self.listWidget)
        
    def defualt_pressed(self):
        if(self.default.isChecked()):
            self.left_change.setEnabled(True)
            self.right_change.setEnabled(True)
            self.textbox.setEnabled(False)
        else:
            self.left_change.setEnabled(False)
            self.right_change.setEnabled(False)
            self.textbox.setEnabled(True)
            
    def r1_pressed(self):
        if(self.r1.isChecked()):
            self.preview.clear()
            r1_radio=subprocess.run(["rosnode","list"],stdout=subprocess.PIPE)
            entries = []
            entries=(r1_radio.stdout.decode().split('\n'))
            for i in entries:
                QtWidgets.QListWidgetItem(i, self.preview)
                
    def r2_pressed(self):
        if(self.r2.isChecked()):
            self.preview.clear()
            r2_radio=subprocess.run(["rostopic","list"],stdout=subprocess.PIPE)
            entries = []
            entries=(r2_radio.stdout.decode().split('\n'))
            for i in entries:
                QtWidgets.QListWidgetItem(i, self.preview)
                
    def r3_pressed(self):
        if(self.r3.isChecked()):
            self.preview.clear()
            r3_radio=subprocess.run(["rosservice","list"],stdout=subprocess.PIPE)
            entries = []
            entries=(r3_radio.stdout.decode().split('\n'))
            for i in entries:
                QtWidgets.QListWidgetItem(i, self.preview)
                
    def r4_pressed(self):
        if(self.r4.isChecked()):
            self.preview.clear()
            r4_radio=subprocess.run(["rosmsg","list"],stdout=subprocess.PIPE)
            entries = []
            entries=(r4_radio.stdout.decode().split('\n'))
            for i in entries:
                QtWidgets.QListWidgetItem(i, self.preview)
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(771, 623)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 5, 750, 610))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setStyleSheet("background-color : white")
        self.tabWidget.setStyleSheet("QTabWidget::tab-bar{alignment:center; }\n"
"QTabBar::tab{height:40px; width:108px; color:blue;font:15pt}\n"
);

        self.tab.setObjectName("tab")
        
        self.Rostitle = QtWidgets.QLabel(self.tab)
        #pixmap = QPixmap('ROS.png')
        #self.Rostitle.setPixmap(pixmap)
        self.movie = QMovie("ros_1.gif")
        self.Rostitle.setMovie(self.movie)
        self.movie.start()
        self.Rostitle.setAlignment(Qt.AlignCenter)
        self.Rostitle.setGeometry(QtCore.QRect(280, 20, 180, 100))
        self.Rostitle.setObjectName("Rostitle")
        
        self.animation = QtWidgets.QLabel(self.tab)
        self.animation.setGeometry(QtCore.QRect(50, 150, 650, 250))
        self.animation.setStyleSheet("background-color : white")
        self.animation.setStyleSheet("border: 1px solid black;")
        
        self.Roscore = QtWidgets.QPushButton(self.tab)
        self.Roscore.setFont(QtGui.QFont('Times', 15))
        self.Roscore.setStyleSheet("background-color : yellow")
        self.Roscore.clicked.connect(self.roscore_pressed)
        self.Roscore.setGeometry(QtCore.QRect(50, 420, 150, 41))
        self.Roscore.setObjectName("Roscore")

        self.kill = QtWidgets.QPushButton(self.tab)
        self.kill.setFont(QtGui.QFont('Times', 15))
        self.kill.setEnabled(False)
        self.kill.setStyleSheet("background-color : red")
        self.kill.clicked.connect(self.killall_pressed)
        self.kill.setGeometry(QtCore.QRect(300, 420, 150, 41))
        self.kill.setObjectName("kill")

        self.turtlesim = QtWidgets.QPushButton(self.tab)
        self.turtlesim.setFont(QtGui.QFont('Times',15))
        self.turtlesim.setEnabled(False)
        self.turtlesim.setStyleSheet("background-color : blue")
        self.turtlesim.clicked.connect(self.turtlesim_node_pressed)
        self.turtlesim.setGeometry(QtCore.QRect(550, 420, 150, 41))
        self.turtlesim.setObjectName("TurtleSim")

        self.teleopt = QtWidgets.QPushButton(self.tab)
        self.teleopt.setFont(QtGui.QFont('Times', 15))
        self.teleopt.setEnabled(False)
        self.teleopt.setStyleSheet("background-color : green")
        self.teleopt.clicked.connect(self.teleopt_pressed)
        self.teleopt.setGeometry(QtCore.QRect(300, 500, 150, 41))
        self.teleopt.setObjectName("teleopt")

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.spawn = QtWidgets.QPushButton(self.tab_2)
        self.spawn.clicked.connect(self.spawn_pressed)
        self.spawn.setFont(QtGui.QFont('Times', 15))
        self.spawn.setEnabled(False)
        self.spawn.setStyleSheet("background-color : green")
        self.spawn.setGeometry(QtCore.QRect(40, 40, 161, 31))
        self.spawn.setObjectName("spawn")

        self.Toggle_Pen = QtWidgets.QPushButton(self.tab_2)
        self.Toggle_Pen.setFont(QtGui.QFont('Times', 15))
        self.Toggle_Pen.setEnabled(False)
        self.Toggle_Pen.setStyleSheet("background-color : orange")
        self.Toggle_Pen.setGeometry(QtCore.QRect(420, 40, 151, 31))
        self.Toggle_Pen.setObjectName("Toggle_Pen")
        self.Toggle_Pen.clicked.connect(self.Toggle_Pen_pressed)

        self.kill_turtle = QtWidgets.QPushButton(self.tab_2)
        self.kill_turtle.setFont(QtGui.QFont('Times', 15))
        self.kill_turtle.setEnabled(False)
        self.kill_turtle.setStyleSheet("background-color : red")
        self.kill_turtle.setGeometry(QtCore.QRect(600, 250, 141, 31))
        self.kill_turtle.setObjectName("kill_turtle")
        self.kill_turtle.clicked.connect(self.kill_turtle_pressed)
        
        self.reset = QtWidgets.QPushButton(self.tab_2)
        self.reset.setFont(QtGui.QFont('Times', 15))
        self.reset.setEnabled(False)
        self.reset.setStyleSheet("background-color : yellow")
        self.reset.setGeometry(QtCore.QRect(240, 40, 141, 31))
        self.reset.setObjectName("reset")
        self.reset.clicked.connect(self.reset_pressed)

        self.clear = QtWidgets.QPushButton(self.tab_2)
        self.clear.setFont(QtGui.QFont('Times', 15))
        self.clear.setEnabled(False)
        self.clear.setStyleSheet("background-color : brown")
        self.clear.setGeometry(QtCore.QRect(600, 290, 141, 31))
        self.clear.setObjectName("clear")
        self.clear.clicked.connect(self.clear_pressed)

        self.teleport_absolute = QtWidgets.QPushButton(self.tab_2)
        self.teleport_absolute.setFont(QtGui.QFont('Times', 15))
        self.teleport_absolute.setEnabled(False)
        self.teleport_absolute.setStyleSheet("background-color : pink")
        self.teleport_absolute.setGeometry(QtCore.QRect(600, 170, 141, 31))
        self.teleport_absolute.setObjectName("teleport_absolute")
        self.teleport_absolute.clicked.connect(self.teleport_absolute_pressed)

        self.teleport_relative = QtWidgets.QPushButton(self.tab_2)
        self.teleport_relative.setFont(QtGui.QFont('Times', 15))
        self.teleport_relative.setEnabled(False)
        self.teleport_relative.setStyleSheet("background-color : orchid")
        self.teleport_relative.setGeometry(QtCore.QRect(600, 210, 141, 31))
        self.teleport_relative.setObjectName("teleport_relative")
        self.teleport_relative.clicked.connect(self.teleport_relative_pressed)
        
        self.listWidget = QtWidgets.QListWidget(self.tab_2)
        self.listWidget.setGeometry(QtCore.QRect(40, 130, 551, 391))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setEnabled(False)
        self.listWidget.setStyleSheet("background-color : white")
        self.listWidget.setStyleSheet("foreground-color : blue")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        QtWidgets.QListWidgetItem('Name\t(initial)x\t(initial)y\t(initial)t', self.listWidget)
        self.listWidget.clicked.connect(self.listview_clicked)
        
        self.Shape_server = QtWidgets.QCheckBox(self.tab_5)
        self.Shape_server.clicked.connect(self.shapeserver_pressed)
        self.Shape_server.setEnabled(False)
        self.Shape_server.setStyleSheet("background-color : blue")
        self.Shape_server.setGeometry(QtCore.QRect(300, 40, 131, 41))
        self.Shape_server.setObjectName("Shape_server")

        self.client = QtWidgets.QPushButton(self.tab_5)
        self.client.clicked.connect(self.shapeclient_goal_pressed)
        self.client.setEnabled(False)
        self.client.setStyleSheet("background-color : orange")
        self.client.setGeometry(QtCore.QRect(300, 500, 131, 41))
        self.client.setObjectName("client")
             
        self.left_change = QtWidgets.QPushButton(self.tab_5)
        self.left_change.setGeometry(80, 430, 50, 50)
        self.left_change.setEnabled(False)
        self.left_change.setStyleSheet("border-radius : 25; border : 2px solid yellow; background-color : yellow")
        self.left_change.clicked.connect(self.decrement)
        
        self.right_change = QtWidgets.QPushButton(self.tab_5)
        self.right_change.setGeometry(280, 430, 50, 50)
        self.right_change.setEnabled(False)
        self.right_change.setStyleSheet("border-radius : 25; border : 2px solid yellow; background-color : yellow")
        self.right_change.clicked.connect(self.increment)
        
        self.shape_preview = QtWidgets.QLabel(self.tab_5)
        self.shape_preview.setGeometry(QtCore.QRect(60, 180, 300, 230))
        sel = QPixmap('select.png')
        self.shape_preview.setPixmap(sel)
        self.shape_preview.setAlignment(Qt.AlignCenter)
        self.shape_preview.setEnabled(False)
        self.shape_preview.setStyleSheet("border: 5px solid white;")
        
        self.default = QtWidgets.QRadioButton(self.tab_5)
        self.default.setGeometry(300, 110, 131, 41)
        self.default.setStyleSheet("background-color : yellow")
        self.default.setEnabled(False)
        self.default.clicked.connect(self.defualt_pressed)
        
        self.textbox = QtWidgets.QLineEdit(self.tab_5)
        self.textbox.setEnabled(False)
        self.textbox.setStyleSheet("foreground-color : white");
        self.textbox.setGeometry(480, 210, 100, 30)
        
        self.text_shape = QtWidgets.QLabel(self.tab_5)
        sides = QPixmap('sides.png')
        self.text_shape.setPixmap(sides)
        self.text_shape.setEnabled(False)
        self.text_shape.setStyleSheet("foreground-color : white")
        self.text_shape.setGeometry(480, 160, 200, 60)
        
        self.textbox_1 = QtWidgets.QLineEdit(self.tab_5)
        self.textbox_1.setEnabled(False)
        self.textbox_1.setStyleSheet("foreground-color : white")
        self.textbox_1.setGeometry(480, 330, 100, 30)
        
        self.text_radius = QtWidgets.QLabel(self.tab_5)
        rad = QPixmap('radius.png')
        self.text_radius.setPixmap(rad)
        self.text_radius.setEnabled(False)
        self.text_radius.setStyleSheet("foreground-color : white")
        self.text_radius.setGeometry(480, 280, 200, 60)
        
        self.tabWidget.addTab(self.tab_5, "")
        
        self.tab_6 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_6, "")
        self.tab_6.setObjectName("tab_6")
        
        self.r1 = QtWidgets.QRadioButton(self.tab_6)
        self.r1.setGeometry(50, 40, 131, 30)
        self.r1.setStyleSheet("background-color : orange")
        self.r1.setEnabled(False)
        self.r1.clicked.connect(self.r1_pressed)
        
        self.r2 = QtWidgets.QRadioButton(self.tab_6)
        self.r2.setGeometry(230, 40, 131, 30)
        self.r2.setStyleSheet("background-color : yellow")
        self.r2.setEnabled(False)
        self.r2.clicked.connect(self.r2_pressed)
        
        self.r3 = QtWidgets.QRadioButton(self.tab_6)
        self.r3.setGeometry(405, 40, 131, 30)
        self.r3.setStyleSheet("background-color : lightgreen")
        self.r3.setEnabled(False)
        self.r3.clicked.connect(self.r3_pressed)
        
        self.r4 = QtWidgets.QRadioButton(self.tab_6)
        self.r4.setGeometry(570, 40, 131, 30)
        self.r4.setStyleSheet("background-color : violet")
        self.r4.setEnabled(False)
        self.r4.clicked.connect(self.r4_pressed)
        
#         pixmap_9 = QPixmap('background.jpg')
#         self.tab_2.setPixmap(pixmap_9)
#         self.tab_2.setStyleSheet("background-color : aqua")
#         self.tab_5.setStyleSheet("background-color : aqua")
#         self.tab_6.setStyleSheet("background-color : aqua")
#         self.tab.setStyleSheet("background-color : aqua")
        
        self.preview = QtWidgets.QListWidget(self.tab_6)
        self.preview.setObjectName("preview")
        self.preview.setGeometry(QtCore.QRect(60, 100, 630, 420))
        self.preview.setStyleSheet("border: 2px solid black;")
        self.preview.clicked.connect(self.list_preview_clicked)
        
        backg = QPixmap('background.jpg')
        
        self.picture = QtWidgets.QLabel(self.tab_5)
        self.picture.lower()
        self.picture.setPixmap(backg)
        self.picture.setGeometry(0,0, 750, 610)
        
        self.picture_1 = QtWidgets.QLabel(self.tab_6)
        self.picture_1.lower()
        self.picture_1.setPixmap(backg)
        self.picture_1.setGeometry(0,0, 750, 610)
        
        self.picture_2 = QtWidgets.QLabel(self.tab_2)
        self.picture_2.lower()
        self.picture_2.setPixmap(backg)
        self.picture_2.setGeometry(0,0, 750, 610)
        
        self.picture_3 = QtWidgets.QLabel(self.tab)
        self.picture_3.lower()
        self.picture_3.setPixmap(backg)
        self.picture_3.setGeometry(0,0, 750, 610)
        
        self.picture_4 = QtWidgets.QLabel(Form)
        self.picture_4.lower()
        self.picture_4.setPixmap(backg)
        self.picture_4.setGeometry(0,0, 771, 623)
        
        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Turtlesim_Simulation"))
        self.Roscore.setText(_translate("Form", "Roscore"))
        self.kill.setText(_translate("Form", "Kill Roscore"))
        self.turtlesim.setText(_translate("Form", "Launch Turtlesim"))
        self.teleopt.setText(_translate("Form", "Control Turtlebot"))
        self.left_change.setText(_translate("Form", "<"))
        self.right_change.setText(_translate("Form", ">"))
        self.default.setText(_translate("Form", "default shapes"))
        #self.text_shape.setText(_translate("Form", "Enter number of sides:"))
        #self.text_radius.setText(_translate("Form", "Enter radius:"))
        #self.shape_preview.setText(_translate("Form", "                            Select a Figure"))
        self.r1.setText(_translate("Form", "Nodes"))
        self.r2.setText(_translate("Form", "Topics"))
        self.r3.setText(_translate("Form", "Services"))
        self.r4.setText(_translate("Form", "Messages"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Topics"))
        self.spawn.setText(_translate("Form", "Spawn"))
        self.Toggle_Pen.setText(_translate("Form", "Toggle Pen"))
        self.kill_turtle.setText(_translate("Form", "Kill"))
        self.reset.setText(_translate("Form", "Reset"))
        self.clear.setText(_translate("Form", "Clear"))
        self.teleport_absolute.setText(_translate("Form", "Teleport_absolute"))
        self.teleport_relative.setText(_translate("Form", "Teleport_relative"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Services"))
        self.Shape_server.setText(_translate("Form", "Shape_server"))
        self.client.setText(_translate("Form", "Client"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Form", "Action"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("Form", "Lists"))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.setFixedSize(771,623)
    Form.show()
    sys.exit(app.exec_())
