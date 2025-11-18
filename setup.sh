!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'


echo ""
echo -e "${GREEN}Installing color-converter dependencies${NC}"
echo ""
python3 -m venv backgrounds/color_extractor
source backgrounds/color_extractor/bin/activate
pip install pillow numpy scikit-learn
deactivate

echo ""
echo -e "${GREEN}Setup complete!${NC}"

