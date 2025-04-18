# quickmark

A simple tool for bookmarking frequently visited directories. Provides an explicit and predictable alternative to history-based tools like `autojump` or `zoxide`.

## Features

- Explicitly bookmark directories with meaningful names
- Quick navigation to bookmarked directories
- Simple text-based storage (JSON)
- No "magic" or automatic learning - you control your bookmarks

## Installation

### Option 1: Install via pip (recommended)

```bash
pip install git+https://github.com/yourusername/quickmark.git
quickmark install
```

### Option 2: Manual installation

1. Download the `quickmark.py` script
2. Make it executable: `chmod +x quickmark.py`
3. Run: `./quickmark.py install`

## Usage

### Adding a bookmark

```bash
# Bookmark the current directory as "work"
qm add work

# Bookmark a specific directory as "proj"
qm add proj ~/work/clients/big_corp/project_alpha
```

### Navigating to a bookmarked directory

```bash
# Jump to the "proj" bookmark
qm proj
```

### Listing bookmarks

```bash
qm list
```

### Deleting a bookmark

```bash
qm delete proj
```

### Getting help

```bash
qm help
```

## License

MIT