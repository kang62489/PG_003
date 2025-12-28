from PySide6.QtCore import QEvent, QRect, QSize, Qt
from PySide6.QtWidgets import (
    QLineEdit,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionButton,
)


class DelegateCenterAlign(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


class DelegateAlignRightCenter(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignRight | Qt.AlignVCenter


class DelegateCellEdit(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        editor.setText(value)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.EditRole)

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignHCenter | Qt.AlignVCenter
        option.font.setFamily("Calibri")


class DelegateCheckableListItem(QStyledItemDelegate):
    """Delegate to control text positioning in QListView items"""

    def __init__(self, text_margin=30, parent=None):
        super().__init__(parent)
        self.text_margin = text_margin  # Space between checkbox and text

    def paint(self, painter, option, index):
        """Paint text for list items with proper spacing"""
        # Get item data
        checked = index.model().data(index, Qt.CheckStateRole) == Qt.Checked
        text = index.model().data(index, Qt.DisplayRole)

        painter.save()

        # Draw selection background if selected
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        # Create a style option for the checkbox
        checkOption = QStyleOptionButton()
        checkOption.rect = QRect(
            option.rect.left() + 4,
            option.rect.top() + (option.rect.height() - 40) // 2,
            40,
            40,
        )
        checkOption.state = QStyle.State_Enabled
        if checked:
            checkOption.state |= QStyle.State_On
        else:
            checkOption.state |= QStyle.State_Off

        # Draw the checkbox using the widget's style
        option.widget.style().drawControl(
            QStyle.CE_CheckBox,
            checkOption,
            painter,
            option.widget,
        )

        # Draw text with proper spacing
        # The 40px is the checkbox width from QSS
        text_rect = option.rect.adjusted(40 + self.text_margin, 0, 0, 0)
        text_color = (
            option.palette.highlightedText().color()
            if option.state & QStyle.State_Selected
            else option.palette.text().color()
        )
        painter.setPen(text_color)
        painter.drawText(text_rect, Qt.AlignVCenter, text)

        painter.restore()

    def editorEvent(self, event, model, option, index):
        """Handle mouse clicks on the checkbox"""
        # Check if item is checkable
        if not (index.flags() & Qt.ItemIsUserCheckable):
            return False

        # Only handle mouse events
        if event.type() not in (QEvent.MouseButtonRelease, QEvent.MouseButtonPress):
            return False

        # Create a rect for the checkbox (40px from QSS)
        checkbox_rect = QRect(
            option.rect.left() + 4,
            option.rect.top() + (option.rect.height() - 40) // 2,
            40,
            40,
        )

        # Check if click was on the checkbox
        if not checkbox_rect.contains(event.pos()):
            return False

        # Toggle checkbox on mouse release
        if event.type() == QEvent.MouseButtonRelease:
            current_state = index.data(Qt.CheckStateRole)
            new_state = 0 if current_state == Qt.Checked else 2  # 0=Unchecked, 2=Checked
            return model.setData(index, new_state, Qt.CheckStateRole)

        return True

    def sizeHint(self, option, index):
        """Ensure item height accommodates the checkbox"""
        # Add 8px to the space around the checkbox for padding
        size = super().sizeHint(option, index)
        return QSize(
            size.width(),
            max(size.height(), 40 + 8),
        )  # 40px checkbox + 8px padding
