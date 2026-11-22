"""
Generate synthetic Wire cross-platform backups (.wbu) for the wireBackup tests.

Every value here is fabricated: user IDs, names, handles, texts, asset keys and hashes. A real backup
is a person's conversations, so none can be sanitised into a fixture. The envelope follows
BackupHeaderSerializer.kt and MPBackupExporter.kt of wireapp/kalium, and the pages follow its
backup.proto, both at commit 8ea735e3cd0c12eb8a23250db48f4e591d2cbc70; page names, page order and the
fixed BackupInfo values follow real unencrypted backups made by Wire Desktop and Wire for Android. Covered:

  - backup A, unencrypted, whose account is not among its users (as in the real Desktop backups):
    a named group, an unnamed conversation with one other sender, an unnamed conversation only the
    account wrote in, a conversation without messages named '_' (as in each real backup), and
    messages in a conversation the conversations page does not list
  - text with a line break, a text that is also valid protobuf (which a schemaless decoder misreads),
    an edited text, a quote, a quote of a message not in the backup, a mention of a user and of
    everyone, a reaction page with a reaction to a message not in the backup (as in the real Android one)
  - an image asset with metadata and AES-GCM, an audio asset without a name, a location
  - a sender the users page does not list, a sender client ID stored as 'null', and a field number
    backup.proto does not name, which must be skipped and logged
  - backup B, encrypted: header only, listed in the Backup artifact and not opened
  - backup C, unencrypted, of another account and named as Wire for Android names its backups,
    sharing a conversation ID with A, which must stay a conversation of its own in the conversation view
  - a .wbu file without the WBUX header, which must add nothing

Usage:
    python admin/test/scripts/gen_wire_backup_synth.py [output_dir]

Then zip the output folder and feed it to make_test_data.py.
"""
import io
import os
import shutil
import struct
import sys
import zipfile

BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "synth_wire_backup")

DOMAIN = "wire.example.org"
SELF = "00000000-0000-4000-8000-00000000a001"
ALICE = "00000000-0000-4000-8000-00000000a002"
BOB = "00000000-0000-4000-8000-00000000a003"
GHOST = "00000000-0000-4000-8000-00000000a004"
OTHER_SELF = "00000000-0000-4000-8000-00000000b001"
GROUP = "00000000-0000-4000-8000-0000000c0001"
DIRECT = "00000000-0000-4000-8000-0000000c0002"
NOTES = "00000000-0000-4000-8000-0000000c0003"
EMPTY = "00000000-0000-4000-8000-0000000c0004"
UNLISTED = "00000000-0000-4000-8000-0000000c0005"
T0 = 1735732800000  # 2025-01-01T12:00:00Z


# ---- protobuf encoding ----

def varint(value):
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def f_int(number, value):
    return varint(number << 3) + varint(value)


def f_bytes(number, value):
    if isinstance(value, str):
        value = value.encode("utf-8")
    return varint(number << 3 | 2) + varint(len(value)) + value


def f_float(number, value):
    return varint(number << 3 | 5) + struct.pack("<f", value)


def qid(number, value, domain=DOMAIN):
    return f_bytes(number, f_bytes(1, value) + f_bytes(2, domain))


def info(account):
    return f_bytes(1, f_bytes(1, "Common") + f_bytes(2, "1.0") + qid(3, account)
                   + f_int(4, T0 + 86400000 * 30) + f_bytes(5, "lol"))


def user(uid, name, handle):
    return f_bytes(4, qid(1, uid) + f_bytes(2, name) + f_bytes(3, handle))


def conversation(cid, name, modified=None):
    body = qid(1, cid) + f_bytes(2, name)
    if modified is not None:
        body += f_int(3, modified)
    return f_bytes(2, body)


def message(mid, minute, sender, cid, content, client="c1a2b3c4d5e6f701", edited=None, extra=b""):
    body = (f_bytes(1, mid) + f_int(2, T0 + minute * 60000) + qid(3, sender) + f_bytes(4, client)
            + qid(5, cid) + content + f_int(9, minute + 1))
    if edited is not None:
        body += f_int(10, T0 + edited * 60000)
    return f_bytes(3, body + extra)


def text(value, quoted=None, mentions=(), everyone=()):
    body = f_bytes(1, value)
    for start, length, uid in mentions:
        body += f_bytes(2, f_int(1, start) + f_int(2, length) + qid(3, uid))
    if quoted:
        body += f_bytes(3, quoted)
    for start, length in everyone:
        body += f_bytes(4, f_int(1, start) + f_int(2, length))
    return f_bytes(6, body)


def reaction(mid, cid, entries):
    body = f_bytes(1, mid) + qid(2, cid)
    for emoji, users in entries:
        body += f_bytes(3, f_bytes(1, emoji) + b"".join(qid(2, u) for u in users))
    return f_bytes(5, body)


# ---- envelope ----

def header(encrypted, salt_byte):
    out = b"WBUX" + b"\x00" + struct.pack(">H", 4) + bytes([salt_byte]) * 16 + bytes([salt_byte ^ 0xFF]) * 32
    out += struct.pack(">I", 4) + struct.pack(">I", 33554432) + (b"\x01" if encrypted else b"\x00")
    return out + b"\x00" * (1024 - len(out))


