#!/usr/bin/env python3
"""Controller visualization widget

Displays TourBox Elite image with highlighting for selected controls.
"""

import logging
import os
from xml.etree import ElementTree as ET
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, Qt, QRectF, QByteArray
from PySide6.QtGui import QPainter
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtSvg import QSvgRenderer

logger = logging.getLogger(__name__)


class ControllerView(QWidget):
    """Widget to display TourBox controller with button highlighting"""

    # Signal emitted when user clicks on a control
    control_clicked = Signal(str)  # control name

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_control = None
        self._svg_renderer = None
        self._svg_path = None
        self._svg_data = None
        self._init_ui()
        self._load_svg()

    def _init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # SVG rendering widget
        self.svg_widget = SVGControllerWidget(self)
        self.svg_widget.setMinimumSize(400, 300)
        layout.addWidget(self.svg_widget)

    def _load_svg(self):
        """Load the TourBox SVG file"""
        # Get path to SVG file (relative to this module)
        self._svg_path = os.path.join(
            os.path.dirname(__file__),
            'assets',
            'tourbox_elite.svg'
        )

        if not os.path.exists(self._svg_path):
            logger.error(f"SVG file not found: {self._svg_path}")
            return

        # Load SVG data
        with open(self._svg_path, 'rb') as f:
            self._svg_data = f.read()

        # Load SVG renderer
        self._svg_renderer = QSvgRenderer(self._svg_path)
        if not self._svg_renderer.isValid():
            logger.error(f"Invalid SVG file: {self._svg_path}")
            self._svg_renderer = None
            return

        # Pass renderer and data to the widget
        self.svg_widget.set_svg_data(self._svg_renderer, self._svg_data)
        logger.info(f"Loaded SVG from: {self._svg_path}")

    def highlight_control(self, control_name: str):
        """Highlight a specific control on the image

        Args:
            control_name: Name of the control to highlight (e.g., 'side', 'knob_cw')
        """
        self._current_control = control_name
        self.svg_widget.set_highlighted_control(control_name)
        logger.debug(f"Highlighted control: {control_name}")

    def clear_highlight(self):
        """Clear the current highlight"""
        self._current_control = None
        self.svg_widget.set_highlighted_control(None)
        logger.debug("Cleared highlight")


class SVGControllerWidget(QWidget):
    """Custom widget for rendering SVG with control highlighting"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._base_renderer = None
        self._highlight_renderer = None
        self._svg_data = None
        self._highlighted_control = None
        self.setMinimumSize(400, 300)

    def set_svg_data(self, renderer: QSvgRenderer, svg_data: bytes):
        """Set the SVG renderer and raw data"""
        self._base_renderer = renderer
        self._svg_data = svg_data
        self.update()

    def set_highlighted_control(self, control_name: str):
        """Set which control to highlight"""
        self._highlighted_control = control_name

        # Create a renderer with the selected control visible
        if control_name and self._svg_data:
            try:
                # Parse SVG and make the control visible
                modified_svg = self._make_control_visible(self._svg_data, control_name)
                if modified_svg:
                    self._highlight_renderer = QSvgRenderer(QByteArray(modified_svg))
                else:
                    self._highlight_renderer = None
            except Exception as e:
                logger.error(f"Failed to create highlight renderer: {e}")
                self._highlight_renderer = None
        else:
            self._highlight_renderer = None

        self.update()

    def _make_control_visible(self, svg_data: bytes, control_id: str) -> bytes:
        """Modify SVG to show only the specified control"""
        try:
            # Register namespaces to preserve them
            ET.register_namespace('', 'http://www.w3.org/2000/svg')
            ET.register_namespace('inkscape', 'http://www.inkscape.org/namespaces/inkscape')
            ET.register_namespace('sodipodi', 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd')

            root = ET.fromstring(svg_data)

            # Find the control element by ID
            control_elem = root.find(f".//*[@id='{control_id}']")

            if control_elem is None:
                logger.warning(f"Control element '{control_id}' not found in SVG")
                return None

            # Simply change the control's style from hidden to visible
            current_style = control_elem.get('style', '')

            # Remove display:none or set display:inline
            if 'display:none' in current_style:
                new_style = current_style.replace('display:none', 'display:inline')
                control_elem.set('style', new_style)
            elif 'display' not in current_style:
                # No display property, add it
                control_elem.set('style', current_style + ';display:inline' if current_style else 'display:inline')
            else:
                # Has display property but not none, just make sure it's inline
                control_elem.set('style', current_style.replace('display:inline', 'display:inline'))

            # Convert back to bytes
            return ET.tostring(root, encoding='utf-8')

        except Exception as e:
            logger.error(f"Failed to modify SVG: {e}")
            return None

    def paintEvent(self, event):
        """Paint the SVG with highlighting"""
        if not self._base_renderer:
            # Show placeholder if no SVG loaded
            painter = QPainter(self)
            painter.fillRect(self.rect(), Qt.lightGray)
            painter.drawText(
                self.rect(),
                Qt.AlignCenter,
                "TourBox Elite\n(SVG not found)"
            )
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # Calculate scaling to fit widget while maintaining aspect ratio
        svg_size = self._base_renderer.defaultSize()
        widget_size = self.size()

        scale_x = widget_size.width() / svg_size.width()
        scale_y = widget_size.height() / svg_size.height()
        scale = min(scale_x, scale_y)

        # Calculate centered position
        scaled_width = svg_size.width() * scale
        scaled_height = svg_size.height() * scale
        x = (widget_size.width() - scaled_width) / 2
        y = (widget_size.height() - scaled_height) / 2

        target_rect = QRectF(x, y, scaled_width, scaled_height)

        # Render base SVG (shows background, controls layer is hidden)
        self._base_renderer.render(painter, target_rect)

        # Render highlight overlay (shows only the selected control)
        if self._highlight_renderer:
            self._highlight_renderer.render(painter, target_rect)
