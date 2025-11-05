# TourBox Elite Configuration GUI - Development Progress

**Last Updated:** 2025-11-05
**Status:** Feature Complete - Visual controller representation with highlighting implemented

## Project Overview

Building a Qt-based GUI application for configuring TourBox Elite button mappings and application-specific profiles on Linux. This provides feature parity with the official Windows/Mac TourBox software.

**Technology Stack:**
- Python 3.9+
- PySide6 (Qt 6)
- qasync (Qt/asyncio integration)
- Bleak (Bluetooth LE)
- Reuses existing driver code from `tourboxelite/` modules

**Documentation:**
- [Full PRD](GUI_PRD.md) - Complete product requirements
- [GUI README](../tourboxelite/gui/README.md) - Usage and architecture

## Current Status

### ✅ Completed Features

#### 1. Project Structure
- Created `tourboxelite/gui/` directory with modular architecture
- All GUI code is self-contained and doesn't modify existing driver
- Can run with: `python -m tourboxelite.gui`

**Files created:**
```
tourboxelite/gui/
├── __init__.py                   # Module initialization
├── __main__.py                   # Entry point
├── requirements.txt              # GUI dependencies (PySide6, qasync)
├── README.md                     # Documentation
├── main_window.py                # Main application window with save/test
├── controller_view.py            # TourBox image widget (placeholder)
├── profile_manager.py            # Profile list management with create/delete
├── profile_settings_dialog.py    # Profile settings editor with window capture
├── controls_list.py              # Controls table with current mappings
├── control_editor.py             # Action editor widget
├── config_writer.py              # Configuration file writer (complete)
├── ble_listener.py               # BLE connection handler (stub)
└── driver_manager.py             # Systemd service management (complete)
```

#### 2. Driver Management
- ✅ Auto-stops driver on GUI launch with modal progress dialog
- ✅ Shows initialization steps: "Checking driver status" → "Stopping driver" → "Loading configuration"
- ✅ Remembers if driver was running
- ✅ Auto-restarts driver on exit (if it was running)
- ✅ Error handling with user-friendly dialogs
- ✅ Status bar shows driver state

**Implementation:** `driver_manager.py` + integration in `main_window.py`

#### 3. Profile Loading & Display
- ✅ Loads all profiles from `~/.config/tourbox/mappings.conf`
- ✅ Displays profiles in two-column table (Name | Window)
- ✅ Shows default profile selected on launch
- ✅ Profile selection updates controls list
- ✅ Prevents deletion of default profile
- ✅ Full profile management (see section 12 for details)

**Implementation:** `profile_manager.py`, `profile_settings_dialog.py`

#### 4. Controls List
- ✅ Shows all 20 TourBox controls in table (top-right panel)
- ✅ Displays human-readable action names:
  - Modifiers: "Ctrl", "Alt", "Shift", "Super"
  - Keys: Letters, numbers, symbols
  - Combinations: "Ctrl+C", "Ctrl+Shift+Z"
  - Mouse wheel: "Wheel Up", "Wheel Down"
- ✅ Symbol key mapping: `]` instead of "Brace", `=` instead of "Equal", etc.
- ✅ Proper column sizing (control names resize to content, actions stretch)
- ✅ Selection highlights in both list and controller view

**Implementation:** `controls_list.py`

**Bug fixes applied:**
- Fixed cell span issue causing row 0 to show blank
- Fixed symbol key display (brackets, equals, etc.)
- Fixed column resize on profile change

#### 5. Control Editor
- ✅ Action type selector: Keyboard / Mouse Wheel / None
- ✅ **Keyboard actions:**
  - Toggle buttons for modifiers: Ctrl, Alt, Shift, Super
  - Text input for regular keys (a-z, 0-9, symbols)
  - Dropdown for special keys (Enter, Escape, arrows, F1-F12, etc.)
  - Dropdown has separator headings for organization
- ✅ **Mouse wheel actions:**
  - Direction dropdown: Vertical Up/Down, Horizontal Left/Right
- ✅ Apply button builds action string and updates controls list
- ✅ Test button (stub - not yet implemented)
- ✅ Parses existing actions and populates UI correctly
- ✅ Handles single-character symbols correctly (], [, =, -, etc.)

**Implementation:** `control_editor.py`

