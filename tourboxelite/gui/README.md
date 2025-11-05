# TourBox Elite Configuration GUI

Graphical interface for configuring TourBox Elite button mappings and application-specific profiles.

## Installation

The GUI dependencies are **automatically installed** by the main `install.sh` script. If you performed a manual installation, ensure you have the GUI dependencies:

```bash
pip install -r tourboxelite/gui/requirements.txt
```

## Usage

### Running the GUI

```bash
tourbox-gui
```

The installer creates a launcher script in `/usr/local/bin/tourbox-gui` that you can run from anywhere.

### What the GUI Does

1. **On Launch:**
   - Automatically stops the TourBox driver service
   - Connects to your TourBox Elite via Bluetooth
   - Loads your existing configuration

2. **Configuration:**
   - Edit button mappings visually
   - Create/edit application-specific profiles
   - Real-time feedback when pressing physical buttons
   - Set up window matching rules with "Capture Active Window"

3. **On Exit:**
   - Saves changes to configuration file
   - Automatically restarts the driver service

## Features

- **Visual Controller Display:** See which button you're configuring
- **Profile Management:** Create, edit, and delete profiles
- **Real-time Feedback:** Press a physical button to select it for configuration
- **Easy Key Assignment:** Use modifier buttons + text input for key combos
- **Window Matching:** Capture active window for automatic profile switching
- **Test Mode:** Restart driver to test your changes

## Documentation

**📖 [Complete User Guide](../../docs/GUI_USER_GUIDE.md)** - Comprehensive guide with tutorials, tips, and troubleshooting

**Development Documentation:**
- [PRD](../../docs/GUI_PRD.md) - Product requirements and specifications
- [Progress](../../docs/GUI_PROGRESS.md) - Development status and implementation notes

## Development Status

**✅ Feature Complete** - The GUI is fully functional for configuring TourBox Elite button mappings and profiles. See [GUI_PROGRESS.md](../../docs/GUI_PROGRESS.md) for detailed implementation status.

## Architecture

The GUI is built with:
- **PySide6:** Qt 6 bindings for cross-desktop compatibility
- **qasync:** Integration between Qt and asyncio for BLE operations
- **Bleak:** Bluetooth Low Energy communication (reused from driver)

All GUI code is self-contained in this directory and does not modify the existing driver code.
