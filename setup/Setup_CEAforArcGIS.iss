[Setup]
AppName=CEAforArcGIS
AppVersion=1.5
DefaultDirName={pf}\CEAforArcGIS

[Files]
Source: "site-packages\*"; DestDir: "{app}\site-packages"; Flags: ignoreversion recursesubdirs
Source: "..\cea\*"; DestDir: "{userappdata}\ESRI\Desktop10.4\ArcToolbox\My Toolboxes\cea"; Flags: ignoreversion recursesubdirs
Source: "cealib.pth"; DestDir: "C:\Python27\ArcGIS10.4\Lib\site-packages"; Flags: ignoreversion; AfterInstall: WriteCealibPth

[PreCompile]
Name: "copy_library.bat";

[Code]
procedure WriteCealibPth();
begin
  SaveStringToFile('C:\Python27\ArcGIS10.4\Lib\site-packages\cealib.pth', ExpandConstant('{app}\site-packages'), False);
end;