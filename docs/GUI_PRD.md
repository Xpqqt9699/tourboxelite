# Product Requirements Document: TourBox Elite Configuration GUI

## 1. Overview

### 1.1 Purpose
Create a graphical user interface application for Linux that allows users to configure button mappings and application-specific profiles for the TourBox Elite controller.

### 1.2 Background
The TourBox Elite Linux driver currently requires users to manually edit INI configuration files to customize button mappings and create application-specific profiles. The official TourBox software on Windows and macOS provides a full-featured GUI for this purpose. Linux users expect similar functionality for feature parity.

### 1.3 Goals
- Provide an intuitive visual interface for configuring TourBox Elite button mappings
- Match feature parity with official Windows/Mac TourBox software
- Eliminate need for manual config file editing
- Enable real-time visual feedback when interacting with the physical device
- Support application-specific profile creation and management

## 2. Target Audience

### 2.1 Primary Users
- Creative professionals using TourBox Elite on Linux
- Users migrating from Windows/Mac who expect a GUI configuration tool
- Linux users who prefer graphical tools over command-line/text editing

### 2.2 User Characteristics
- Familiar with desktop applications
- May or may not be comfortable with terminal/text editors
- Want quick, visual configuration without reading documentation

## 3. Functional Requirements

### 3.1 Application Lifecycle Management

**REQ-3.1.1: Auto-stop Driver on Launch**
- When GUI launches, automatically stop the TourBox driver service
- Command: `systemctl --user stop tourbox`
- Display status indicator showing driver is stopped

**REQ-3.1.2: Auto-restart Driver on Exit**
- When GUI closes (window close or quit), automatically restart the driver
- Command: `systemctl --user start tourbox`
- Ensure restart happens even on abnormal exit where possible

**REQ-3.1.3: BLE Connection**
- Connect to TourBox Elite via Bluetooth Low Energy after stopping driver
- Use existing Bleak library and BLE configuration from driver codebase
- Display connection status (connected/disconnected)
- Handle connection errors gracefully with user-friendly messages

### 3.2 Configuration File Management

**REQ-3.2.1: Load Configuration**
- Read existing configuration from `~/.config/tourbox/mappings.conf`
- Parse all profiles and button mappings
- Handle malformed config files gracefully with error messages

**REQ-3.2.2: Save Configuration**
- Write updated configuration back to `~/.config/tourbox/mappings.conf`
- Preserve config file format and comments where possible
- Create backup of config before writing changes
- Validate configuration before saving

**REQ-3.2.3: Configuration Validation**
- Validate key combinations are valid
- Ensure all required controls are mapped in each profile
- Warn user of potential issues before saving

### 3.3 Real-time Input Detection

**REQ-3.3.1: Physical Button Detection**
- Listen for BLE notifications from TourBox Elite
- Detect which button/dial/scroll was pressed or rotated
- Map BLE event codes to control names using existing button code mappings

**REQ-3.3.2: Visual Feedback**
- Highlight the corresponding control in the visual controller image
- Scroll to and select the control in the controls list
- Load the control's configuration into the edit area
- Provide clear visual indication of which control is active

### 3.4 Profile Management

**REQ-3.4.1: Profile List Display**
- Display all available profiles in a list
- Indicate currently selected profile
- Show profile names clearly
- Default profile always present and cannot be deleted

**REQ-3.4.2: Profile Selection**
- Allow user to select a profile to edit
- Load profile's button mappings when selected
- Update controls list to show selected profile's mappings

**REQ-3.4.3: Create New Profile**
- Provide "+" button or "New Profile" action
- Present options:
  - "Based on selected profile" - copies current profile settings
  - "Empty profile" - starts with no mappings
- Prompt for profile name
- Validate profile name is unique and valid for INI format

**REQ-3.4.4: Delete Profile**
- Provide delete button/action
- Confirm deletion with user
- Prevent deletion of default profile
- Remove profile from config file

**REQ-3.4.5: Profile Window Matching**
- Allow user to configure window matching rules for each profile
- Fields for:
  - App ID
  - Window Class
  - Window Title
