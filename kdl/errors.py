from __future__ import annotations

from rich.text import Text

from . import t


class ParseError(Exception):
    def __init__(self, s: t.Stream, i: int, details: str) -> None:

        self.msg = f"{s.loc(i)} {details}"
        if len(self.msg) > 78:
            self.msg = f"{s.loc(i)}\n  {details}"

        self.fancy_message = self._fancy_message(s, i, details)
        super().__init__(self.msg)

    def _fancy_message(
            self,
            stream: t.Stream,
            idx: int,
            msg: str,
            context: int = 2
    ) -> Text:
        text = stream._chars.splitlines()
        line = stream.line(idx)
        col = stream.col(idx)

        start = max(1, line - context)
        end = min(len(text), line + context)

        lines: Text = Text(f"{stream.filename} {line}:{col} {msg}\n")

        for lineno in range(start, end + 1):
            prefix = ">" if lineno == line else " "
            code = text[lineno - 1]
            lines.append(Text(
                f"{prefix} {lineno:4d} | {code}\n",
                style="bold red" if lineno == line else ""
            ))
            if lineno == line:
                lines.append(Text(" " * (col + 7) + "^\n", style="bold red"))

        return lines


class ParseFragment:
    def __init__(self, fragment: str, s: t.Stream, i: int) -> None:
        self.fragment = fragment
        self._s = s
        self._i = i

    def error(self, msg: str) -> ParseError:
        return ParseError(self._s, self._i, msg)