#### 6. UI Integration & Flow
- ✅ 4-panel layout: controller image | profiles list | controls list | editor
- ✅ Bi-directional control selection:
  - Click control in list → highlights in image + loads in editor
  - (Physical button press → highlight + select - not yet implemented)
- ✅ Status bar shows current state and actions
- ✅ Profile selection updates all relevant widgets
- ✅ Action changes update controls list immediately
- ✅ Shows "(not saved)" status when modified

**Implementation:** `main_window.py`

#### 7. Display & Formatting
- ✅ Human-readable action display throughout
- ✅ Consistent symbol mapping across all components
- ✅ Proper title casing for key names
- ✅ Clean modifier names (Ctrl vs KEY_LEFTCTRL)

**Implementation:** Symbol mapping in `controls_list.py`, `main_window.py`, and `control_editor.py`

#### 8. Save Functionality (COMPLETE)
- ✅ Menu bar with File → Save (Ctrl+S), Test (Ctrl+T), Quit
- ✅ Toolbar with Save and Test buttons
- ✅ Tracks modifications in memory (modified_mappings dict)
- ✅ Window title shows profile name and asterisk (*) when modified
- ✅ Save button enabled only when changes exist
- ✅ Preserves comments and formatting in config file
- ✅ Atomic writes (temp file → rename)
- ✅ Automatic timestamped backups before saving
- ✅ Cleanup of old backups (keeps 5 most recent)
- ✅ Controls set to "none" are removed from config (not written as "none")
- ✅ Unsaved changes prompt when switching profiles
- ✅ Unsaved changes prompt when closing application
- ✅ Success/failure dialogs with clear messaging

**Implementation:** `config_writer.py` (new), `main_window.py`

#### 9. Test/Stop Test Functionality (COMPLETE)
- ✅ Test button enabled whenever a profile is selected
- ✅ Starts driver with modal progress dialog
- ✅ Auto-saves changes before testing
- ✅ Entire UI disabled during testing mode (greyed out)
- ✅ Button changes to "Stop Test" (only active control)
- ✅ Status bar shows "Testing mode - Driver running"
- ✅ Clear feedback dialogs for test start/stop
- ✅ Stop Test button stops driver with modal dialog
- ✅ UI re-enables after stopping test
- ✅ Allows rapid test → adjust → test iteration
- ✅ Handles close while testing (auto-stops driver)

**Implementation:** `main_window.py`, `driver_manager.py`

#### 10. Display & Formatting Improvements (COMPLETE)
- ✅ Arrow keys display correctly (Left, Right, Up, Down) - not stripped
- ✅ Multi-word keys use spaces not underscores (Context Menu, Page Up, Zoom Reset)
- ✅ Mouse wheel actions display as "Wheel Up/Down/Left/Right"
- ✅ Zoom keys added to special keys dropdown (Zoom Reset, Zoom In, Zoom Out)
- ✅ Context Menu added to dropdown
- ✅ Consistent "(unmapped)" display for undefined/none controls (not "(none)")
- ✅ Normalized key matching (handles spaces, underscores, case-insensitive)
- ✅ Controls list scrolls to top when switching profiles

**Implementation:** `controls_list.py`, `main_window.py`, `control_editor.py`

#### 11. User Experience Enhancements (COMPLETE)
- ✅ Window title shows current profile name
- ✅ Asterisk (*) in title when unsaved changes exist
- ✅ Status bar always visible and shows current state
- ✅ Profile switch with unsaved changes: Save/Discard/Cancel dialog
- ✅ Discarding changes reloads original values in UI
- ✅ Close with unsaved changes: Save/Discard/Cancel dialog
- ✅ Save/Test buttons properly enable/disable based on state
- ✅ Clear visual feedback for all operations
- ✅ Keyboard navigation with arrow keys (up/down in lists, left/right between panes)

**Implementation:** `main_window.py`, `profile_manager.py`

#### 12. Profile Management (COMPLETE)
- ✅ **Profile List Display:**
  - Two-column table showing Name and Window matching rules
  - Shows "class: Firefox" or "app_id: code" format for clarity
  - Default profile has blank window column
  - No row numbers for clean appearance
- ✅ **Profile Creation:**
  - "+" button to create new profiles
  - Option to copy current profile's mappings or start empty
  - Duplicate name validation
  - Automatic prompt to set up window matching after creation
