"""Direction and dates of WhatsApp chat exports are derived only where the exports settle them."""
import datetime
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.artifacts.whatsappExportedchats import whatsappExportedchats

DIRECTION, SENDER, CONVERSATION, BASIS = 1, 2, 3, 7


class Context:
    def __init__(self, paths):
        self.paths = [str(p) for p in paths]

    def get_files_found(self):
        return self.paths

    def get_relative_path(self, path):
        return pathlib.Path(path).name


def write(directory, folder, name, lines):
    path = pathlib.Path(directory) / folder / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return path


class TestExportedDirection(unittest.TestCase):
    def rows(self, *files):
        return whatsappExportedchats.__wrapped__(Context(files))[1]

    def test_one_to_one_and_group_share_one_owner(self):
        with tempfile.TemporaryDirectory() as d:
            one = write(d, 'a', 'WhatsApp Chat with Alice.txt', [
                '13/12/2025, 09:00 - Alice: Hi', '13/12/2025, 09:01 - Owner: Hello'])
            group = write(d, 'g', 'WhatsApp Chat with Group.txt', [
                '14/12/2025, 10:00 - Alice created group "Group"',
                '14/12/2025, 10:01 - Bob: Hi all', '14/12/2025, 10:02 - Owner: Hi Bob'])
            rows = self.rows(one, group)
        by_text = {(r[CONVERSATION], r[SENDER]): r for r in rows}
        self.assertEqual(by_text[('Alice', 'Owner')][DIRECTION], 'Outgoing')
        self.assertEqual(by_text[('Alice', 'Alice')][DIRECTION], 'Incoming')
        self.assertEqual(by_text[('Group', 'Owner')][DIRECTION], 'Outgoing')
        self.assertEqual(by_text[('Group', 'Owner')][BASIS], 'owner name from one-to-one chats')
        self.assertEqual(by_text[('Group', 'Bob')][DIRECTION], 'Incoming')
        self.assertEqual(by_text[('Group', '')][DIRECTION], '')
        self.assertEqual(rows[0][0], datetime.datetime(2025, 12, 13, 9, 0))

    def test_exports_from_two_phones_leave_groups_blank(self):
        with tempfile.TemporaryDirectory() as d:
            first = write(d, 'a', 'WhatsApp Chat with Alice.txt', [
                '13/12/2025, 09:00 - Alice: Hi', '13/12/2025, 09:01 - Owner One: Hello'])
            second = write(d, 'b', 'WhatsApp Chat with Bob.txt', [
                '13/12/2025, 09:00 - Bob: Hi', '13/12/2025, 09:01 - Owner Two: Hello'])
            group = write(d, 'g', 'WhatsApp Chat with Group.txt', [
                '14/12/2025, 10:01 - Bob: Hi all', '14/12/2025, 10:02 - Owner One: Hi'])
            rows = self.rows(first, second, group)
        group_rows = [r for r in rows if r[CONVERSATION] == 'Group']
        self.assertEqual([r[DIRECTION] for r in group_rows], ['', ''])
        self.assertEqual([r[DIRECTION] for r in rows if r[CONVERSATION] == 'Bob'], ['Incoming', 'Outgoing'])

    def test_ios_group_system_message_and_ambiguous_dates(self):
        with tempfile.TemporaryDirectory() as d:
            one = write(d, 'WhatsApp Chat - Alice', '_chat.txt', [
                '[1/2/25, 9:05:00 AM] Alice: Hi', '[1/2/25, 1:15:00 PM] Owner: Hello'])
            group = write(d, 'WhatsApp Chat - Group', '_chat.txt', [
                '[1/2/25, 9:00:00 AM] Group: ‎Alice created this group',
                '[1/2/25, 9:01:00 AM] Alice: Welcome'])
            rows = self.rows(one, group)
        self.assertEqual({r[0] for r in rows}, {''})
        system = [r for r in rows if r[SENDER] == 'Group'][0]
        self.assertEqual(system[DIRECTION], '')
        self.assertEqual(system[4], 'Alice created this group')


if __name__ == '__main__':
    unittest.main()
