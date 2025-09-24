# PyQt MainWindow Project Template

A Qt-based application template using PySide6 with threading capabilities.

## Getting Started

### Clone the Repository

To clone this repository with all submodules:

```bash
git clone --recurse-submodules https://github.com/LinhTrucVo/PyQtMainWindow_Project_Template.git
cd PyQtMainWindow_Project_Template
```

If you already cloned the repository without submodules, initialize them:

```bash
git submodule update --init --recursive
```
or update them:

```bash
git submodule update --remote --recursive
```

After update submodule:

```bash
git add src/PyQtLib_Project_Template
git commit -m "updare submodule"
git push
```

## Submodules

This project uses the following submodules:

- **PyQtLib_Project_Template**: Core PyQt threading and messaging library
  - Repository: https://github.com/LinhTrucVo/PyQtLib_Project_Template.git
  - Path: `src/PyQtLib_Project_Template`


## 📦 Quick Start

```sh
git clone https://github.com/LinhTrucVo/PyQtQuick_Project_Template.git
cd PyQtQuick_Project_Template
# python -m venv .venv
# .venv\Scripts\activate  # On Windows
conda create --name PyQtQuick_Project_Template_env python=3.11 -y
conda activate PyQtQuick_Project_Template_env
pip install -r venv_requirements.txt
build.bat

```

## Create submodule
```sh
cd src/Client_Code/
python create_client_code.py
```
<img width="267" height="182" alt="image" src="https://github.com/user-attachments/assets/ecff7b35-3675-43ab-aa8b-c486cc464874" />
