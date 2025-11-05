#!/usr/bin/env python3
"""Control editor widget

Allows editing of individual control actions with modifiers, keys, and action types.
"""

import logging
from typing import Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QLineEdit, QGroupBox, QButtonGroup
)
from PySide6.QtCore import Signal, Qt
from evdev import ecodes as e

logger = logging.getLogger(__name__)

# Character to keycode mapping for symbols and special characters
CHAR_TO_KEYCODE = {
    # Symbols (both shifted and unshifted)
    '=': 'EQUAL',
    '+': 'EQUAL',  # Shift+=
    '-': 'MINUS',
    '_': 'MINUS',  # Shift+-
    '[': 'LEFTBRACE',
    '{': 'LEFTBRACE',  # Shift+[
    ']': 'RIGHTBRACE',
    '}': 'RIGHTBRACE',  # Shift+]
    ';': 'SEMICOLON',
    ':': 'SEMICOLON',  # Shift+;
    "'": 'APOSTROPHE',
    '"': 'APOSTROPHE',  # Shift+'
    ',': 'COMMA',
    '<': 'COMMA',  # Shift+,
    '.': 'DOT',
    '>': 'DOT',  # Shift+.
    '/': 'SLASH',
    '?': 'SLASH',  # Shift+/
    '\\': 'BACKSLASH',
    '|': 'BACKSLASH',  # Shift+\
    '`': 'GRAVE',
    '~': 'GRAVE',  # Shift+`
    '1': '1',
    '!': '1',  # Shift+1
    '2': '2',
    '@': '2',  # Shift+2
    '3': '3',
    '#': '3',  # Shift+3
    '4': '4',
    '$': '4',  # Shift+4
    '5': '5',
    '%': '5',  # Shift+5
    '6': '6',
    '^': '6',  # Shift+6
    '7': '7',
    '&': '7',  # Shift+7
    '8': '8',
    '*': '8',  # Shift+8
    '9': '9',
    '(': '9',  # Shift+9
    '0': '0',
    ')': '0',  # Shift+0
}

# Special keys that can't be reliably typed
SPECIAL_KEYS = {
    'None': None,
    '--- Control Keys ---': None,
    'Enter': e.KEY_ENTER,
    'Escape': e.KEY_ESC,
    'Tab': e.KEY_TAB,
    'Space': e.KEY_SPACE,
    'Backspace': e.KEY_BACKSPACE,
    'Delete': e.KEY_DELETE,
    'Insert': e.KEY_INSERT,
    'Context Menu': e.KEY_CONTEXT_MENU,
    '--- Arrow Keys ---': None,
    'Up': e.KEY_UP,
    'Down': e.KEY_DOWN,
    'Left': e.KEY_LEFT,
    'Right': e.KEY_RIGHT,
    '--- Navigation ---': None,
    'Home': e.KEY_HOME,
    'End': e.KEY_END,
    'Page Up': e.KEY_PAGEUP,
    'Page Down': e.KEY_PAGEDOWN,
    '--- Zoom Keys ---': None,
    'Zoom Reset': e.KEY_ZOOMRESET,
    'Zoom In': e.KEY_ZOOMIN,
    'Zoom Out': e.KEY_ZOOMOUT,
    '--- Function Keys ---': None,
    'F1': e.KEY_F1, 'F2': e.KEY_F2, 'F3': e.KEY_F3, 'F4': e.KEY_F4,
    'F5': e.KEY_F5, 'F6': e.KEY_F6, 'F7': e.KEY_F7, 'F8': e.KEY_F8,
    'F9': e.KEY_F9, 'F10': e.KEY_F10, 'F11': e.KEY_F11, 'F12': e.KEY_F12,
}


