"""支持 ``python -m minichain`` 直接运行。"""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())