- ✅ **Profile Editing (Settings):**
  - "⚙" button to edit profile settings (disabled for default profile)
  - Edit profile name (with validation)
  - Set window matching rules (app_id and window_class)
  - "Capture Active Window" feature with 5-second countdown
  - Uses WaylandWindowMonitor to detect focused window
  - Auto-populates app_id and window_class from captured window
  - Apply changes to memory (Save button writes to config)
- ✅ **Profile Deletion:**
  - "-" button to delete profiles (disabled for default profile)
  - Confirmation dialog before deletion
  - Properly removes profile from config while preserving comments
  - Auto-selects default profile after deletion
- ✅ **Profile Rename Tracking:**
  - Correctly saves renamed profiles to config file
  - Updates section headers when profile names change
- ✅ **Comment Preservation:**
  - Maintains profile comments in config file during all operations
  - Proper spacing between profiles after deletion

**Implementation:** `profile_manager.py`, `profile_settings_dialog.py` (new), `config_writer.py`

#### 13. Controller Visualization (COMPLETE)
- ✅ **SVG Image:**
  - Custom TourBox Elite drawing created in Inkscape
  - Background layer with complete device illustration
  - Controls layer with 20 individual highlight overlays
  - Proper object IDs matching control names
  - Scalable vector format for perfect rendering at any size
- ✅ **Rendering System:**
  - QSvgRenderer with dynamic SVG manipulation
  - Controls hidden by default, shown on selection
  - Perfect alignment between background and highlights
  - Automatic scaling while maintaining aspect ratio
  - Real-time updates when controls are selected
- ✅ **Integration:**
  - Highlights appear when clicking controls in table
  - Visual feedback for selected control
  - Window resizable with proper SVG scaling
  - Optimized layout (1280x1024 initial window size)

**Implementation:** `controller_view.py`, `tourboxelite/gui/assets/tourbox_elite.svg`

### 🚧 Partially Implemented

#### BLE Connection
- ✅ Module structure created (`ble_listener.py`)
- ✅ Connection and unlock code written (reuses driver code)
- ❌ Not integrated into main window yet
- ❌ No button press detection → control selection

### ❌ Not Yet Implemented

#### 1. BLE Connection & Real-time Input
**What's needed:**
- Connect to TourBox on GUI launch (after stopping driver)
- Listen for button press notifications
- Map BLE codes to control names
- Trigger control selection in UI
- Handle connection errors gracefully

**Implementation approach:**
- Create BLEListener instance in main_window
- Connect signals to UI slots
- Use qasync to integrate asyncio with Qt event loop
- Reuse unlock sequence and notification handler from driver

**Files to modify:**
- `main_window.py` - Create and manage BLEListener
- `ble_listener.py` - Complete implementation
- Need to load MAC address from config

#### 2. Advanced Features (LOWER PRIORITY)
- Profile import/export
- Macro recording
- Undo/redo for changes
- Live preview without restarting driver
- Configuration presets for popular apps

## Known Issues

### Fixed Issues
- ✅ Row 0 showing blank due to table cell span not being cleared
- ✅ Columns not filling width after profile change (removed resizeColumnsToContents call)
- ✅ Symbol keys showing as "Brace" instead of actual symbols
- ✅ Editor parsing taking wrong character from key names
- ✅ Variable name collision with `except Exception as e:` shadowing evdev import
- ✅ Arrow keys (LEFT, RIGHT) being stripped from display
- ✅ Multi-word keys showing underscores instead of spaces
- ✅ Mouse wheel actions showing raw format (WHEEL:1) instead of human-readable
- ✅ Zoom keys and Context Menu missing from dropdown
- ✅ Inconsistent display of unmapped vs none controls
- ✅ Key matching failing for multi-word keys with spaces
- ✅ Status bar disappearing after adding menu/toolbar
- ✅ Test button grayed out on startup
- ✅ Config file comments being lost on save

### Current Issues
None known at this time.

## Testing Status