- "Capture Active Window" button functionality:
  - Pause for 3-5 seconds with countdown
  - Use WaylandWindowMonitor to detect focused window
  - Auto-populate window matching fields
  - User can edit/clear auto-populated values
- Display help text explaining when profile will activate

### 3.5 Control Configuration

**REQ-3.5.1: Controls List Display**
- Show all TourBox controls in a scrollable list:
  - Buttons: side, top, tall, short, c1, c2, tour
  - D-pad: dpad_up, dpad_down, dpad_left, dpad_right
  - Scroll wheel: scroll_up, scroll_down, scroll_click
  - Knob: knob_cw, knob_ccw, knob_click
  - Dial: dial_cw, dial_ccw, dial_click
- Display current action for each control
- Allow clicking to select for editing

**REQ-3.5.2: Control Selection**
- When control clicked in list:
  - Highlight in visual controller image
  - Load configuration into edit area
  - Provide visual indication of selection

**REQ-3.5.3: Bi-directional Selection**
- Physical button press → selects in list + highlights image
- List click → highlights image
- Both → load into edit area

### 3.6 Action Configuration

**REQ-3.6.1: Action Type Selection**
- Dropdown/toggle for action type:
  - Keyboard Action
  - Mouse Wheel
  - None (disabled)

**REQ-3.6.2: Keyboard Action Configuration**
- Modifier buttons (toggle on/off):
  - Ctrl (KEY_LEFTCTRL)
  - Alt (KEY_LEFTALT)
  - Shift (KEY_LEFTSHIFT)
  - Super (KEY_LEFTMETA)
- Text input field for typeable characters:
  - Letters: A-Z, a-z
  - Numbers: 0-9
  - Symbols: -, =, [, ], ;, ', `, \, ,, ., /, etc.
  - User types the character directly
- Key dropdown for special (non-typeable) keys:
  - Control keys: Enter, Escape, Tab, Space, Backspace, Delete, Insert
  - Arrow keys: Up, Down, Left, Right
  - Navigation: Home, End, Page Up, Page Down
  - Function keys: F1-F12
- Either text input OR dropdown is used, not both
- Convert to appropriate KEY_* codes for config file

**REQ-3.6.3: Mouse Wheel Configuration**
- Direction dropdown:
  - Vertical Up (REL_WHEEL:1)
  - Vertical Down (REL_WHEEL:-1)
  - Horizontal Left (REL_HWHEEL:-1)
  - Horizontal Right (REL_HWHEEL:1)
- Optional: Amount field for scroll speed (±1, ±2, etc.)

**REQ-3.6.4: None/Disabled**
- Control is unmapped
- No action generated when pressed

### 3.7 Save and Test

**REQ-3.7.1: Save/Apply Button**
- Write current configuration to file
- Validate before saving
- Provide feedback on success/failure
- Do not restart driver automatically

**REQ-3.7.2: Test Button**
- Save configuration
- Restart driver: `systemctl --user restart tourbox`
- Display status of restart operation
- Optionally show driver logs for troubleshooting

## 4. User Interface Requirements

### 4.1 Main Window Layout

```
┌──────────────────────┬─────────────────────────────────┐
│                      │                                 │
│  TourBox Image       │  Controls List (scrollable)     │
│  (with highlights)   │  ┌──────────┬─────────────────┐ │
│                      │  │ Control  │ Current Action  │ │
│                      │  ├──────────┼─────────────────┤ │
│                      │  │ side     │ Super           │ │
│                      │  │ top      │ Shift           │ │
│                      │  │ tall     │ Alt             │ │
│                      │  │ short    │ Ctrl            │ │
│                      │  │ ...      │ ...             │ │
│                      │  └──────────┴─────────────────┘ │
├──────────────────────┼─────────────────────────────────┤
│  Profiles List       │  Edit Control: [side]           │
│  ┌────────────────┐  │  ┌───────────────────────────┐  │
│  │ ☑ default      │  │  │ Action Type: [Keyboard ▼] │  │
│  │ ☐ vscode       │  │  │                           │  │
│  │ ☐ firefox      │  │  │ Modifiers:                │  │
│  │ ☐ gimp         │  │  │ [Ctrl][Alt][Shift][Super] │  │
│  └────────────────┘  │  │                           │  │
│  [+] New Profile     │  │ Key: [c] or [Enter    ▼]  │  │
│  [-] Delete Profile  │  │                           │  │
│                      │  │ [Save/Apply]  [Test]      │  │
│                      │  └───────────────────────────┘  │
└──────────────────────┴─────────────────────────────────┘
```

