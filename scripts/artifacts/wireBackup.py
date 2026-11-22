__artifacts_v2__ = {
    "wireBackupMessages": {
        "name": "Wire Backup - Messages",
        "description": "Text, asset and location messages of an unencrypted Wire cross-platform backup (.wbu), with "
                       "edits, quotes, mentions and reactions as the backup records them.",
        "author": "@kalink0",
        "creation_date": "2026-11-22",
        "last_update_date": "2026-11-22",
        "requirements": "none",
        "category": "Wire Backup",
        "notes": "The backup holds no media files: an attachment is recorded only as a reference to the file on "
                 "the Wire backend (see the Asset References artifact), so no message shows its media. "
                 "Reads a .wbu file in Wire's cross-platform backup format: a 1024-byte header starting with WBUX, "
                 "then a ZIP of protobuf pages, decoded here against backup.proto of wireapp/kalium (see the Backup "
                 "artifact). An encrypted backup is listed in the Backup artifact and not opened; RLEAPP cannot pass "
                 "a password to an artifact yet. One row per ExportedMessage. The exporter writes only text, asset "
                 "and location messages: system messages, calls and other content are not in the backup. Sent At "
                 "is time_iso and Last Edited At is lastEditTime, both Unix milliseconds, shown in UTC. Direction "
                 "is Outgoing when the sender's qualified user ID is the backup's own (BackupInfo.userId) and "
                 "Incoming otherwise; the Sender of an outgoing message is 'Local User', as the Desktop backups "
                 "tested did not list the account among their users. Other senders are named from the backup's "
                 "users, with the handle; a sender the backup does not list is shown by user ID, as a few were in "
                 "the Desktop backups. Conversation is the conversation's name; the backup does not store whether "
                 "a conversation is one-to-one or a group, and an unnamed conversation is labelled 'Unnamed:' with "
                 "the other senders seen in it, which need not be all its members, or with its ID when only the "
                 "account wrote in it. Conversation Key (source file and conversation ID) is what LAVA's "
                 "conversation view groups on, so two backups stay apart; when more than one backup is read, "
                 "Conversation ends with the backup's file in brackets, so the same chat from two backups can be "
                 "told apart. Assets are references to files on the "
                 "Wire backend, not the files: the backup holds no media, so there is no media column (see the "
                 "Asset References artifact). Sender Client ID is reported as stored; the Desktop backups held the "
                 "string 'null' on some rows, the Android backup on none. Quoted Message resolves "
                 "quoted_message_id within the same backup and is blank when the quoted message is not in it, as "
                 "for a few quotes of the Android backup. Mentions lists the mentioned users, and 'everyone' for a "
                 "mention of all. Reactions lists each emoji with the users who gave it; a reaction to a message "
                 "the backup does not hold is logged and not reported, as some of the Android backup were. "
                 "Latitude and Longitude are stored as 32-bit floats and shown to the seven significant digits "
                 "these hold. Latitude, Longitude and Location Name had no value on any row of the tested backups; "
                 "they are checked only on a synthetic fixture, as is the 'everyone' mention. The Desktop backups "
                 "held text messages only, with no quote, mention or reaction, and carried web_pk on every message, "
                 "which backup.proto describes as web-specific; it is not reported. Tested on two unencrypted "
                 "backups made by Wire Desktop and one made by Wire for Android.",
        "paths": ('*.wbu',),
        "output_types": "standard",
        "artifact_icon": "message-square",
        "data_views": {
            "conversation": {
                "conversationDiscriminatorColumn": "Conversation Key",
                "conversationLabelColumn": "Conversation",
                "textColumn": "Message",
                "directionColumn": "Direction",
                "directionSentValue": "Outgoing",
                "timeColumn": "Sent At",
                "senderColumn": "Sender",
            }
        },
    },
    "wireBackupAssets": {
        "name": "Wire Backup - Asset References",
        "description": "Asset messages of an unencrypted Wire cross-platform backup (.wbu) with the backend asset ID, "
                       "token, key and hash that locate and decrypt each file on the Wire backend.",
        "author": "@kalink0",
        "creation_date": "2026-11-22",
        "last_update_date": "2026-11-22",
        "requirements": "none",
        "category": "Wire Backup",
        "notes": "The backup holds no media files. The ZIP of the tested backups held only protobuf pages, and "
                 "kalium's exporter (MPBackupExporter.kt) writes nothing else into it. The files themselves can "
                 "only come from the Wire backend or from the app's own storage on a device, neither of which "
                 "this artifact reads. One row per ExportedMessage with asset content in a backup read as in the "
                 "Messages artifact, holding what the sending client recorded about each file: MIME type, "
                 "size and name as sent, the asset ID, token and domain on the Wire backend, the OTR Key the file "
                 "is encrypted with and the SHA-256 of the encrypted file, both hex. Encryption is the stored "
                 "algorithm (AES-CBC or AES-GCM), blank when not stored. Width, Height and Duration come from the "
                 "image, video or audio metadata where present. Whether the file can still be fetched from the "
                 "backend is not checked. Only the Android backup tested held asset messages: images and videos "
                 "with metadata and files without, some without a file name, token or MIME type. Encryption held "
                 "AES-CBC on all rows of it. Asset Domain held one value on all rows of it, the domain of the "
                 "account. It "
                 "held no audio metadata, so Duration (ms) is checked on audio only on a synthetic fixture.",
        "paths": ('*.wbu',),
        "output_types": "standard",
        "artifact_icon": "paperclip",
    },
    "wireBackupConversations": {
        "name": "Wire Backup - Conversations",
        "description": "Conversations of an unencrypted Wire cross-platform backup (.wbu) with the span and count of "
                       "the messages the backup holds for each.",
        "author": "@kalink0",
        "creation_date": "2026-11-22",
        "last_update_date": "2026-11-22",
        "requirements": "none",
        "category": "Wire Backup",
        "notes": "One row per ExportedConversation in a backup read as in the Messages artifact. Name is as stored; "
                 "it was empty for most conversations of the tested backups and '_' for some without messages in "
                 "each, whose meaning is not established. The backup does not store whether "
                 "a conversation is one-to-one or a group. Participants Seen lists the senders of the conversation's "
                 "messages in the backup, which need not be all its members. Last Modified At and Last Read At are "
                 "lastModifiedTime and lastReadTime, Unix milliseconds in UTC; Last Read At was blank on every row "
                 "of the tested backups. First Message, Last Message and Messages cover the messages of the backup "
                 "only, which are text, asset and location messages; most conversations of the tested backups had "
                 "none, so First Message and Last Message are blank on those rows. Listed in Conversations is No "
                 "for a conversation that only messages refer to. Listed in Conversations held Yes on all rows of "
                 "the tested backups.",
        "paths": ('*.wbu',),
        "output_types": "standard",
        "artifact_icon": "message-circle",
    },
    "wireBackupUsers": {
        "name": "Wire Backup - Users",
        "description": "Users of an unencrypted Wire cross-platform backup (.wbu) with name, handle and the number of "
                       "messages they sent in it.",
        "author": "@kalink0",
        "creation_date": "2026-11-22",
        "last_update_date": "2026-11-22",
        "requirements": "none",
        "category": "Wire Backup",
        "notes": "One row per ExportUser in a backup read as in the Messages artifact: qualified user ID, display "
                 "name and handle as stored. The exporter writes the other users the client knows, so the list is "
                 "not limited to contacts and need not include the account itself. Is Account is Yes for the "
                 "account's own user; the Android backup tested listed it, the Desktop backups did not. Messages "
                 "Sent counts the user's messages in the backup.",
        "paths": ('*.wbu',),
        "output_types": "standard",
        "artifact_icon": "users",
    },
    "wireBackupInfo": {
        "name": "Wire Backup - Backup",
        "description": "Header and account of each Wire cross-platform backup file (.wbu), encrypted or not, with the "
                       "number of records found in it.",
        "author": "@kalink0",
        "creation_date": "2026-11-22",
        "last_update_date": "2026-11-22",
        "requirements": "none",
        "category": "Wire Backup",
        "notes": "One row per .wbu file whose header starts with WBUX. The header layout is that of "
                 "BackupHeaderSerializer.kt in wireapp/kalium: format, header version, salt, hashed user ID, the "
                 "Argon2 operations and memory limits, and the encrypted flag, padded to 1024 bytes. An encrypted "
                 "backup is listed with its header only; its contents are XChaCha20-Poly1305 encrypted under a key "
                 "derived from the password and are not opened. Account User ID and Created At (creation_time, Unix "
                 "milliseconds, UTC) come from the BackupInfo of the first page of an unencrypted backup. The "
                 "exporter writes the fixed values 'Common', '1.0' and 'lol' as platform, version and client ID, so "
                 "they are not reported. The Hashed User ID is an Argon2 hash of the account's user ID; it is "
                 "reported, not checked against Account User ID. Created At (from Name) is the date, or date and "
                 "time, in the file name as written there: Wire Desktop named the tested backups "
                 "Wire-<handle>-Backup_<date>.wbu, Wire for Android Wire-<handle>-<date>_<time>.wbu; the time zone "
                 "of that name is not recorded. Reactions counts the messages with reactions. Header Version held "
                 "4 on all rows of the tested backups. Argon2 Operations Limit held 4 on all rows of the tested "
                 "backups. Argon2 Memory Limit (bytes) held 33554432 on all rows of the tested backups; both are "
                 "the defaults in kalium's Hash.kt. Read Error "
                 "holds why the ZIP of an unencrypted backup could not be opened. Read Error had no value on any "
                 "row of the tested backups.",
        "paths": ('*.wbu',),
        "output_types": "standard",
        "artifact_icon": "archive",
    },
}

