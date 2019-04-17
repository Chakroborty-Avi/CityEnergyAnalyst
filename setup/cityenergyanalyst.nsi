# NSIS script for creating the City Energy Analyst installer


; include the modern UI stuff
!include "MUI2.nsh"

# download CEA conda env from here (FIXME: update to a more sane download URL)
# !define CEA_ENV_URL "https://polybox.ethz.ch/index.php/s/M8MYliTOGbbSCjH/download"
# !define CEA_ENV_FILENAME "cea.7z"
!define CEA_ENV_URL "https://polybox.ethz.ch/index.php/s/USmeJGf3PnjksFc/download"
!define CEA_ENV_FILENAME "Dependencies.7z"

!define CEA_TITLE "City Energy Analyst"

# figure out the version based on cea\__init__.py
!system "get_version.exe"
!include "cea_version.txt"

Name "${CEA_TITLE} ${VER}"
!define MUI_FILE "savefile"
!define MUI_BRANDINGTEXT "City Energy Analyst ${VER}"
CRCCheck On


OutFile "Output\Setup_CityEnergyAnalyst_${VER}.exe"


;--------------------------------
;Folder selection page

InstallDir "$LOCALAPPDATA\CityEnergyAnalyst"

;Request application privileges for Windows Vista
RequestExecutionLevel user

;--------------------------------
;Interface Settings

!define MUI_ABORTWARNING

;--------------------------------
;Pages

!insertmacro MUI_PAGE_LICENSE "..\LICENSE"
!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "Dummy Section" SecDummy

SetOutPath "$INSTDIR"

;Download the CityEnergyAnalyst conda environment
inetc::get ${CEA_ENV_URL} ${CEA_ENV_FILENAME}
Pop $R0 ;Get the return value
StrCmp $R0 "OK" download_ok
    MessageBox MB_OK "Download failed: $R0"
    Quit
download_ok:
    # get on with life...


# unzip python environment to ${INSTDIR}\Dependencies
Nsis7z::Extract ${CEA_ENV_FILENAME} "Installing Python %s..."
Delete ${CEA_ENV_FILENAME}

nsExec::ExecToLog '"$INSTDIR\Dependencies\Python\Scripts\pip.exe" install cityenergyanalyst'
nsExec::ExecToLog '"$INSTDIR\Dependencies\Python\Scripts\pip.exe" install -U --no-cache cityenergyanalyst'


;Create uninstaller
WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd

;--------------------------------
;Descriptions

;Language strings
;  LangString DESC_SecDummy ${LANG_ENGLISH} "A test section."

  ;Assign language strings to sections
;  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
;    !insertmacro MUI_DESCRIPTION_TEXT ${SecDummy} $(DESC_SecDummy)
;  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...

  Delete "$INSTDIR\Uninstall.exe"

  RMDir "$INSTDIR"

  DeleteRegKey /ifempty HKCU "Software\Modern UI Test"

SectionEnd