### 4.2 Visual Design Principles

**REQ-4.2.1: Clear Visual Hierarchy**
- Left side: Device representation and profile selection
- Right side: Configuration and editing
- Clear separation between sections

**REQ-4.2.2: Immediate Feedback**
- Highlight active control in image
- Visual state changes for button presses
- Clear indication of selected profile
- Status indicators for driver state

**REQ-4.2.3: Accessibility**
- Sufficient color contrast
- Clear labels for all controls
- Keyboard navigation support
- Tooltips for complex features

### 4.3 Controller Image

**REQ-4.3.1: Visual Representation**
- Display image or diagram of TourBox Elite
- Clearly show all buttons, dials, and controls
- Sufficient size for easy identification

**REQ-4.3.2: Highlighting System**
- Overlay highlight on active control
- Color/style that stands out clearly
- Smooth transitions when changing selection
- Persist highlight until new control selected

### 4.4 Dialogs and Modals

**REQ-4.4.1: New Profile Dialog**
- Profile name input field
- Radio buttons or dropdown for:
  - "Based on selected profile"
  - "Empty profile"
- OK/Cancel buttons

**REQ-4.4.2: Delete Confirmation**
- Clear message about what will be deleted
- Warning if deleting profile with custom mappings
- Confirm/Cancel buttons

**REQ-4.4.3: Window Capture Dialog**
- Countdown timer display (3-5 seconds)
- Instructions for user
- Cancel button
- Auto-close on capture or timeout

**REQ-4.4.4: Error Messages**
- Clear description of error
- Suggested solutions where possible
- OK button to dismiss

## 5. Technical Requirements

### 5.1 Technology Stack

**REQ-5.1.1: Framework**
- Python 3.9+ (matches existing driver)
- Qt 6 via PySide6 for cross-desktop Linux UI
- Bleak for Bluetooth Low Energy communication
- Reuse existing config_loader and window_monitor modules

**REQ-5.1.2: Dependencies**
- PySide6 (Qt 6 bindings for Python)
- qasync (Qt/asyncio integration for async BLE operations)
- Bleak (BLE communication)
- QPainter/QPixmap (for image overlay/highlighting)
- Standard library: configparser, subprocess, asyncio

### 5.2 Architecture

**REQ-5.2.1: Code Reuse**
- Import and reuse existing BLE connection code
- Use BUTTON_CODES mapping from config_loader.py
- Leverage WaylandWindowMonitor for window detection
- Use same config file parsing logic

**REQ-5.2.2: Module Structure**
```
tourboxelite/
  gui/
    __init__.py
    main_window.py       # Main Qt window (QMainWindow)
    controller_view.py   # TourBox image with highlighting (QWidget)
    profile_manager.py   # Profile list and management (QListWidget)
    control_editor.py    # Edit area for actions (QWidget)
    ble_listener.py      # BLE event handling with Qt signals
    driver_manager.py    # Systemd service control
```

**REQ-5.2.3: Async Handling**
- Use Qt event loop integration with asyncio (qasync library)
- Handle BLE events asynchronously
- Use Qt signals/slots for thread-safe UI updates
- Non-blocking UI operations

### 5.3 Integration Points

**REQ-5.3.1: Driver Service**
- Interface with systemd via subprocess
- Commands: start, stop, restart, status
- Handle service errors gracefully

**REQ-5.3.2: Configuration File**
- Read/write ~/.config/tourbox/mappings.conf
- Maintain INI format compatibility
- Preserve comments and formatting where possible

**REQ-5.3.3: BLE Device**
- Connect to same device as driver
- Use identical BLE service UUIDs and characteristics
- Handle disconnect/reconnect scenarios

### 5.4 Error Handling