import os
import re
import struct
import zipfile

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc, logfunc

# Format references are to wireapp/kalium at commit 8ea735e3cd0c12eb8a23250db48f4e591d2cbc70
# (https://github.com/wireapp/kalium/tree/8ea735e3cd0c12eb8a23250db48f4e591d2cbc70):
# - tools/protobuf-codegen/src/main/proto/backup.proto: the page schema decoded below.
# - domain/backup/src/commonMain/kotlin/com/wire/backup/envelope/BackupHeaderSerializer.kt: the header.
# - domain/backup/src/commonMain/kotlin/com/wire/backup/dump/MPBackupExporter.kt: an unencrypted backup
#   is the header, 24 zero bytes in place of the XChaCha20-Poly1305 stream header, then the ZIP.
# - logic/src/commonMain/kotlin/com/wire/kalium/logic/feature/backup/mapper/BackupDataMappers.kt: only
#   text, asset and location messages are exported.
# The decoder reads the protobuf wire format against that schema, so a text that happens to be valid
# protobuf stays text. Fields the schema does not name are skipped and counted.

HEADER_MAGIC = b'WBUX'
HEADER_SIZE = 1024
LOCAL_USER = 'Local User'
FILE_NAME_DATE = re.compile(r'^Wire-.+-(?:Backup_)?(\d{4}-\d{2}-\d{2}(?:_\d{2}-\d{2}-\d{2})?)(?:_enc)?\.wbu$',
                            re.IGNORECASE)


