import api
import sys
import multiprocessing

if __name__ == '__main__':
    # Pyinstaller fix
    multiprocessing.freeze_support()

    sys.exit(api.main())