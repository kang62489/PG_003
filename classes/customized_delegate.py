from PySide6.QtCore import Qt, QSize, QRect, QEvent
from PySide6.QtWidgets import (
    QStyledItemDelegate,
    QLineEdit,
    QStyleOptionButton,
    QStyle,
)

class CenterAlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter

class CellEditDelegate(QStyledItemDelegate):
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
        option.font.setFamily("Caliibri")

class CheckBoxSizeDelegate(QStyledItemDelegate):
    """Delegate to control checkbox size in QListView items"""
    def __init__(self, checkbox_size=20, parent=None):
        super().__init__(parent)
        self.checkbox_size = checkbox_size
    
    def paint(self, painter, option, index):
        """Paint custom-sized checkbox and text for list items"""
        # Get item's checkbox state (True/False)
        checked = index.model().data(index, Qt.CheckStateRole) == Qt.Checked
        text = index.model().data(index, Qt.DisplayRole)
        
        painter.save()
        
        # Draw selection background if selected
        # highlight() returns the system's standard highlight color (typically blue on Windows, blue/gray on macOS, I set purple on Windows)
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        
        # Get checkbox position
        checkbox_rect = self._getCheckboxRect(option.rect)
        
        # Draw custom-sized checkbox
        self._drawCheckbox(painter, option, checkbox_rect, checked)
        
        # Draw text next to checkbox
        text_rect = option.rect.adjusted(self.checkbox_size + 8, 0, 0, 0)
        text_color = option.palette.highlightedText().color() if option.state & QStyle.State_Selected else option.palette.text().color()
        painter.setPen(text_color)
        painter.drawText(text_rect, Qt.AlignVCenter, text)
        
        # Restore painter state
        painter.restore()
    
    def _drawCheckbox(self, painter, option, checkbox_rect, checked):
        """Helper method to draw a scaled checkbox"""
        # Save state for scaling
        painter.save()
        
        # Calculate center point of checkbox
        center_x = checkbox_rect.left() + checkbox_rect.width() / 2
        center_y = checkbox_rect.top() + checkbox_rect.height() / 2
        
        # Scale checkbox (default size is ~13px)
        # translate origin to center, scale, then translate back
        scale_factor = self.checkbox_size / 13.0
        painter.translate(center_x, center_y)
        painter.scale(scale_factor, scale_factor)
        painter.translate(-center_x, -center_y)
        
        # Create checkbox style options
        # QStyleOptionButton contains all the infomation that 
        # QStyle functions need to draw graphic elements like QPushbutton, QRadiobutton and QCheckBox.
        custom_checkbox_info = QStyleOptionButton()
        standard_size = 13
        custom_checkbox_info.rect = QRect(
            int(center_x - standard_size/2), 
            int(center_y - standard_size/2),
            standard_size, 
            standard_size
        )
        
        # Set checkbox state
        custom_checkbox_info.state = QStyle.State_Enabled
        custom_checkbox_info.state |= QStyle.State_On if checked else QStyle.State_Off
        
        # Draw the checkbox
        option.widget.style().drawPrimitive(QStyle.PE_IndicatorCheckBox, custom_checkbox_info, painter, option.widget)
        
        # Restore original scale
        painter.restore()
    
    def _getCheckboxRect(self, item_rect):
        """Calculate the rectangle for the checkbox"""
        # Horizontal: add 4 px margin from the left edge
        # Vertical: center the checkbox within the item height
        return QRect(
            item_rect.left() + 4, 
            item_rect.top() + (item_rect.height() - self.checkbox_size) // 2,
            self.checkbox_size, 
            self.checkbox_size
        )
    
    def editorEvent(self, event, model, option, index):
        """Handle mouse clicks on the checkbox"""
        # Check if item is checkable
        if not (index.flags() & Qt.ItemIsUserCheckable):
            return False
        
        # Only handle mouse events
        if event.type() not in (QEvent.MouseButtonRelease, QEvent.MouseButtonPress):
            return False
        
        # Check if click was on the checkbox
        checkbox_rect = self._getCheckboxRect(option.rect)
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
        return QSize(size.width(), max(size.height(), self.checkbox_size + 8))