class _ProtoError(ValueError):
    pass


def _varint(buf, pos):
    result = shift = 0
    while True:
        if pos >= len(buf) or shift > 63:
            raise _ProtoError('truncated varint')
        byte = buf[pos]
        pos += 1
        result |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return result, pos
        shift += 7


def _fields(buf):
    """Split one protobuf message into {field number: [raw values]} by wire type."""
    out = {}
    pos = 0
    while pos < len(buf):
        tag, pos = _varint(buf, pos)
        number, wire_type = tag >> 3, tag & 7
        if wire_type == 0:
            value, pos = _varint(buf, pos)
        elif wire_type == 1:
            value, pos = buf[pos:pos + 8], pos + 8
        elif wire_type == 2:
            length, pos = _varint(buf, pos)
            value, pos = buf[pos:pos + length], pos + length
        elif wire_type == 5:
            value, pos = buf[pos:pos + 4], pos + 4
        else:
            raise _ProtoError(f'unsupported wire type {wire_type}')
        if pos > len(buf):
            raise _ProtoError('truncated field')
        out.setdefault(number, []).append(value)
    return out


class _Message:
    """One decoded protobuf message, read by field number as the schema types it."""

    def __init__(self, buf, known, unknown):
        self.raw = _fields(buf)
        for number in self.raw:
            if number not in known:
                unknown[number] = unknown.get(number, 0) + 1

    def has(self, number):
        return number in self.raw

    def str(self, number):
        values = self.raw.get(number)
        if not values or not isinstance(values[-1], (bytes, bytearray)):
            return ''
        return bytes(values[-1]).decode('utf-8', errors='replace')

    def bytes(self, number):
        values = self.raw.get(number)
        return bytes(values[-1]) if values and isinstance(values[-1], (bytes, bytearray)) else b''

    def int(self, number):
        values = self.raw.get(number)
        if not values or not isinstance(values[-1], int):
            return None
        value = values[-1]
        return value - (1 << 64) if value >= 1 << 63 else value

    def float(self, number):
        values = self.raw.get(number)
        if not values or not isinstance(values[-1], (bytes, bytearray)) or len(values[-1]) != 4:
            return None
        # A protobuf float is 32 bits wide: seven significant digits are all it holds.
        return float(f"{struct.unpack('<f', values[-1])[0]:.7g}")

    def messages(self, number):
        return [v for v in self.raw.get(number, []) if isinstance(v, (bytes, bytearray))]


