@echo off
setlocal enabledelayedexpansion
setlocal

echo. 
echo #########################################
echo Build Package for Node Project
echo #########################################

::Overrides
SET SOURCE_CONTROL_VALIDATION=N

::Get current date and time
SET CURR_DATE=""
SET CURR_TIME=""
For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set CURR_DATE=%%c-%%a-%%b)
For /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set CURR_TIME=%%a:%%b)

::Get current directory
SET CURRENT_FOLDER_NAME=""
for %%I in (.) do set CURRENT_FOLDER_NAME=%%~nxI

echo.
echo PROJECT NAME - %CURRENT_FOLDER_NAME%

echo.
:PROMPT
SET /P AREYOUSURE=Enter Y to confirm package creation: (Y/[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END

echo.
echo Checking for node (any version) installation
call node --version

if %ERRORLEVEL% GEQ 1 GOTO NODE_NOT_FOUND_ERROR

IF "%SOURCE_CONTROL_VALIDATION%" NEQ "Y" (
	GOTO SHOW_MENU
)

if exist .git\ (
	GOTO VALIDATE_GIT
) else (
	GOTO VALIDATE_TFS
)

:VALIDATE_GIT
echo.
echo Checking for any local changes 
CALL git diff --quiet || echo Local changes found
if %ERRORLEVEL% GEQ 1 (
	GOTO LOCAL_CHANGES_WARNING
) else (
	GOTO LOCAL_CHANGES_NONE
)

:LOCAL_CHANGES_WARNING
echo.
CALL git diff --compact-summary
echo.
SET /P AREYOUSURE= **WARNING** Local changes found. Cancel build:([Y]/N) ?
IF /I "%AREYOUSURE%" NEQ "N" GOTO LOCAL_CHANGES_PRESENT_ERROR

:LOCAL_CHANGES_NONE
echo.
echo Getting latest commit id
FOR /f "tokens=1" %%f IN ('git rev-parse --short HEAD' ) DO SET LAST_COMMIT_ID=%%f
echo Last CommitId=%LAST_COMMIT_ID%
GOTO SHOW_MENU

:VALIDATE_TFS
echo.
echo Checking for TFS executable
call tf.exe 1>nul

if %ERRORLEVEL% GEQ 1 GOTO TFS_EXE_NOT_FOUND_ERROR

echo.
echo Getting latest TFS changeset number
call:fnGetTfsChangesetNumber LAST_TFS_CHANGESET_NUM
echo Latest TFS changeset number=%LAST_TFS_CHANGESET_NUM%

:SHOW_MENU
SET L_DEPLOY_ENV_NAME=""
ECHO.
ECHO ***************************************
ECHO SELECT ENV TO BUILD
ECHO A - Dev
ECHO B - Test
ECHO C - Prod
ECHO.
ECHO Z - Cancel
ECHO ***************************************
CHOICE /c:ABCZ
::echo %ERRORLEVEL%
::ERRORLEVEL is always an index value of the choice value and not equal to the actual choice value 
IF %ERRORLEVEL% EQU 1 (
	SET L_DEPLOY_ENV_NAME=dev
)
IF %ERRORLEVEL% EQU 2 (
	SET L_DEPLOY_ENV_NAME=test
)
IF %ERRORLEVEL% EQU 3 (
	SET L_DEPLOY_ENV_NAME=prod
)
IF %ERRORLEVEL% EQU 4 (
	GOTO END
)

::Do Clean up 
if exist .\target rmdir /Q /S .\target


set PACKAGE_NAME=%CURRENT_FOLDER_NAME%
set PACKAGE_FOLDER=.\target\%PACKAGE_NAME%
echo %PACKAGE_FOLDER%

mkdir %PACKAGE_FOLDER%
echo. 


echo Creating site folder
call npm run build
SET SITE_BUILD_ERROR_LEVEL=%ERRORLEVEL%

if %SITE_BUILD_ERROR_LEVEL% GEQ 1 GOTO SITE_BUILD_ERROR
xcopy dist\%PACKAGE_NAME%\assets\config\%L_DEPLOY_ENV_NAME% dist\%PACKAGE_NAME%\assets\ /s /e /Y
rmdir dist\%PACKAGE_NAME%\assets\config /Q /S

echo.
echo Getting latest commit id
FOR /f "tokens=1" %%f IN ('git rev-parse --short HEAD' ) DO SET LAST_COMMIT_ID=%%f
SET COMMIT_FILE_PATH=dist\%PACKAGE_NAME%\assets\app-version.txt
echo Copying CommitId  %LAST_COMMIT_ID% to the file %COMMIT_FILE_PATH%
echo.>> %COMMIT_FILE_PATH%
echo| set /p=commitId=%LAST_COMMIT_ID% >> %COMMIT_FILE_PATH%

echo Copying site folder
xcopy dist\%PACKAGE_NAME% %PACKAGE_FOLDER%\ /s /e
if exist .\site rmdir /Q /S .\site 

echo Copying WEB-INF folder for Java deployment
xcopy WEB-INF %PACKAGE_FOLDER%\WEB-INF /s /e /I 

echo.
echo Creating Manifest file
SET MANIFEST_FILE_PATH=%PACKAGE_FOLDER%\MANIFEST.TXT
echo TfsChangesetNum=%LAST_TFS_CHANGESET_NUM% > %MANIFEST_FILE_PATH%
echo GitCommitId=%LAST_COMMIT_ID% >> %MANIFEST_FILE_PATH%
echo BuildTimestamp=%CURR_DATE% %CURR_TIME% >> %MANIFEST_FILE_PATH%
echo BuildEnvironment=%L_DEPLOY_ENV_NAME% >> %MANIFEST_FILE_PATH%
echo BuildUser=%USERNAME% >> %MANIFEST_FILE_PATH%
echo.

echo.
echo Creating WAR file
cd %PACKAGE_FOLDER%
jar -cvf ..\transformerstudio.war  *
cd..\..
rmdir %PACKAGE_FOLDER% /Q /S

echo.
echo ***************************************
echo Build command completed for environment: %L_DEPLOY_ENV_NAME%
echo TFS Changeset Num : %LAST_TFS_CHANGESET_NUM%
echo Git Commitid      : %LAST_COMMIT_ID% 
echo Build output      : %PACKAGE_FOLDER%_%CURR_DATE%_%CURR_TIME%.war 
echo ***************************************
echo.

pause 
GOTO END

:NODE_NOT_FOUND_ERROR
echo.
echo Please install python first!
echo.
pause 
GOTO END

:LOCAL_CHANGES_PRESENT_ERROR
echo.
echo Build cancelled by user due to local changes found.
echo.
pause 
GOTO END

:SITE_BUILD_ERROR
echo.
echo Website build failed. Please scroll up to see error.
echo.
pause
GOTO END 

:TFS_EXE_NOT_FOUND_ERROR
echo.
echo ERROR: Source control validation failed. Please ensure tf.exe is available on PATH. 
echo Usually, it's found at C:\Program Files (x86)\Microsoft Visual Studio 12.0\Common7\IDE
echo.
echo ------------------------------------------------
echo NOTE: To disable this validation in case working in client environment: 
echo Modify below property found at the beginning of this script and rerun.
echo SET SOURCE_CONTROL_VALIDATION=N
echo ------------------------------------------------
echo.
pause 
GOTO END

:: Function Definitions

:fnGetPropFromFile - Read key=value from file
set RESULT=
::for /f %%i in ('findstr %~2 %~1') do (set RESULT=%%i)
for /f "tokens=*" %%i in ('findstr %~2 %~1') do (set RESULT=%%i)
::echo RESULT=%RESULT%
set RESULT=%RESULT: =%
set RESULT=%RESULT:"=%
set RESULT=%RESULT:,=%

FOR /f "tokens=1,2 delims==" %%a IN ("%RESULT%") do (SET RESULT=%%b)
::ECHO %RESULT%

SET "%~3=%RESULT%"
goto:eof

:fnGetTfsChangesetNumber - Get changeset number from TFS
set RESULT=
for /f "tokens=*" %%i in ('tf history ./ /noprompt /recursive  /stopafter:1') do (set RESULT=%%i)
::echo %RESULT%

FOR /f "tokens=1,2 delims= " %%a IN ("%RESULT%") do (SET RESULT=%%a)
::echo %RESULT%
SET "%~1=%RESULT%"
goto:eof


:END
endlocal