**Tested and working:**
- ✅ GUI launches without errors
- ✅ Driver stops on launch (with modal dialog)
- ✅ Profiles load and display correctly
- ✅ All controls show proper action names (arrows, multi-word keys, symbols)
- ✅ Mouse wheel actions display as "Wheel Up/Down/Left/Right"
- ✅ Switching profiles updates controls list and scrolls to top
- ✅ Clicking controls loads them into editor
- ✅ Modifiers and keys populate correctly in editor
- ✅ Special keys dropdown includes all needed keys (arrows, zoom, context menu)
- ✅ Apply button updates UI with human-readable display
- ✅ **Save functionality preserves comments and formatting**
- ✅ **Atomic writes with timestamped backups**
- ✅ **Old backups cleaned up automatically**
- ✅ **Controls set to "none" removed from config file**
- ✅ **Unsaved changes prompts work correctly**
- ✅ **Window title shows profile name and modified state**
- ✅ **Test/Stop Test mode works correctly**
- ✅ **UI properly disabled during testing**
- ✅ **Modal dialogs for all driver start/stop operations**
- ✅ Closing GUI restarts driver (if it was running initially)
- ✅ Closing during test mode stops driver first

**Not yet tested:**
- BLE connection to actual device (for real-time button detection in GUI)
- Physical button presses triggering control selection

## Next Session Priorities

### Optional Enhancements (Future Sessions)
1. **Implement BLE connection** - Real-time button press detection in GUI
   - Would enable clicking physical buttons to select controls in GUI
   - Not critical since testing mode already allows testing with physical device
2. **Polish & improvements** - Based on real-world usage feedback
3. **Documentation updates** - User guide for GUI features

### Core Functionality Status
**✅ COMPLETE - GUI is fully functional for its primary purpose:**
- Edit button mappings with visual interface
- Visual TourBox representation with control highlighting
- Save changes preserving config format
- Test configurations with physical device
- Complete profile management (create, edit, delete, window matching)
- No manual config file editing required

## Development Notes

### Important Code Locations

**Reusable driver code:**
- `tourboxelite/config_loader.py` - Config parsing (already used)
- `tourboxelite/window_monitor.py` - Window detection (for profile matching)
- `tourboxelite/device_ble.py` - BLE constants and unlock sequence

**GUI entry point:**
```bash
source venv/bin/activate
python -m tourboxelite.gui
```

**Logging:**
Currently set to DEBUG level in `main_window.py:main()`. Can change to INFO for production.

### Design Decisions

**Why Qt instead of GTK:**
- Better cross-desktop compatibility (KDE + GNOME)
- More polished widget set
- Project already supports both KDE and GNOME equally

**Why not save on Apply:**
- Allows user to experiment without modifying config
- Prevents accidental overwrites
- Explicit save action is clearer for users

**Symbol mapping approach:**
- Maintain SYMBOL_MAP dict in multiple files
- Could be refactored to shared utility module
- Trade-off: duplication vs. complexity

### Code Style Notes

- Using Qt signals/slots for component communication
- Logging extensively for debugging
- Human-readable display names separate from internal names
- Error handling with user-friendly dialogs

## Resources