def write_backup(path, pages, encrypted=False, salt_byte=0x11):
    with open(path, "wb") as handle:
        handle.write(header(encrypted, salt_byte))
        if encrypted:
            handle.write(bytes((i * 37 + 11) & 0xFF for i in range(24 + 512)))
            return
        handle.write(b"\x00" * 24)
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, data in pages:
                info_ = zipfile.ZipInfo(name, date_time=(2025, 1, 31, 12, 0, 0))
                info_.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info_, data)
        handle.write(buf.getvalue())


def backup_a():
    image = f_bytes(7, f_bytes(1, "image/jpeg") + f_int(2, 48213) + f_bytes(3, "beach.jpg")
                    + f_bytes(4, bytes(range(32))) + f_bytes(5, bytes(range(32, 64)))
                    + f_bytes(6, "3-2-00000000-0000-4000-8000-0000000a5501") + f_bytes(7, "tok-synthetic-1")
                    + f_bytes(8, DOMAIN) + f_int(9, 1)
                    + f_bytes(10, f_int(1, 1024) + f_int(2, 768)))
    audio = f_bytes(7, f_bytes(1, "audio/mp4") + f_int(2, 9120)
                    + f_bytes(4, bytes(range(64, 96))) + f_bytes(5, bytes(range(96, 128)))
                    + f_bytes(6, "3-2-00000000-0000-4000-8000-0000000a5502")
                    + f_bytes(12, f_int(1, 4500) + f_bytes(2, bytes([1, 5, 9, 5, 1]))))
    location = f_bytes(8, f_float(1, 13.405) + f_float(2, 52.52) + f_bytes(3, "Synthetic Square") + f_int(4, 14))
    messages = [
        message("m-001", 0, ALICE, GROUP, text("Welcome to the group")),
        message("m-002", 1, SELF, GROUP, text("Thanks!\nGlad to be here")),
        message("m-003", 2, BOB, GROUP, text("@Alice Example and @all: meeting at noon",
                                             mentions=[(0, 14, ALICE)], everyone=[(19, 4)])),
        message("m-004", 3, SELF, GROUP, text("Noted, see you there", quoted="m-003"), edited=5),
        message("m-005", 4, ALICE, GROUP, image),
        message("m-006", 6, GHOST, GROUP, text("I left the company"), client="null"),
        message("m-007", 7, BOB, GROUP, location),
        message("m-101", 10, ALICE, DIRECT, text("(1(2\r\nabc")),
        message("m-102", 11, SELF, DIRECT, audio),
        message("m-103", 12, SELF, DIRECT, text("Call me later"), extra=f_int(15, 7)),
        message("m-104", 13, ALICE, DIRECT, text("Replying to a message that is gone", quoted="m-gone")),
        message("m-201", 20, SELF, NOTES, text("Note to self")),
        message("m-301", 30, BOB, UNLISTED, text("A conversation the backup does not list")),
    ]
    pages = [
        ("messages_0.binpb", info(SELF) + b"".join(messages[:7])),
        ("messages_1.binpb", info(SELF) + b"".join(messages[7:])),
        ("users_0.binpb", info(SELF) + user(ALICE, "Alice Example", "alice.example")
         + user(BOB, "Bob Sample", "bob.sample")),
        ("conversations_0.binpb", info(SELF) + conversation(GROUP, "Synthetic Group", T0 + 600000)
         + conversation(DIRECT, "", T0 + 720000) + conversation(NOTES, "", T0 + 1200000)
         + conversation(EMPTY, "_", T0)),
        ("reactions_0.binpb", info(SELF) + reaction("m-001", GROUP, [("👍", [SELF, BOB])])
         + reaction("m-005", GROUP, [("❤️", [BOB])]) + reaction("m-gone", DIRECT, [("😂", [ALICE])])),
    ]
    return pages


def backup_c():
    return [
        ("messages_0.binpb", info(OTHER_SELF)
         + message("m-901", 40, OTHER_SELF, GROUP, text("Same conversation ID, other backup"))),
        ("users_0.binpb", info(OTHER_SELF) + user(ALICE, "Alice Example", "alice.example")),
        ("conversations_0.binpb", info(OTHER_SELF) + conversation(GROUP, "Synthetic Group")),
    ]


def main():
    if os.path.isdir(BASE):
        shutil.rmtree(BASE)
    os.makedirs(os.path.join(BASE, "second"))
    write_backup(os.path.join(BASE, "Wire-owner-Backup_2025-01-31.wbu"), backup_a())
    write_backup(os.path.join(BASE, "Wire-owner-Backup_2025-01-31_enc.wbu"), [], encrypted=True, salt_byte=0x22)
    write_backup(os.path.join(BASE, "second", "Wire-other-2025-02-01_10-20-30.wbu"), backup_c(), salt_byte=0x33)
    with open(os.path.join(BASE, "not-a-backup.wbu"), "w", encoding="utf-8") as handle:
        handle.write("This file only has the extension.\n")
    print(f"Synthetic Wire backups written to {BASE}")


if __name__ == "__main__":
    main()
