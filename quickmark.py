#!/usr/bin/env python3
"""
quickmark: A simple directory bookmarking tool.

This script allows users to bookmark directories and quickly navigate to them.
"""

import os
import sys
import argparse
import json
from pathlib import Path

# Define the path for the bookmarks file
BOOKMARKS_FILE = os.path.expanduser("~/.quickmark_bookmarks.json")
# Define the script name as it would be installed
SCRIPT_NAME = os.path.basename(__file__)


def load_bookmarks():
    """Load bookmarks from the JSON file."""
    if os.path.exists(BOOKMARKS_FILE):
        try:
            with open(BOOKMARKS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Bookmarks file is corrupted. Creating a new one.")
            return {}
    return {}


def save_bookmarks(bookmarks):
    """Save bookmarks to the JSON file."""
    with open(BOOKMARKS_FILE, 'w') as f:
        json.dump(bookmarks, f, indent=2)


def add_bookmark(name, path):
    """Add a new bookmark."""
    # Load existing bookmarks
    bookmarks = load_bookmarks()

    # Expand the path (resolve ~ and environment variables)
    expanded_path = os.path.expanduser(path)
    expanded_path = os.path.expandvars(expanded_path)

    # Check if the path exists
    if not os.path.isdir(expanded_path):
        print(f"Error: Directory '{expanded_path}' does not exist.")
        return False

    # Convert to absolute path
    abs_path = os.path.abspath(expanded_path)

    # Add the bookmark
    bookmarks[name] = abs_path
    save_bookmarks(bookmarks)
    print(f"Added bookmark '{name}' -> '{abs_path}'")
    return True


def delete_bookmark(name):
    """Delete a bookmark."""
    bookmarks = load_bookmarks()
    if name in bookmarks:
        del bookmarks[name]
        save_bookmarks(bookmarks)
        print(f"Deleted bookmark '{name}'")
        return True
    else:
        print(f"Error: Bookmark '{name}' not found.")
        return False


def list_bookmarks():
    """List all bookmarks."""
    bookmarks = load_bookmarks()
    if not bookmarks:
        print("No bookmarks found.")
        return

    print("Bookmarks:")
    max_name_len = max(len(name) for name in bookmarks) if bookmarks else 0
    for name, path in sorted(bookmarks.items()):
        print(f"  {name:{max_name_len}} -> {path}")


def get_bookmark_path(name):
    """Get the path for a bookmark."""
    bookmarks = load_bookmarks()
    if name in bookmarks:
        path = bookmarks[name]
        # Print the path to stdout so the shell function can use it
        print(path)
        return True
    else:
        print(f"Error: Bookmark '{name}' not found.", file=sys.stderr)
        return False


def get_shell_function():
    """Return the shell function text."""
    return f"""
# quickmark shell function
qm() {{
    # First check if it's a command
    case "$1" in
        add|delete|list|install|shell-function)
            {SCRIPT_NAME} "$@"
            ;;
        # If not a known command, treat the first argument as a bookmark name
        *)
            if [ -z "$1" ]; then
                # No arguments, show help
                {SCRIPT_NAME}
            else
                # Try to navigate to the bookmark
                local target_dir=$({SCRIPT_NAME} go "$1")
                if [ $? -eq 0 ] && [ -n "$target_dir" ]; then
                    cd "$target_dir"
                fi
            fi
            ;;
    esac
}}
"""


def print_shell_function():
    """Print the shell function to be added to ~/.bashrc or ~/.zshrc."""
    print(get_shell_function())
    print("\nAdd the above function to your ~/.bashrc or ~/.zshrc file.")


def install_shell_function():
    """Install the shell function to the user's shell config file."""
    shell_function = get_shell_function()

    # Determine which shell the user is using
    shell = os.environ.get('SHELL', '')

    # Set the appropriate config file
    if 'zsh' in shell:
        config_file = os.path.expanduser('~/.zshrc')
    else:
        # Default to bash
        config_file = os.path.expanduser('~/.bashrc')

    try:
        # Check if the function is already installed
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                content = f.read()
                if 'quickmark shell function' in content:
                    print(f"Shell function already installed in {config_file}")
                    return True

        # Append the function to the config file
        with open(config_file, 'a') as f:
            f.write('\n')  # Add a newline for cleanliness
            f.write(shell_function)

        print(f"Shell function installed in {config_file}")
        print(f"Please restart your shell or run 'source {config_file}' to activate it.")
        return True

    except Exception as e:
        print(f"Error installing shell function: {e}")
        print("You can manually add the following to your shell config file:")
        print(shell_function)
        return False


def main():
    """Main function for the quickmark tool."""
    parser = argparse.ArgumentParser(description='Quickly bookmark and navigate to directories.')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a bookmark')
    add_parser.add_argument('name', help='Name of the bookmark')
    add_parser.add_argument('path', nargs='?', default=os.getcwd(),
                            help='Path to bookmark (defaults to current directory)')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a bookmark')
    delete_parser.add_argument('name', help='Name of the bookmark to delete')

    # List command
    subparsers.add_parser('list', help='List all bookmarks')

    # Go command (used internally by the shell function)
    go_parser = subparsers.add_parser('go', help='Go to a bookmarked directory')
    go_parser.add_argument('name', help='Name of the bookmark to navigate to')

    # Shell function command
    subparsers.add_parser('shell-function', help='Print the shell function to add to your shell config')

    # Install command
    subparsers.add_parser('install', help='Install the shell function to your shell config file')

    args = parser.parse_args()

    if args.command == 'add':
        add_bookmark(args.name, args.path)
    elif args.command == 'delete':
        delete_bookmark(args.name)
    elif args.command == 'list':
        list_bookmarks()
    elif args.command == 'go':
        get_bookmark_path(args.name)
    elif args.command == 'shell-function':
        print_shell_function()
    elif args.command == 'install':
        install_shell_function()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()