from filters import VisionSystem

def main():
    vision_system = VisionSystem()
    while True:
        vision_system.step()

if __name__ == '__main__':
    main()
