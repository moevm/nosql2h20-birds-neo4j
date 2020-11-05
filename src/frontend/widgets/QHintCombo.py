from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QCompleter, QComboBox
from idna import unicode


class QHintCombo(QComboBox):
    def __init__(self, items=None, parent=None):
        super(QHintCombo, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)
        self.completer = QCompleter(self)

        # always show all completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setPopup(self.view())
        self.setCompleter(self.completer)

        self.lineEdit().textEdited[unicode].connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)
        if items:
            self.setItems(items)

    def setModel(self, model):
        super(QHintCombo, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(QHintCombo, self).setModelColumn(column)

    def view(self):
        return self.completer.popup()

    def index(self):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)

    def setItems(self, arr):
        model = QStandardItemModel()
        for i, word in enumerate(arr):
            item = QStandardItem(word)
            model.setItem(i, 0, item)
        self.setModel(model)
        self.setModelColumn(0)
        self.show()