class ControlEditor(QWidget):
    """Widget for editing a control's action"""

    # Signal emitted when user changes the action
    action_changed = Signal(str, str)  # control_name, action_string

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_control = None
        self._init_ui()

    def _init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)

        # Header
        self.header_label = QLabel("Edit Control")
        self.header_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.header_label)

        # Control name display
        self.control_label = QLabel("No control selected")
        self.control_label.setStyleSheet("font-size: 12px; color: #666;")
        layout.addWidget(self.control_label)

        # Action type selection
        action_type_layout = QHBoxLayout()
        action_type_layout.addWidget(QLabel("Action Type:"))
        self.action_type_combo = QComboBox()
        self.action_type_combo.addItems(["Keyboard", "Mouse Wheel", "None"])
        self.action_type_combo.currentTextChanged.connect(self._on_action_type_changed)
        action_type_layout.addWidget(self.action_type_combo)
        action_type_layout.addStretch()
        layout.addLayout(action_type_layout)

        # Keyboard action group
        self.keyboard_group = QGroupBox("Keyboard Action")
        keyboard_layout = QVBoxLayout(self.keyboard_group)

        # Modifiers
        mod_label = QLabel("Modifiers:")
        keyboard_layout.addWidget(mod_label)

        mod_layout = QHBoxLayout()
        self.ctrl_btn = QPushButton("Ctrl")
        self.ctrl_btn.setCheckable(True)
        self.ctrl_btn.setMaximumWidth(80)
        mod_layout.addWidget(self.ctrl_btn)

        self.alt_btn = QPushButton("Alt")
        self.alt_btn.setCheckable(True)
        self.alt_btn.setMaximumWidth(80)
        mod_layout.addWidget(self.alt_btn)

        self.shift_btn = QPushButton("Shift")
        self.shift_btn.setCheckable(True)
        self.shift_btn.setMaximumWidth(80)
        mod_layout.addWidget(self.shift_btn)

        self.super_btn = QPushButton("Super")
        self.super_btn.setCheckable(True)
        self.super_btn.setMaximumWidth(80)
        mod_layout.addWidget(self.super_btn)

        mod_layout.addStretch()
        keyboard_layout.addLayout(mod_layout)

        # Key input
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("Key:"))

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Type a character (a-z, 0-9, symbols)")
        self.key_input.setMaxLength(1)
        self.key_input.setMaximumWidth(200)
        self.key_input.textChanged.connect(self._on_key_input_changed)
        key_layout.addWidget(self.key_input)

        key_layout.addWidget(QLabel("or"))

        self.special_key_combo = QComboBox()
        for key_name in SPECIAL_KEYS.keys():
            self.special_key_combo.addItem(key_name)
            # Disable separator items
            if SPECIAL_KEYS[key_name] is None:
                idx = self.special_key_combo.count() - 1
                self.special_key_combo.model().item(idx).setEnabled(False)
        self.special_key_combo.setMaximumWidth(150)
        self.special_key_combo.currentTextChanged.connect(self._on_special_key_changed)
        key_layout.addWidget(self.special_key_combo)

        key_layout.addStretch()
        keyboard_layout.addLayout(key_layout)

        layout.addWidget(self.keyboard_group)

        # Mouse wheel action group
        self.mouse_group = QGroupBox("Mouse Wheel Action")
        mouse_layout = QVBoxLayout(self.mouse_group)

        mouse_dir_layout = QHBoxLayout()
        mouse_dir_layout.addWidget(QLabel("Direction:"))
        self.mouse_direction_combo = QComboBox()
        self.mouse_direction_combo.addItems([
            "Vertical Up",
            "Vertical Down",
            "Horizontal Left",
            "Horizontal Right"
        ])
        mouse_dir_layout.addWidget(self.mouse_direction_combo)
        mouse_dir_layout.addStretch()
        mouse_layout.addLayout(mouse_dir_layout)

        layout.addWidget(self.mouse_group)
        self.mouse_group.hide()  # Hidden by default

        # Buttons
        button_layout = QHBoxLayout()
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self._on_apply)
        button_layout.addWidget(self.apply_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        layout.addStretch()

        # Initially disabled
        self.setEnabled(False)

    def load_control(self, control_name: str, current_action: str):
        """Load a control for editing

        Args:
            control_name: Name of the control (e.g., 'side', 'knob_cw')
            current_action: Current action string (e.g., 'KEY_LEFTCTRL+KEY_C')
        """
        self.current_control = control_name
        self.control_label.setText(f"Editing: {control_name}")
        self.setEnabled(True)

        # Parse current action and populate UI
        self._parse_and_populate(current_action)

        logger.info(f"Loaded control for editing: {control_name}")

    def _parse_and_populate(self, action_str: str):
        """Parse action string and populate UI fields

        Args:
            action_str: Action string like 'KEY_LEFTCTRL+KEY_C' or 'REL_WHEEL:1'
        """
        # Reset UI
        self.ctrl_btn.setChecked(False)
        self.alt_btn.setChecked(False)
        self.shift_btn.setChecked(False)
        self.super_btn.setChecked(False)
        self.key_input.clear()
        self.special_key_combo.setCurrentIndex(0)

        if not action_str or action_str == "(none)" or action_str == "(unmapped)":
            self.action_type_combo.setCurrentText("None")
            return

        # Check if it's a mouse wheel action (handle both raw and human-readable formats)
        if action_str.startswith("Wheel "):
            self.action_type_combo.setCurrentText("Mouse Wheel")
            # Parse direction from human-readable format
            if "Up" in action_str:
                self.mouse_direction_combo.setCurrentText("Vertical Up")
            elif "Down" in action_str:
                self.mouse_direction_combo.setCurrentText("Vertical Down")
            elif "Left" in action_str:
                self.mouse_direction_combo.setCurrentText("Horizontal Left")
            elif "Right" in action_str:
                self.mouse_direction_combo.setCurrentText("Horizontal Right")
            return
        elif action_str.startswith("WHEEL:") or action_str.startswith("HWHEEL:"):
            # Legacy format support
            self.action_type_combo.setCurrentText("Mouse Wheel")
            if action_str.startswith("WHEEL:"):
                value = int(action_str.split(":")[1])
                if value > 0:
                    self.mouse_direction_combo.setCurrentText("Vertical Up")
                else:
                    self.mouse_direction_combo.setCurrentText("Vertical Down")
            elif action_str.startswith("HWHEEL:"):
                value = int(action_str.split(":")[1])
                if value > 0:
                    self.mouse_direction_combo.setCurrentText("Horizontal Right")
                else:
                    self.mouse_direction_combo.setCurrentText("Horizontal Left")
            return

        # It's a keyboard action
        self.action_type_combo.setCurrentText("Keyboard")

        # Parse key combination
        parts = action_str.split("+")
        for part in parts:
            part = part.strip()
            part_upper = part.upper()
            if "CTRL" in part_upper:
                self.ctrl_btn.setChecked(True)
            elif "ALT" in part_upper:
                self.alt_btn.setChecked(True)
            elif "SHIFT" in part_upper:
                self.shift_btn.setChecked(True)
            elif "META" in part_upper or "SUPER" in part_upper:
                self.super_btn.setChecked(True)
            else:
                # It's the actual key
                # Check if it's a single character (letter, number, or symbol)
                if len(part) == 1:
                    # It's a character - put it in text field
                    self.key_input.setText(part.lower())
                else:
                    # It's a special key name - try to match in special keys dropdown
                    # First try exact match, then try without spaces/underscores/case-insensitive
                    found = False
                    part_normalized = part.lower().replace(' ', '').replace('_', '')

                    for i in range(self.special_key_combo.count()):
                        item_text = self.special_key_combo.itemText(i)
                        item_normalized = item_text.lower().replace(' ', '').replace('_', '')

                        # Try exact match first
                        if item_text.lower() == part.lower():
                            self.special_key_combo.setCurrentIndex(i)
                            found = True
                            break
                        # Try normalized match (no spaces or underscores)
                        elif item_normalized == part_normalized:
                            self.special_key_combo.setCurrentIndex(i)
                            found = True
                            break

                    if not found:
                        # Unknown key, leave dropdown at None
                        logger.warning(f"Could not parse key: {part}")
                        self.special_key_combo.setCurrentIndex(0)

    def _on_action_type_changed(self, action_type: str):
        """Handle action type change"""
        if action_type == "Keyboard":
            self.keyboard_group.show()
            self.mouse_group.hide()
        elif action_type == "Mouse Wheel":
            self.keyboard_group.hide()
            self.mouse_group.show()
        else:  # None
            self.keyboard_group.hide()
            self.mouse_group.hide()

    def _on_key_input_changed(self, text: str):
        """Handle key input text change - clear special key dropdown"""
        if text:
            self.special_key_combo.setCurrentIndex(0)

    def _on_special_key_changed(self, key_name: str):
        """Handle special key dropdown change - clear text input"""
        if key_name and key_name != "None" and SPECIAL_KEYS.get(key_name) is not None:
            self.key_input.clear()

    def _on_apply(self):
        """Handle Apply button click"""
        if not self.current_control:
            return

        # Build action string
        action_str = self._build_action_string()
        logger.info(f"Apply: {self.current_control} -> {action_str}")

        # Emit signal
        self.action_changed.emit(self.current_control, action_str)

    def _build_action_string(self) -> str:
        """Build action string from current UI state

        Returns:
            Action string like 'KEY_LEFTCTRL+KEY_C' or 'REL_WHEEL:1'
        """
        action_type = self.action_type_combo.currentText()

        if action_type == "None":
            return "none"

        if action_type == "Mouse Wheel":
            direction = self.mouse_direction_combo.currentText()
            if direction == "Vertical Up":
                return "REL_WHEEL:1"
            elif direction == "Vertical Down":
                return "REL_WHEEL:-1"
            elif direction == "Horizontal Left":
                return "REL_HWHEEL:-1"
            elif direction == "Horizontal Right":
                return "REL_HWHEEL:1"

        # Keyboard action
        parts = []

        # Add modifiers
        if self.ctrl_btn.isChecked():
            parts.append("KEY_LEFTCTRL")
        if self.alt_btn.isChecked():
            parts.append("KEY_LEFTALT")
        if self.shift_btn.isChecked():
            parts.append("KEY_LEFTSHIFT")
        if self.super_btn.isChecked():
            parts.append("KEY_LEFTMETA")

        # Add key
        if self.key_input.text():
            # Convert character to KEY_ code
            char = self.key_input.text()

            # Check if it's a symbol/special character
            if char in CHAR_TO_KEYCODE:
                key_name = CHAR_TO_KEYCODE[char]
                parts.append(f"KEY_{key_name}")
            else:
                # Regular letter (a-z) - just uppercase it
                parts.append(f"KEY_{char.upper()}")
        elif self.special_key_combo.currentText() != "None":
            key_name = self.special_key_combo.currentText()
            if SPECIAL_KEYS.get(key_name):
                # Find the KEY_ constant name
                for name, code in e.__dict__.items():
                    if name.startswith('KEY_') and code == SPECIAL_KEYS[key_name]:
                        parts.append(name)
                        break

        return "+".join(parts) if parts else "none"
