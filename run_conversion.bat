@echo off
echo Running voice conversion...
python inference_v2.py --source ./assets/sorce-audio.wav --target ./assets/targets.wav --output ./output
echo Conversion completed!
pause
