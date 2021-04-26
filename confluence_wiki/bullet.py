from utils import close_tag, enclosed_tag, open_tag


class BulletList:

    def __init__(self, source):
        self.current_level = False
        self.last_level = False
        self.prefix = ""
        self.source = source
        self.wrapper_tag_type = ""

    def calculate_level(self, *args, **kwargs):
        raise NotImplementedError

    def proccess_bullets(self, line):
        line_replacement = ""

        # Current item is a bullet point
        if self.current_level:
            # Open a new level
            if not self.last_level or self.current_level > self.last_level:
                line_replacement += open_tag(self.wrapper_tag_type)
            # Close existing level i.e the previous indentation has ended
            elif self.last_level > self.current_level:
                line_replacement += close_tag(self.wrapper_tag_type)

            cleaned_line = line[len(self.prefix):]
            line_replacement += enclosed_tag("li", cleaned_line)
        # Current item is not a bullet point, may need to close off existing levels
        else:
            if self.last_level:
                # close levels
                self.cleanup_tag_closure(self.last_level)

            line_replacement += line

        self.last_level = self.current_level
        return line_replacement

    def cleanup_tag_closure(self, last_level):
        output = ""
        for level in range(0, last_level):
            output += close_tag(self.wrapper_tag_type)
        return output

    def parse_string(self):
        lines = io.StringIO(self.source)
        output = ""

        while True:
            line = lines.readline()

            # Clean up we're done and no more lines exist
            if not line:
                if self.last_level:
                    # close levels
                    output += self.cleanup_tag_closure(self.last_level)
                break

            self.current_level, self.prefix = self.calculate_level(line)
            output += self.proccess_bullets(line)

        return output


class OrderedBulletList(BulletList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wrapper_tag_type = "ol"

    def calculate_level(self, line):
        if line.startswith("# "):
            return 1, "# "
        elif line.startswith("## "):
            return 2, "## "
        elif line.startswith("### "):
            return 3, "### "
        elif line.startswith("#### "):
            return 4, "#### "
        elif line.startswith("##### "):
            return 5, "##### "
        elif line.startswith("###### "):
            return 6, "###### "
        return False, ""


class UnOrderedBulletList(BulletList):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wrapper_tag_type = "ul"

    def calculate_level(self, line):
        if line.startswith("* "):
            return 1, "* "
        elif line.startswith("** "):
            return 2, "** "
        elif line.startswith("*** "):
            return 3, "*** "
        elif line.startswith("**** "):
            return 4, "**** "
        elif line.startswith("***** "):
            return 5, "***** "
        elif line.startswith("****** "):
            return 6, "****** "
        return False, ""
