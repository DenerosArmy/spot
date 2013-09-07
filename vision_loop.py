from vision import *

def main():
    vision_system = ContourClassifier()
    while True:
        vision_system.step()

if __name__ == '__main__':
    main()
