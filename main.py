# This Python file uses the following encoding: utf-8
import time

import modules.mm_reality as mm
import modules.sreality as sreal
import modules.reality as real


if __name__ == '__main__':
    pages = [sreal, real, mm]
    try:
        for name in pages:
            name.GetScraped()

    finally:
        time.sleep(5)