**Qt Documentation:**
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [Qt Widgets](https://doc.qt.io/qt-6/qtwidgets-index.html)

**Project Files:**
- PRD: `docs/GUI_PRD.md`
- Driver code: `tourboxelite/*.py`
- Config example: `tourboxelite/default_mappings.conf`

## Session Summary: Save & Test Implementation (2025-11-03)

### What Was Accomplished
This session focused on implementing the core save and test functionality that makes the GUI fully usable:

**Major Features Added:**
1. **Complete Save System** (`config_writer.py`)
   - Preserves comments and formatting in config files
   - Atomic writes with automatic backups
   - Smart handling of "none" controls (removes from config)

2. **Test/Stop Test Mode** (enhanced `main_window.py`)
   - Modal dialogs for driver start/stop
   - Full UI disable/enable during testing
   - Rapid iteration workflow support

3. **Menu Bar & Toolbar**
   - File menu with keyboard shortcuts (Ctrl+S, Ctrl+T)
   - Visual button access for all operations

4. **Display Bug Fixes**
   - Arrow keys display correctly
   - Multi-word keys use spaces not underscores
   - Mouse wheel actions human-readable
   - Consistent "(unmapped)" display

5. **UX Improvements**
   - Window title shows profile and modified state
   - Unsaved changes prompts
   - Status bar always visible
   - Controls list auto-scrolls to top

### Lines of Code Changed
- New file: `config_writer.py` (~230 lines)
- Modified: `main_window.py` (added ~300 lines)
- Modified: `control_editor.py` (improved parsing logic)
- Modified: `controls_list.py` (display improvements)
- Modified: `profile_manager.py` (reselection support)

### Result
**GUI is now feature-complete for primary use case:** Users can fully configure their TourBox Elite without touching config files, with professional save/test workflow and excellent UX.

---

## Session Summary: Profile Management System (2025-11-04)

### What Was Accomplished
This session focused on implementing complete profile management functionality:

**Major Features Added:**
1. **Profile Settings Dialog** (`profile_settings_dialog.py`)
   - Edit profile name with validation
   - Set window matching (app_id and window_class)
   - "Capture Active Window" feature with 5-second countdown timer
   - Integration with WaylandWindowMonitor for automatic window detection
   - Apply button to save changes to memory

2. **Profile Creation** (enhanced `profile_manager.py`)
   - "+" button to create new profiles
   - Option to copy current profile or start empty
   - Duplicate name validation
   - Auto-prompt for window matching setup

3. **Profile Deletion** (enhanced `profile_manager.py`, `config_writer.py`)
   - "-" button with confirmation dialog
   - Proper comment preservation in config file
   - Auto-select default profile after deletion

4. **Profile Rename Support** (`main_window.py`, `config_writer.py`)
   - Tracking of original profile names using id(profile)
   - Proper config file section header updates on rename
   - Detection of rename vs. new profile creation

5. **UI Improvements**
   - Changed from list to two-column table (Name | Window)
   - Window column shows "class: Firefox" or "app_id: code" format
   - Edit button (⚙) disabled for default profile
   - Keyboard navigation with arrow keys between panes
   - Unsaved profile settings detection and prompts

### Lines of Code Changed
- New file: `profile_settings_dialog.py` (~254 lines)
- Modified: `profile_manager.py` (added profile management logic)
- Modified: `config_writer.py` (save_profile_metadata with rename support, delete_profile)
- Modified: `main_window.py` (profile rename tracking, keyboard navigation)
- Modified: `control_editor.py` (CHAR_TO_KEYCODE dictionary for symbol mapping)

### Result
**Complete profile management system:** Users can now create, edit, and delete profiles entirely through the GUI, with automatic window detection and proper config file handling. No manual editing required for any profile operations.

---

## Session Summary: Controller Visualization (2025-11-05)

### What Was Accomplished
This session focused on implementing visual representation of the TourBox Elite with interactive control highlighting:

**Major Features Added:**
1. **SVG Artwork Creation** (Inkscape)
   - Custom TourBox Elite illustration with accurate layout
   - Background layer with complete device drawing
   - Controls layer with 20 individual highlight overlays (yellow fills)
   - Proper object IDs for all controls matching control names
   - Hidden controls by default, shown on selection

2. **SVG Rendering System** (`controller_view.py`)
   - QSvgRenderer with dynamic SVG XML manipulation
   - Loads base SVG showing background only
   - On control selection, modifies SVG in memory to show specific highlight
   - Renders both base and highlight to same target rectangle for perfect alignment
   - Automatic scaling with aspect ratio preservation

3. **Integration & Polish**
   - Control highlights appear when selecting from Controls Configuration table
   - Real-time visual feedback for selected control
   - Window resizable with proper SVG scaling
   - Initial window size optimized to 1280x1024
   - Panel sizes adjusted for better visual balance

### Technical Approach
- **Challenge**: Qt's QSvgRenderer renders individual elements with different coordinate systems
- **Solution**: Parse SVG with ElementTree, modify display:none → display:inline for selected control
- **Result**: Both background and highlight render using same transformation, ensuring perfect alignment

### Lines of Code Changed
- Modified: `controller_view.py` (complete rewrite of rendering logic, ~210 lines)
- Modified: `main_window.py` (window sizing adjustments)
- New asset: `tourboxelite/gui/assets/tourbox_elite.svg` (custom artwork)

### Result
**Complete visual feedback system:** Users can now see exactly which control they're editing with a beautiful, scalable TourBox Elite representation. The GUI is now visually polished and provides excellent UX.

---

**Status:** Ready for real-world usage and user feedback!
