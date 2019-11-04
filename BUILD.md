# Build from source

## Install Dependencies

- Python 3.7
[[Official](
    https://www.python.org/downloads/
)]
[[Anaconda](
    https://www.anaconda.com/distribution/#download-section
)]
[[Miniconda](
    https://docs.conda.io/en/latest/miniconda.html
)]

### Linux

```
$ pip intall -r requirements/linux.txt
```

### Windows

- NSIS
[[SourceForge](
    https://nsis.sourceforge.io/Download
)]

```
> pip install -r requirements\windows.txt
```

## Build Application

### Linux

```
$ pyinstaller --add-data "version.txt:." --add-data "LICENSE:." main.py
```

### Windows

```
> pyinstaller --add-data "version.txt;." --add-data "LICENSE;." main.py
```

## Create Installer for Windows

- Start NSIS
- Compiler > Compile NSI scripts
- Drag and drop `system-info-installer.nsi` to NSIS window

It will create `system-info-installer.exe` file.
