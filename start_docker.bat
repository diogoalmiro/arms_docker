cd /d "%~dp0"
docker run -it -v %cd%/workflow:/home/App arms_workflow
