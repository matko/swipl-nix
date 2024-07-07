import re
from functools import total_ordering

pattern = r"^V(\d+)\.(\d+)\.(\d+)(?:-(\w+))?$"

@total_ordering
class Version:
    def __init__(self, m):
        self.major = int(m.group(1))
        self.minor = int(m.group(2))
        self.patch = int(m.group(3))
        self.suffix = m.group(4)

    def parse(tag):
        m = re.match(pattern, tag)
        if not m:
            return None

        return Version(m)

    def is_supported(self):
        return self >= Version.parse('V8.4.0')


    @property
    def version(self):
        return f'{self.major}.{self.minor}.{self.patch}' + (f'-{self.suffix}' if self.suffix is not None else '')

    @property
    def tag(self):
        return f'V{self.version}'

    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor and self.suffix == other.suffix and self.patch == other.patch

    def __lt__(self, other):
        if self.major < other.major:
            return True
        elif self.major > other.major:
            return False

        if self.minor < other.minor:
            return True
        elif self.minor > other.minor:
            return False

        if self.patch < other.patch:
            return True
        elif self.patch > other.patch:
            return False


        if self.suffix is None and other.suffix is not None:
            return True
        if other.suffix is None:
            return False

        return self.suffix < other.suffix

    def __repr__(self):
        return f'Version({self.version})'
