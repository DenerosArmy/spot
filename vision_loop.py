from vision import *

def main():
    vision_system = ContourClassifier(trainable=True)
    while True:
        vision_system.step()

if __name__ == '__main__':
    main()
