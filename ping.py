import re
import typing
from time import strftime

from cached_property import cached_property
from stream.functions.strings import strip
from stream.io.std import stdin


class Ping(object):
    def __init__(
            self,
            raw_file: str,
            log_file: str,
            timeout_file: str,
            unknown_file: str,
    ):
        self._first_line = None
        self._t = None

        self._raw_file = raw_file
        self._log_file = log_file
        self._timeout_file = timeout_file
        self._unknown_file = unknown_file

    @cached_property
    def _first_regex(self) -> typing.Pattern:
        return re.compile(r'^PING (?P<host>[\d\w\.]+) \((?P<ip>[\d\.]+)\):')

    @cached_property
    def _first_match(self) -> typing.Match:
        if self._first_line is None:
            raise ValueError
        match = self._first_regex.match(self._first_line)
        if match is None:
            raise ValueError
        return match

    @cached_property
    def host(self) -> str:
        return self._first_match.group('host')

    @cached_property
    def ip(self) -> str:
        return self._first_match.group('ip')

    def _log_raw(self, line: str) -> None:
        with open(self._raw_file, 'a') as f:
            f.write(f'{self._t}\t{line}\n')

    @cached_property
    def _success_regex(self) -> typing.Pattern:
        return re.compile(rf'^\d+ bytes from {self.ip}: icmp_seq=(?P<seq>\d+) ttl=\d+ time=(?P<time>[\d\.]+) ms$')

    def _log_success(self, seq: str, time: str) -> None:
        with open(self._log_file, 'a') as f:
            f.write(f'{self._t}\t{seq}\t{time}\n')

    @cached_property
    def _timeout_regex(self) -> typing.Pattern:
        return re.compile(r'^Request timeout for icmp_seq (?P<seq>\d+)$')

    def _log_timeout(self, seq: str) -> None:
        with open(self._log_file, 'a') as f:
            f.write(f'{self._t}\t{seq}\t-1\n')
        with open(self._timeout_file, 'a') as f:
            f.write(f'{self._t}\t{seq}\n')

    def _log_unknown(self, line: str) -> None:
        with open(self._unknown_file, 'a') as f:
            f.write(f'{self._t}\t{line}\n')

    def process_line(self, line: str) -> None:
        self._t = strftime('%Y-%m-%d %H:%M:%S')
        self._log_raw(line)

        success = self._success_regex.match(line)
        if success is not None:
            self._log_success(success.group('seq'), success.group('time'))
            return

        timeout = self._timeout_regex.match(line)
        if timeout is not None:
            self._log_timeout(timeout.group('seq'))
            return

        self._log_unknown(line)

    def __call__(self, lines: typing.Iterator[str]) -> None:
        self._first_line = next(lines)
        for line in lines:
            self.process_line(line)


def main() -> None:
    ping = Ping(
        'raw.log',
        'ping.log',
        'timeout.log',
        'unknown.log',
    )
    stdin.stream | strip | iter > ping


if __name__ == '__main__':
    main()
