"""Create input sketches, not simulated AI results."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def create_samples():
    root = Path(__file__).resolve().parent / "samples"
    root.mkdir(exist_ok=True)
    def font(size):
        for name in ["C:/Windows/Fonts/segoepr.ttf", "C:/Windows/Fonts/arial.ttf", "DejaVuSans.ttf"]:
            try: return ImageFont.truetype(name, size)
            except OSError: pass
        return ImageFont.load_default(size=size)
    image = Image.new("RGB", (900,750), "#fcfaf3")
    d = ImageDraw.Draw(image)
    def box(x,y,w,h): d.rectangle((x,y,x+w,y+h),outline="#51483e",width=3)
    def text(x,y,t,size=20): d.text((x,y),t,font=font(size),fill="#51483e")
    text(48,28,"MY LOGIN PAGE",28)
    text(560,32,"keep it simple!")
    box(45,85,810,610)
    text(80,110,"[ N ]  Napkin Notes")
    d.line((70,155,825,155),fill="#51483e",width=2)
    box(235,200,430,420)
    text(340,230,"Welcome back",26)
    text(278,279,"Sign in to your workspace",18)
    text(270,327,"Email",19)
    box(270,360,360,48)
    text(285,372,"you@example.com",16)
    text(270,425,"Password",19)
    box(270,455,360,48)
    text(287,463,"* * * * * * * *")
    box(270,535,360,48)
    text(402,544,"Sign in")
    text(235,645,"center card / rounded corners / indigo button",16)
    image.save(root / "login-sketch.png")
    a = ImageDraw.Draw(image)
    a.text((545,110),"Add dark mode toggle",font=font(18),fill="#9b3a36")
    a.line([(680,143),(740,175),(805,175)],fill="#9b3a36",width=3)
    a.ellipse((785,163,827,185),outline="#9b3a36",width=2)
    target = root / "annotations"
    target.mkdir(exist_ok=True)
    image.save(target / "dark-mode-edit.png")
    print("Created login sketch and annotation sample.")

if __name__ == "__main__":
    create_samples()
