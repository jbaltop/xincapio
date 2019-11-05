# name of the installer
OutFile "system-info-installer.exe"

InstallDir "$PROGRAMFILES64\System Information"

# default section start
Section

SetOutPath $INSTDIR

# define what to install
File /r "dist\main\*"

WriteUninstaller $INSTDIR\uninstall.exe

CreateDirectory "$SMPROGRAMS\System Information\"
CreateShortCut "$SMPROGRAMS\System Information\System Information.lnk" "$INSTDIR\main.exe" "--gui"
CreateShortCut "$SMPROGRAMS\System Information\uninstall.exe.lnk" "$INSTDIR\uninstall.exe"

# default section end
SectionEnd

Section "Uninstall"

# always delete uninstaller first
Delete $INSTDIR\uninstall.exe

Delete $INSTDIR\*
RMDir /r $INSTDIR\Include
RMDir /r $INSTDIR\PyQt5
RMDir /r $INSTDIR\win32com
RMDir /r "$SMPROGRAMS\System Information"

SectionEnd