**REQ-5.4.1: Connection Errors**
- Handle TourBox not powered on
- Handle TourBox out of range
- Handle BLE adapter issues
- Provide clear error messages with solutions

**REQ-5.4.2: Configuration Errors**
- Handle corrupted config files
- Handle missing config files
- Validate user input before saving
- Provide recovery options

**REQ-5.4.3: Driver Errors**
- Handle systemd service not found
- Handle permission issues
- Handle driver already stopped/started
- Display appropriate error messages

## 6. Non-Functional Requirements

### 6.1 Performance

**REQ-6.1.1: Responsiveness**
- UI must remain responsive during BLE operations
- Button press detection latency < 100ms
- Visual highlights appear immediately on selection

**REQ-6.1.2: Resource Usage**
- Minimal CPU usage when idle
- Reasonable memory footprint (< 100MB)
- No memory leaks during extended use

### 6.2 Reliability

**REQ-6.2.1: Data Safety**
- Always backup config before modifying
- Atomic file writes to prevent corruption
- Validate before overwriting existing config

**REQ-6.2.2: Crash Recovery**
- Attempt to restart driver even if app crashes
- Don't leave driver in stopped state
- Restore config from backup if save failed

### 6.3 Compatibility

**REQ-6.3.1: Linux Distributions**
- Support Debian/Ubuntu (primary)
- Support other major distributions
- Document distribution-specific requirements

**REQ-6.3.2: Desktop Environments**
- Support GNOME (Wayland) - Qt provides good visual integration
- Support KDE Plasma (Wayland) - Native Qt appearance
- Support Sway/Hyprland
- Qt framework provides consistent cross-desktop experience
- Graceful degradation for X11

**REQ-6.3.3: Display Servers**
- Full functionality on Wayland
- Window capture functionality limited on X11 as appropriate

### 6.4 Usability

**REQ-6.4.1: Learning Curve**
- New users should understand basic functions within 5 minutes
- Common tasks (changing button mapping) < 30 seconds
- Advanced tasks (creating new profile) < 2 minutes

**REQ-6.4.2: Documentation**
- Include tooltips for all major features
- Provide help button/menu with user guide
- Include examples for common configurations

## 7. Future Enhancements (Out of Scope for v1.0)

### 7.1 Potential Features
- Macro recording (record sequence of keypresses)
- Profile import/export for sharing
- Cloud sync of profiles
- Multiple TourBox device support
- Custom button icons/labels
- Undo/redo for configuration changes
- Configuration presets for popular applications
- Live preview mode (test without restarting driver)
- Button hold vs. press actions
- Advanced scripting support

## 8. Success Criteria

### 8.1 User Acceptance
- Users can configure all buttons without editing text files
- Users can create app-specific profiles without documentation
- Users report GUI is intuitive and easy to use
- Feature parity with Windows/Mac official software

### 8.2 Technical Success
- Zero data loss during configuration changes
- No crashes during normal operation
- Works reliably across target Linux distributions
- BLE connection stable during extended use

### 8.3 Adoption
- Majority of new users prefer GUI over manual config editing
- Reduces support requests related to configuration
- Positive feedback from Linux user community

## 9. Risks and Mitigations

### 9.1 Risk: BLE Connection Conflicts
**Mitigation:** Always stop driver before GUI connects; restart on exit

### 9.2 Risk: Configuration Corruption
**Mitigation:** Validate all input; backup before saving; atomic writes

### 9.3 Risk: Cross-platform Compatibility Issues
**Mitigation:** Test on multiple distributions; handle compositor differences

### 9.4 Risk: User Confusion with Complex Features
**Mitigation:** Progressive disclosure; tooltips; good defaults; help documentation

## 10. Appendices

### 10.1 Button Code Reference
See `tourboxelite/config_loader.py:BUTTON_CODES` for complete mapping of control names to BLE event codes.

### 10.2 Key Name Reference
See `tourboxelite/config_loader.py:KEY_NAMES` for complete mapping of keyboard key names to evdev codes.

### 10.3 Config File Format
See `tourboxelite/default_mappings.conf` for example configuration file format.

---

**Document Version:** 1.0
**Last Updated:** 2025-11-03
**Status:** Draft
