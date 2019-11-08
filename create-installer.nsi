# name of the installer
OutFile "xincapio-installer.exe"

InstallDir "$PROGRAMFILES64\xincapio"

# default section start
Section

SetOutPath $INSTDIR

# define what to install
File /r "dist\main\*"

WriteUninstaller $INSTDIR\uninstall.exe

CreateDirectory "$SMPROGRAMS\Xincapio\"
CreateShortCut "$SMPROGRAMS\Xincapio\Xincapio.lnk" "$INSTDIR\main.exe" "--gui"
CreateShortCut "$SMPROGRAMS\Xincapio\uninstall.exe.lnk" "$INSTDIR\uninstall.exe"

# add uninstall information
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Xincapio" "DisplayName" "Xincapio"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Xincapio" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""

# default section end
SectionEnd

Section "Uninstall"

# always delete uninstaller first
Delete $INSTDIR\uninstall.exe

Delete $INSTDIR\*
RMDir /r $INSTDIR\Include
RMDir /r $INSTDIR\PyQt5
RMDir /r $INSTDIR\win32com
RMDir /r "$SMPROGRAMS\Xincapio"

# remove uninstall information
DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Xincapio"

SectionEnd
