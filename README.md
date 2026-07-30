# pyncli

A Python library and command-line interface for administering **Nextcloud** servers.

`pyncli` was originally developed as an internal automation tool for managing a production Nextcloud deployment integrated with LDAP. It provides both a Python API and a command-line interface for automating repetitive administrative tasks that are difficult or time-consuming to perform through the web interface.

The project is suitable for infrastructure engineers, system administrators, and developers who need to manage users, groups, and Group Folders programmatically.

---

## Features

- User management
- Group management
- Group Folder management
- LDAP integration
- Batch user provisioning
- Python API
- Command-line interface
- Automation-friendly design

---

## Typical Use Cases

- Provisioning new employees
- Creating and maintaining user groups
- Managing shared Group Folders
- Synchronizing LDAP-backed installations
- Automating repetitive administrative operations
- Integrating Nextcloud administration into deployment scripts

---

## Tech Stack

- Python
- Nextcloud OCS API
- LDAP (optional)
- Click
- Requests

---

## Architecture

```
 CLI
   │
   ▼
 Python API
   │
   ▼
 Nextcloud OCS API
   │
   ▼
 Nextcloud Server

        │
        ▼

   LDAP (optional)
```

The same Python API powers both the CLI and external applications, allowing administrative tasks to be automated either from shell scripts or directly from Python code.

---

## Installation

```bash
pip install pyncli
```

or

```bash
pip install -i https://test.pypi.org/simple/ pyncli
```

---

## Quick Examples

List users

```bash
pnc get users
```

Create a new group

```bash
pnc new group --name Developers
```

Create a new Group Folder

```bash
pnc new groupfolder --name SharedDocs
```

Use the Python API

```python
from pyncli.ocs import Ocs

cloud = Ocs(user, password, base_url)

users = cloud.get_users()
groups = cloud.get_groups()
```

---

## Documentation

For detailed installation instructions, configuration options, complete CLI reference, and Python API examples, see the [User Guide](docs/user-guide.md).

---

## Project Status

The project is stable and was successfully used to automate administration of a production Nextcloud installation.

Although active development has stopped, the repository remains available as a reference implementation of a Python-based Nextcloud administration tool.

---

## License

MIT License
