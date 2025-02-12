# Linux 'pip', 'pipenv' Issue

## Prompt

I'm running Raspberry Pi OS:

```bash
flynntknapp@LAMP-SERVER:~/Programming/raspi-remote-lamp $ pip install pipenv
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.

    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.

    For more information visit http://rptl.io/venv

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
flynntknapp@LAMP-SERVER:~/Programming/raspi-remote-lamp $
```

Please explain what is going on, why it's happening, and what is best practice in my situation?

Please explain, in detail, how to make it so I can use pipenv to manage separate python applications (with different dependencies) on this beautiful piece of hardware and software?

## Response

### What's Happening?

The error message `externally-managed-environment` comes from **PEP 668**, which is a Python Enhancement Proposal aimed at preventing system-wide Python installations from being inadvertently modified. This is a security and stability measure implemented by **Debian-based** distributions, including **Raspberry Pi OS (based on Debian)**. 

Instead of allowing users to install packages system-wide with `pip install`, Raspberry Pi OS **enforces** using the **system package manager (`apt`) for system-wide installations** or **virtual environments (`venv`) for project-specific dependencies**.

### Why is This Happening?

1. **Protection of System Packages**  
   - Raspberry Pi OS (like Debian) manages Python packages at the system level using `apt`.  
   - Installing Python packages using `pip` at the system level can break dependencies or interfere with other system applications.

2. **Encouraging Virtual Environments**  
   - Instead of installing everything globally, Python now encourages using **virtual environments** (`venv` or `pipenv`) so each project can have its own isolated dependencies.  
   - This ensures that different projects don’t conflict with each other when they require different versions of the same package.

---

## Best Practice: Setting Up `pipenv` for Managing Python Environments on Raspberry Pi OS

To use `pipenv` to manage separate Python applications with different dependencies, **you need to create and work inside a virtual environment**.

### **Step 1: Install `pipenv` in a Virtual Environment**
Since you cannot install `pipenv` system-wide using `pip`, you must create a virtual environment and install `pipenv` inside it.

#### **1.1 Install Required Packages**
```bash
sudo apt update
sudo apt install python3-pip python3-venv python3-full
```
- `python3-pip` → The package manager for Python  
- `python3-venv` → Allows creating virtual environments  
- `python3-full` → Ensures you have all necessary Python tools  

#### **1.2 Create a Directory for Virtual Environments**
A good practice is to keep all your virtual environments in a separate directory:
```bash
mkdir -p ~/.venvs
```

#### **1.3 Create a Virtual Environment for `pipenv`**
```bash
python3 -m venv ~/.venvs/pipenv
```
This creates an isolated Python environment specifically for `pipenv`.

#### **1.4 Activate the Virtual Environment**
```bash
source ~/.venvs/pipenv/bin/activate
```
Now, you're inside the virtual environment, where `pip` will install packages locally without affecting the system.

#### **1.5 Install `pipenv` in the Virtual Environment**
```bash
pip install pipenv
```

#### **1.6 Deactivate the Virtual Environment**
```bash
deactivate
```
Now, `pipenv` is installed inside its own virtual environment, and you won’t run into system restrictions.

---

## **Using `pipenv` to Manage Different Python Applications**
### **Step 2: Using `pipenv` in a Python Project**
#### **2.1 Go to Your Project Directory**
```bash
cd ~/Programming/raspi-remote-lamp
```

#### **2.2 Ensure `pipenv` is Available**
Since `pipenv` was installed in a virtual environment, we must **run it from there**.

##### **Option 1: Use Absolute Path to `pipenv`**
```bash
~/.venvs/pipenv/bin/pipenv install
```
This ensures that `pipenv` is used from the virtual environment.

##### **Option 2: Add `pipenv` to PATH Temporarily**
Instead of typing the full path every time, you can **add it to your `PATH`** (only for the current session):
```bash
export PATH="$HOME/.venvs/pipenv/bin:$PATH"
```
Then, you can just run:
```bash
pipenv install
```
(You’ll have to re-run the `export` command after rebooting unless you add it to your `~/.bashrc` or `~/.bash_profile`.)

#### **2.3 Initialize a `pipenv` Environment for Your Project**
Once `pipenv` is available, navigate to your project folder and initialize a new environment:
```bash
pipenv install
```
or, if you need a specific Python version:
```bash
pipenv --python 3.9
```
(replace `3.9` with your Raspberry Pi OS's Python version)

#### **2.4 Activate the `pipenv` Shell**
```bash
pipenv shell
```
This will activate the virtual environment, and now any `pip install` commands will only affect this project.

#### **2.5 Install Dependencies**
For example, if your project needs `Flask`:
```bash
pipenv install flask
```
This creates a `Pipfile` that keeps track of the dependencies.

#### **2.6 Running Python Code with `pipenv`**
To run a Python script inside the `pipenv` environment:
```bash
pipenv run python my_script.py
```

#### **2.7 Deactivate the `pipenv` Shell**
When you're done working in the environment:
```bash
exit
```

---

## **Making `pipenv` Always Available**
To make `pipenv` available globally without specifying the full path every time, add it to your `.bashrc` or `.profile`:

```bash
echo 'export PATH="$HOME/.venvs/pipenv/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Now, `pipenv` will always be available when you open a new terminal.

---

## **Final Summary**
- Raspberry Pi OS prevents system-wide `pip install` to protect system packages.
- The best practice is to **use virtual environments (`venv`) to install `pipenv`**.
- Install `pipenv` inside its own virtual environment:
  ```bash
  python3 -m venv ~/.venvs/pipenv
  source ~/.venvs/pipenv/bin/activate
  pip install pipenv
  deactivate
  ```
- Use `pipenv` inside project directories:
  ```bash
  ~/.venvs/pipenv/bin/pipenv install
  pipenv shell
  pipenv install flask  # Example package
  pipenv run python my_script.py
  exit
  ```
- Add `pipenv` to your `PATH` for convenience:
  ```bash
  export PATH="$HOME/.venvs/pipenv/bin:$PATH"
  ```

---

### **Now You Can:**
✅ Manage multiple Python projects with separate dependencies using `pipenv`.  
✅ Avoid breaking system Python packages.  
✅ Keep your Raspberry Pi setup clean and stable.  

This setup is the best way to **maintain flexibility** without conflicting with Raspberry Pi OS's package management. 🚀
