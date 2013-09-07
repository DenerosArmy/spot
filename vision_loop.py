from SimpleCV import *
from filters import VisionSystem

def main():
    cam = Camera(2)
    img = cam.getImage()
    display = Display(img.size())
    vision_system = VisionSystem(100, 100, 2)
    try:
        while not display.isDone():
            img = cam.getImage()
            vision_system.add_observation(img)
            vision_system.annotate_img(img)
            img.save(display)
            if display.mouseLeft or display.mouseRight:
                display.done = True
    except KeyboardInterrupt:
        display.done = True

if __name__ == '__main__':
    main()
