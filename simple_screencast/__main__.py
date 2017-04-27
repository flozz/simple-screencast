import sys

from .application import SimpleScreencastApplication


def main():
    app = SimpleScreencastApplication()
    app.run(sys.argv)


if __name__ == "__main__":
    main()
