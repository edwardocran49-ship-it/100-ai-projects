from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
out=Path(__file__).parent/"data";out.mkdir(exist_ok=True)
image=Image.new("RGB",(1000,520),"#ece7dc");draw=ImageDraw.Draw(image);font=ImageFont.truetype("arial.ttf",72);small=ImageFont.truetype("arial.ttf",34)
for x,name,price,color in [(60,"GROUND COFFEE","$3.49","#7c2d12"),(535,"GREEN TEA","$7.99","#14532d")]:
 draw.rounded_rectangle((x,70,x+405,440),25,fill="white",outline=color,width=8);draw.rectangle((x,70,x+405,150),fill=color);draw.text((x+24,90),name,fill="white",font=small);draw.text((x+78,230),price,fill="#111827",font=font)
image.save(out/"store_shelf.png")
print(out/"store_shelf.png")
