from krita import QVBoxLayout, QPushButton, QWidget, QLayout, QWidgetItem, QRect, QSize,QPoint
from PyQt5 import QtCore

class CollapsibleBoxLayout(QVBoxLayout):
   def __init__(self, title="", parent=None):
       super(CollapsibleBoxLayout, self).__init__(parent)

       self.toggle_button = QPushButton(text=title, checkable=True, checked=False)
       self.toggle_button.clicked.connect(self.on_pressed)
       self.toggle_button.setChecked(False)

       self.content_area = QWidget()

       self.addWidget(self.toggle_button)
       self.addWidget(self.content_area)
       self.setSpacing(0)

       self.content_area.setVisible(False)
       
   def on_pressed(self):
       checked = self.toggle_button.isChecked()
       if checked:
           self.toggle_button.setChecked(True)
           self.content_area.setVisible(True)
       if not checked:
           self.toggle_button.setChecked(False)
           self.content_area.setVisible(False)
       
   def setContentLayout(self, layout):
       lay = self.content_area.layout()
       del lay
       self.content_area.setLayout(layout)
       
   def resizeEvent(self, event):
       self.content_area.setMaximumHeight((self.content_area.layout().heightForWidth(self.width())))
       return super(CollapsibleBoxLayout, self).resizeEvent(event)
   
   
class FlowLayout(QLayout):
   """Custom layout that mimics the behaviour of a flow layout"""

   def __init__(self, parent=None, margin=0, spacing=2):
       """
       Create a new FlowLayout instance.
       This layout will reorder the items automatically.
       @param parent (QWidget)
       @param margin (int)
       @param spacing (int)
       """
       super(FlowLayout, self).__init__(parent)
       # Set margin and spacing
       self.parent_flag = True
       if parent is not None: 
           self.setMargin(margin)
       else:
           self.parent_flag = False
       self.setSpacing(spacing)

       self.itemList = []

   def __del__(self):
       """Delete all the items in this layout"""
       item = self.takeAt(0)
       while item:
           item = self.takeAt(0)

   def addItem(self, item):
       """Add an item at the end of the layout.
       This is automatically called when you do addWidget()
       item (QWidgetItem)"""
       self.itemList.append(item)

   def count(self):
       """Get the number of items in the this layout
       @return (int)"""
       return len(self.itemList)

   def itemAt(self, index):
       """Get the item at the given index
       @param index (int)
       @return (QWidgetItem)"""
       if index >= 0 and index < len(self.itemList):
           return self.itemList[index]
       return None

   def takeAt(self, index):
       """Remove an item at the given index
       @param index (int)
       @return (None)"""
       if index >= 0 and index < len(self.itemList):
           return self.itemList.pop(index)
       return None

   def insertWidget(self, index, widget):
       """Insert a widget at a given index
       @param index (int)
       @param widget (QWidget)"""
       item = QWidgetItem(widget)
       self.itemList.insert(index, item)

   def expandingDirections(self):
       """This layout grows only in the horizontal dimension"""
       return QtCore.Qt.Orientations(QtCore.Qt.Horizontal)

   def hasHeightForWidth(self):
       """If this layout's preferred height depends on its width
       @return (boolean) Always True"""
       return True

   def heightForWidth(self, width):
       """Get the preferred height a layout item with the given width
       @param width (int)"""
       height = self.doLayout(QRect(0, 0, width, 0), True)
       return height

   def setGeometry(self, rect):
       """Set the geometry of this layout
       @param rect (QRect)"""
       super(FlowLayout, self).setGeometry(rect)
       self.doLayout(rect, False)

   def sizeHint(self):
       """Get the preferred size of this layout
       @return (QSize) The minimum size"""
       return self.minimumSize()

   def minimumSize(self):
       """Get the minimum size of this layout
       @return (QSize)"""
       # Calculate the size
       size = QSize()
       for item in self.itemList:
           size = size.expandedTo(item.minimumSize())
       if self.parent_flag:
            # Add the margins
            size += QSize(2 * self.margin(), 2 * self.margin())
       
       return size

   def doLayout(self, rect, testOnly):
       """Layout all the items
       @param rect (QRect) Rect where in the items have to be laid out
       @param testOnly (boolean) Do the actual layout"""
       x = rect.x()
       y = rect.y()
       lineHeight = 0

       for item in self.itemList:
           wid = item.widget()
           spaceX = self.spacing()
           spaceY = self.spacing()
           nextX = x + item.sizeHint().width() + spaceX
           if nextX - spaceX > rect.right() and lineHeight > 0:
               x = rect.x()
               y = y + lineHeight + spaceY
               nextX = x + item.sizeHint().width() + spaceX
               lineHeight = 0

           if not testOnly:
               item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

           x = nextX
           lineHeight = max(lineHeight, item.sizeHint().height())

       return y + lineHeight - rect.y()