# Field numbers the decoder reads, per message type of backup.proto.
_KNOWN = {
    'BackupData': {1, 2, 3, 4, 5},
    'BackupInfo': {1, 2, 3, 4, 5},
    'QualifiedId': {1, 2},
    'User': {1, 2, 3},
    'Conversation': {1, 2, 3, 4},
    'Message': {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
    'Reaction': {1, 2, 3},
    'EmojiReaction': {1, 2},
    'Text': {1, 2, 3, 4},
    'Mention': {1, 2, 3},
    'Asset': set(range(1, 14)),
    'Meta': {1, 2, 3},
    'Location': {1, 2, 3, 4},
}


class _Backup:
    def __init__(self, path):
        self.path = path
        self.header = None
        self.encrypted = False
        self.account = None
        self.created = None
        self.users = {}
        self.conversations = {}
        self.conversation_order = []
        self.messages = []
        self.reactions = {}
        self.pages = 0
        self.unknown = {}
        self.error = ''

    def msg(self, buf, kind):
        return _Message(buf, _KNOWN[kind], self.unknown.setdefault(kind, {}))

    def qid(self, buf):
        message = self.msg(buf, 'QualifiedId')
        return message.str(1).lower(), message.str(2).lower()

    def load_pages(self):
        with zipfile.ZipFile(self.path) as archive:
            names = [n for n in archive.namelist() if n.lower().endswith('.binpb')]
            names.sort(key=_page_sort_key)
            for name in names:
                try:
                    page = self.msg(archive.read(name), 'BackupData')
                    self._load_page(page)
                except (_ProtoError, struct.error, zipfile.BadZipFile, OSError) as ex:
                    logfunc(f'Wire Backup: page {name} of {os.path.basename(self.path)} could not be read: {ex}')
                    continue
                self.pages += 1

    def _load_page(self, page):
        for buf in page.messages(1):
            if self.account is None:
                info = self.msg(buf, 'BackupInfo')
                if info.has(3):
                    self.account = self.qid(info.messages(3)[0])
                self.created = info.int(4)
        for buf in page.messages(4):
            user = self.msg(buf, 'User')
            if user.has(1):
                self.users[self.qid(user.messages(1)[0])] = (user.str(2), user.str(3))
        for buf in page.messages(2):
            conversation = self.msg(buf, 'Conversation')
            if not conversation.has(1):
                continue
            key = self.qid(conversation.messages(1)[0])
            if key not in self.conversations:
                self.conversation_order.append(key)
            self.conversations[key] = (conversation.str(2), conversation.int(3), conversation.int(4))
        for buf in page.messages(3):
            self.messages.append(self._message(self.msg(buf, 'Message')))
        for buf in page.messages(5):
            reaction = self.msg(buf, 'Reaction')
            conversation = self.qid(reaction.messages(2)[0]) if reaction.has(2) else ('', '')
            entries = self.reactions.setdefault((conversation, reaction.str(1).lower()), [])
            for emoji_buf in reaction.messages(3):
                emoji = self.msg(emoji_buf, 'EmojiReaction')
                entries.append((emoji.str(1), [self.qid(u) for u in emoji.messages(2)]))

    def _message(self, message):
        row = {
            'id': message.str(1),
            'time': message.int(2),
            'sender': self.qid(message.messages(3)[0]) if message.has(3) else ('', ''),
            'client': message.str(4),
            'conversation': self.qid(message.messages(5)[0]) if message.has(5) else ('', ''),
            'edited': message.int(10),
            'type': '',
        }
        if message.has(6):
            text = self.msg(message.messages(6)[0], 'Text')
            row.update(type='Text', text=text.str(1), quoted=text.str(3))
            mentions = []
            for buf in text.messages(2):
                mention = self.msg(buf, 'Mention')
                mentions.append(self.qid(mention.messages(3)[0]) if mention.has(3) else ('', ''))
            row['mentions'] = mentions
            row['everyone'] = len(text.messages(4))
        elif message.has(7):
            asset = self.msg(message.messages(7)[0], 'Asset')
            row.update(type='Asset', asset=_asset(self, asset))
        elif message.has(8):
            location = self.msg(message.messages(8)[0], 'Location')
            row.update(type='Location', longitude=location.float(1), latitude=location.float(2),
                       place=location.str(3), zoom=location.int(4))
        return row

    def user_label(self, key):
        if self.account and key == self.account:
            return LOCAL_USER
        name, handle = self.users.get(key, ('', ''))
        if name and handle:
            return f'{name} (@{handle})'
        return name or (f'@{handle}' if handle else _qid_text(key))

    def conversation_label(self, key, senders):
        name = (self.conversations.get(key) or ('', None, None))[0].strip()
        if name:
            return name
        others = sorted({self.user_label(s) for s in senders if s != self.account})
        return 'Unnamed: ' + (', '.join(others) if others else _qid_text(key))


def _asset(backup, asset):
    meta = {}
    for number, kind in ((10, 'image'), (11, 'video'), (12, 'audio'), (13, 'generic')):
        if asset.has(number):
            fields = backup.msg(asset.messages(number)[0], 'Meta')
            meta = {'kind': kind, 'fields': fields}
            break
    width = height = duration = ''
    if meta.get('kind') in ('image', 'video'):
        width, height = meta['fields'].int(1), meta['fields'].int(2)
        if meta['kind'] == 'video':
            duration = meta['fields'].int(3)
    elif meta.get('kind') == 'audio':
        duration = meta['fields'].int(1)
    encryption = asset.int(9)
    return {
        'mime': asset.str(1), 'size': asset.int(2), 'name': asset.str(3),
        'otr_key': asset.bytes(4).hex(), 'sha256': asset.bytes(5).hex(),
        'asset_id': asset.str(6), 'token': asset.str(7), 'domain': asset.str(8),
        'encryption': {0: 'AES-CBC', 1: 'AES-GCM'}.get(encryption, '' if encryption is None else str(encryption)),
        'meta': meta.get('kind', '').capitalize(),
        'width': '' if width is None else width, 'height': '' if height is None else height,
        'duration': '' if duration is None else duration,
    }


def _page_sort_key(name):
    base = os.path.basename(name)
    match = re.match(r'^(.*?)_(\d+)\.binpb$', base, re.IGNORECASE)
    return (match.group(1), int(match.group(2))) if match else (base, -1)


def _qid_text(key):
    value, domain = key
    return f'{value}@{domain}' if domain else value


def _ts(value):
    return convert_unix_ts_to_utc(value) if value else ''


def _read_header(path):
    try:
        with open(path, 'rb') as handle:
            data = handle.read(HEADER_SIZE)
    except OSError as ex:
        logfunc(f'Wire Backup: {path} could not be read: {ex}')
        return None
    if len(data) < 64 or data[:4] != HEADER_MAGIC:
        return None
    return {
        'version': struct.unpack('>H', data[5:7])[0],
        'salt': data[7:23].hex(),
        'hashed_user_id': data[23:55].hex(),
        'ops_limit': struct.unpack('>I', data[55:59])[0],
        'mem_limit': struct.unpack('>I', data[59:63])[0],
        'encrypted': data[63] != 0,
    }


_CACHE = {}


def _load_backups(files_found):
    backups = []
    for path in sorted(set(str(f) for f in files_found)):
        if not path.lower().endswith('.wbu') or not os.path.isfile(path):
            continue
        try:
            stat = os.stat(path)
        except OSError:
            continue
        cache_key = (path, stat.st_size, stat.st_mtime_ns)
        if cache_key in _CACHE:
            backups.append(_CACHE[cache_key])
            continue
        header = _read_header(path)
        if header is None:
            logfunc(f'Wire Backup: {os.path.basename(path)} has no WBUX header and is not read')
            continue
        backup = _Backup(path)
        backup.header = header
        backup.encrypted = header['encrypted']
        if not backup.encrypted:
            try:
                backup.load_pages()
            except (zipfile.BadZipFile, OSError) as ex:
                backup.error = str(ex)
                logfunc(f'Wire Backup: the ZIP of {os.path.basename(path)} could not be opened: {ex}')
            held = {(row['conversation'], row['id'].lower()) for row in backup.messages}
            orphaned = sum(1 for key in backup.reactions if key not in held)
            if orphaned:
                logfunc(f'Wire Backup: {os.path.basename(path)}: {orphaned} reaction record(s) refer to a '
                        'message the backup does not hold and are not reported')
            for kind, counts in backup.unknown.items():
                if counts:
                    logfunc(f'Wire Backup: {os.path.basename(path)}: fields not in the schema skipped in {kind}: '
                            + ', '.join(f'{n} ({c}x)' for n, c in sorted(counts.items())))
        else:
            logfunc(f'Wire Backup: {os.path.basename(path)} is encrypted and is not opened')
        _CACHE[cache_key] = backup
        backups.append(backup)
    return backups


def _senders_by_conversation(backup):
    senders = {}
    for row in backup.messages:
        senders.setdefault(row['conversation'], set()).add(row['sender'])
    return senders


@artifact_processor
def wireBackupMessages(context):
    data_list = []
    sources = []
    readable = [b for b in _load_backups(context.get_files_found()) if not b.encrypted and b.pages]
    for backup in readable:
        sources.append(backup.path)
        source_file = context.get_relative_path(backup.path)
        # With more than one backup the label names the backup too, so the same chat from two
        # backups can be told apart in LAVA's conversation list.
        label_suffix = f' [{source_file}]' if len(readable) > 1 else ''
        senders = _senders_by_conversation(backup)
        texts = {row['id'].lower(): row for row in backup.messages}
        for row in backup.messages:
            conversation = row['conversation']
            message = ''
            latitude = longitude = place = ''
            asset_name = asset_mime = ''
            if row['type'] == 'Text':
                message = row['text']
            elif row['type'] == 'Asset':
                asset = row['asset']
                asset_name, asset_mime = asset['name'], asset['mime']
                message = f"[Asset: {asset_name or asset_mime or asset['asset_id']}]"
            elif row['type'] == 'Location':
                latitude = '' if row['latitude'] is None else row['latitude']
                longitude = '' if row['longitude'] is None else row['longitude']
                place = row['place']
                message = place or f'[Location: {latitude}, {longitude}]'

            quoted_id = row.get('quoted', '')
            quoted = ''
            if quoted_id:
                target = texts.get(quoted_id.lower())
                if target:
                    quoted = target.get('text') if target['type'] == 'Text' else f"[{target['type']}]"
            mentions = [backup.user_label(m) for m in row.get('mentions', [])]
            if row.get('everyone'):
                mentions.append('everyone')
            reactions = []
            for emoji, users in backup.reactions.get((conversation, row['id'].lower()), []):
                reactions.append(f"{emoji} {', '.join(backup.user_label(u) for u in users)}".strip())

            direction = ''
            if backup.account:
                direction = 'Outgoing' if row['sender'] == backup.account else 'Incoming'
            data_list.append((
                _ts(row['time']), _ts(row['edited']), direction, backup.user_label(row['sender']),
                backup.conversation_label(conversation, senders.get(conversation, ())) + label_suffix, message,
                row['type'], quoted, quoted_id, '\n'.join(mentions), '\n'.join(reactions),
                asset_name, asset_mime, latitude, longitude, place,
                _qid_text(conversation), _qid_text(row['sender']), row['client'], row['id'],
                f'{source_file}#{_qid_text(conversation)}', source_file,
            ))

    data_headers = (
        ('Sent At', 'datetime'), ('Last Edited At', 'datetime'), 'Direction', 'Sender', 'Conversation', 'Message',
        'Message Type', 'Quoted Message', 'Quoted Message ID', 'Mentions', 'Reactions',
        'Asset Name', 'Asset MIME Type', ('Latitude', 'latitude'), ('Longitude', 'longitude'), 'Location Name',
        'Conversation ID', 'Sender User ID', 'Sender Client ID (as stored)', 'Message ID',
        'Conversation Key', 'Source File',
    )
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def wireBackupAssets(context):
    data_list = []
    sources = []
    for backup in _load_backups(context.get_files_found()):
        if backup.encrypted or not backup.pages:
            continue
        sources.append(backup.path)
        source_file = context.get_relative_path(backup.path)
        senders = _senders_by_conversation(backup)
        for row in backup.messages:
            if row['type'] != 'Asset':
                continue
            asset = row['asset']
            conversation = row['conversation']
            data_list.append((
                _ts(row['time']), backup.user_label(row['sender']),
                backup.conversation_label(conversation, senders.get(conversation, ())),
                asset['name'], asset['mime'], asset['size'], asset['meta'],
                asset['width'], asset['height'], asset['duration'],
                asset['asset_id'], asset['token'], asset['domain'], asset['encryption'],
                asset['otr_key'], asset['sha256'],
                _qid_text(conversation), row['id'], source_file,
            ))

    data_headers = (
        ('Sent At', 'datetime'), 'Sender', 'Conversation', 'File Name', 'MIME Type', ('Size (bytes)', 'number'),
        'Metadata Type', 'Width', 'Height', 'Duration (ms)', 'Asset ID', 'Asset Token', 'Asset Domain',
        'Encryption', ('OTR Key', 'hash'), ('SHA-256 (encrypted file)', 'hash'),
        'Conversation ID', 'Message ID', 'Source File',
    )
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def wireBackupConversations(context):
    data_list = []
    sources = []
    for backup in _load_backups(context.get_files_found()):
        if backup.encrypted or not backup.pages:
            continue
        sources.append(backup.path)
        source_file = context.get_relative_path(backup.path)
        senders = _senders_by_conversation(backup)
        spans = {}
        for row in backup.messages:
            spans.setdefault(row['conversation'], []).append(row['time'])
        keys = list(backup.conversation_order)
        keys += sorted(k for k in spans if k not in backup.conversations)
        for key in keys:
            name, modified, read = backup.conversations.get(key, ('', None, None))
            times = [t for t in spans.get(key, []) if t]
            data_list.append((
                _ts(modified), _ts(read),
                _ts(min(times)) if times else '', _ts(max(times)) if times else '', len(spans.get(key, [])),
                name, backup.conversation_label(key, senders.get(key, ())),
                '\n'.join(sorted(backup.user_label(s) for s in senders.get(key, ()))),
                'Yes' if key in backup.conversations else 'No (only in messages)',
                _qid_text(key), source_file,
            ))

    data_headers = (
        ('Last Modified At', 'datetime'), ('Last Read At', 'datetime'),
        ('First Message', 'datetime'), ('Last Message', 'datetime'), ('Messages', 'number'),
        'Name', 'Conversation', 'Participants Seen', 'Listed in Conversations', 'Conversation ID', 'Source File',
    )
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def wireBackupUsers(context):
    data_list = []
    sources = []
    for backup in _load_backups(context.get_files_found()):
        if backup.encrypted or not backup.pages:
            continue
        sources.append(backup.path)
        source_file = context.get_relative_path(backup.path)
        sent = {}
        for row in backup.messages:
            sent[row['sender']] = sent.get(row['sender'], 0) + 1
        for key, (name, handle) in backup.users.items():
            data_list.append((
                name, handle, sent.get(key, 0), 'Yes' if key == backup.account else '',
                _qid_text(key), source_file,
            ))

    data_headers = (
        'Name', 'Handle', ('Messages Sent', 'number'), 'Is Account', 'User ID', 'Source File',
    )
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def wireBackupInfo(context):
    data_list = []
    sources = []
    for backup in _load_backups(context.get_files_found()):
        sources.append(backup.path)
        header = backup.header
        file_name = os.path.basename(backup.path)
        match = FILE_NAME_DATE.match(file_name)
        data_list.append((
            _ts(backup.created), match.group(1) if match else '', 'Yes' if backup.encrypted else 'No',
            _qid_text(backup.account) if backup.account else '',
            '' if backup.encrypted else backup.pages,
            '' if backup.encrypted else len(backup.conversations),
            '' if backup.encrypted else len(backup.messages),
            '' if backup.encrypted else len(backup.users),
            '' if backup.encrypted else len(backup.reactions),
            header['version'], header['ops_limit'], header['mem_limit'], header['salt'], header['hashed_user_id'],
            backup.error, context.get_relative_path(backup.path),
        ))

    data_headers = (
        ('Created At', 'datetime'), 'Created At (from Name)', 'Encrypted', 'Account User ID',
        ('Pages', 'number'), ('Conversations', 'number'), ('Messages', 'number'), ('Users', 'number'),
        ('Reactions', 'number'), 'Header Version', 'Argon2 Operations Limit', 'Argon2 Memory Limit (bytes)',
        ('Salt', 'hash'), ('Hashed User ID', 'hash'), 'Read Error', 'Source File',
    )
    return data_headers, data_list, '\n'.join(sources)
