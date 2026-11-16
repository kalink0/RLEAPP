__artifacts_v2__ = {
    "threemaAndroidBackupMessages": {
        "name": "Threema Android Backup - Messages",
        "description": "Messages of one-to-one and group chats from the CSV files of an unpacked Threema for Android "
                       "data backup, with the attached media file rendered inline where the backup holds it.",
        "author": "@kalink0",
        "creation_date": "2026-11-16",
        "last_update_date": "2026-11-16",
        "requirements": "none",
        "category": "Threema Android Backup",
        "notes": "Reads an unpacked Threema for Android data backup; the password-encrypted backup ZIP is not "
                 "opened here. A folder counts as a backup only when its message CSVs carry Threema's header "
                 "(apiid, uid, isoutbox, posted_at, type, body). One row per row of message_<Threema ID>.csv and "
                 "group_message_<group ID>-<creator ID>.csv; Source File is what LAVA's conversation view groups "
                 "on, so two backups stay apart. The timestamp columns are the CSV columns of the same name, Unix "
                 "milliseconds, shown in UTC. Direction is isoutbox, the message model's outbox flag "
                 "(https://github.com/threema-ch/threema-android/blob/097cc6b85698f02031a00ee276786ff47140a5b6/app/src/main/java/ch/threema/app/backuprestore/csv/BackupService.java#L692). "
                 "In the Threema source at that commit every writer of the flag sets it for a message sent by the "
                 "account, also from a linked device, and clears it for a received one; for a call status it is "
                 "the direction of the call. Other status messages are created with 0, so their Direction and "
                 "Sender are blank. The Sender of an outgoing message is 'Local User', as the backup does not name "
                 "the account in plain text. FILE bodies are JSON lists: item 2 is MIME Type, item 4 File Name, "
                 "item 7 the caption. In the tested backup backslashes inside these bodies were doubled, which is "
                 "undone before decoding. Media is message_media_<uid>; in the tested backup only FILE messages "
                 "had one. Quoted Message resolves quoted_message_apiid within the same CSV. Edited At, Deleted "
                 "At, Starred (bit 1 of display_tags) and Group Message States (as stored) come from columns the "
                 "current Threema source writes but the tested backup lacked, so they were blank on every row of "
                 "it and are checked only on a synthetic fixture. Not reported: isqueued (unused in the current "
                 "source), isread (set whenever isoutbox is), issaved, and the poll and distribution list files "
                 "(empty in the tested backup). Tested on one Threema for Android backup.",
        "paths": ('*/message_*.csv', '*/group_message_*.csv', '*/contacts.csv', '*/groups.csv',
                  '*/message_media_*'),
        "output_types": "standard",
        "artifact_icon": "message-square",
        "data_views": {
            "conversation": {
                "conversationDiscriminatorColumn": "Source File",
                "conversationLabelColumn": "Conversation",
                "textColumn": "Message",
                "directionColumn": "Direction",
                "directionSentValue": "Outgoing",
                "timeColumn": "Posted At",
                "senderColumn": "Sender",
                "mediaColumn": "Media",
            }
        },
    },
    "threemaAndroidBackupMedia": {
        "name": "Threema Android Backup - Media",
        "description": "Media files and thumbnails of an unpacked Threema for Android data backup, each with the message "
                       "it belongs to.",
        "author": "@kalink0",
        "creation_date": "2026-11-16",
        "last_update_date": "2026-11-16",
        "requirements": "none",
        "category": "Threema Android Backup",
        "notes": "One row per message_media_<uid> and message_thumbnail_<uid> file in a folder that is read as a "
                 "Threema for Android backup (see the Messages artifact). The message columns come from the message whose uid "
                 "is in the file name; a file whose uid no message of the backup carries is listed with those "
                 "columns blank. Content Type is read from the file's bytes; an ISO-BMFF file whose only track "
                 "handler is a sound track is typed audio/mp4, as the voice messages of the tested backup were "
                 "AAC in such a container. File Role is Media for message_media_ and Thumbnail for "
                 "message_thumbnail_ files. File Name and MIME Type (as stored) are items 4 and 2 of the "
                 "message's JSON body. Every file of the tested backup belonged to a FILE message.",
        "paths": ('*/message_*.csv', '*/group_message_*.csv', '*/contacts.csv', '*/groups.csv',
                  '*/message_media_*', '*/message_thumbnail_*'),
        "output_types": "standard",
        "artifact_icon": "image",
    },
    "threemaAndroidBackupContacts": {
        "name": "Threema Android Backup - Contacts",
        "description": "Contacts of an unpacked Threema for Android data backup with their pictures and the span of the "
                       "messages exchanged with them.",
        "author": "@kalink0",
        "creation_date": "2026-11-16",
        "last_update_date": "2026-11-16",
        "requirements": "none",
        "category": "Threema Android Backup",
        "notes": "One row per row of contacts.csv of a Threema for Android backup (see the Messages artifact). "
                 "Verification Level, Hidden and Archived are reported as stored. Profile Picture and Avatar are "
                 "the contact_profile_pic_<ID> and contact_avatar_<ID> files, named after the files; who set which "
                 "is not established. First Message, Last Message and Messages cover the contact's one-to-one chat "
                 "only, and are blank or 0 when its chat file holds no message, as for most contacts of the tested "
                 "backup. Hidden held 0 on every row of the tested backup.",
        "paths": ('*/message_*.csv', '*/group_message_*.csv', '*/contacts.csv',
                  '*/contact_profile_pic_*', '*/contact_avatar_*'),
        "output_types": "standard",
        "artifact_icon": "users",
    },
    "threemaAndroidBackupGroups": {
        "name": "Threema Android Backup - Groups",
        "description": "Groups of an unpacked Threema for Android data backup with creator, members and the span of the "
                       "group's messages.",
        "author": "@kalink0",
        "creation_date": "2026-11-16",
        "last_update_date": "2026-11-16",
        "requirements": "none",
        "category": "Threema Android Backup",
        "notes": "One row per row of groups.csv in a folder that is read as a Threema for Android backup. Created At is "
                 "created_at as stored, in UTC. Members is the semicolon-separated members column, one member "
                 "per line, named from contacts.csv where the Threema ID is there; whether the list includes "
                 "the account itself is not established. Deleted and Archived are reported as stored. First "
                 "Message, Last Message and Messages come from the group_message_<group ID>-<creator ID>.csv "
                 "file matching the group's id and creator.",
        "paths": ('*/message_*.csv', '*/group_message_*.csv', '*/contacts.csv', '*/groups.csv'),
        "output_types": "standard",
        "artifact_icon": "users",
    },
    "threemaAndroidBackupAccount": {
        "name": "Threema Android Backup - Account",
        "description": "The backup's own Threema ID and creation time as given by the backup's file name, and "
                       "the stored settings, of an unpacked Threema for Android data backup.",
        "author": "@kalink0",
        "creation_date": "2026-11-16",
        "last_update_date": "2026-11-16",
        "requirements": "none",
        "category": "Threema Android Backup",
        "notes": "One row per Threema for Android backup (see the Messages artifact). The tested backups were "
                 "named threema-backup_<Threema ID>_<Unix milliseconds>_1.zip; Threema ID (from Name) and Created "
                 "(from Name) are read from the folder's name when it has that form, and are blank otherwise. On "
                 "the tested backup that ID matched the one inside the identity file, checked by decrypting it "
                 "with the backup's password outside this module. The identity file holds the account's ID and "
                 "private key, password-protected; only its presence is reported. Settings lists the rows of the "
                 "settings file as stored.",
        "paths": ('*/message_*.csv', '*/group_message_*.csv', '*/identity', '*/settings'),
        "output_types": "standard",
        "artifact_icon": "user",
    },
}

import csv
import json
import os
import re
import sys

from scripts.filetype import guess_mime
from scripts.ilapfuncs import artifact_processor, check_in_media, convert_unix_ts_to_utc, logfunc
from scripts.meta_records import media_type_hint

# Source references below are to threema-android at commit 097cc6b85698f02031a00ee276786ff47140a5b6
# (https://github.com/threema-ch/threema-android/tree/097cc6b85698f02031a00ee276786ff47140a5b6), paths
# relative to app/src/main/java/ch/threema/. The backup CSVs are written by
# app/backuprestore/csv/BackupService.java: one-to-one columns L570-L600, rows L688-L709 (a message
# is written only with an apiid or as a VOIP_STATUS, L688); group columns L775-L805, rows L874-L903.
# Older backups lack display_tags, edited_at, deleted_at and g_msg_states; every column added since
# is read when present and left blank when absent.

MESSAGE_HEADER ={'apiid', 'uid', 'isoutbox', 'posted_at', 'type', 'body'}
CONTACT_HEADER = {'identity', 'publickey', 'firstname', 'lastname'}
GROUP_HEADER = {'id', 'creator', 'groupname', 'members'}
ONE_TO_ONE_RE = re.compile(r'^message_(.+)\.csv$')
GROUP_RE = re.compile(r'^group_message_(.+)-([^-]+)\.csv$')
BACKUP_NAME_RE = re.compile(r'^threema-backup_([A-Z0-9*]{8})_(\d{10,13})(?:_\d+)?(?:\.zip)?$')
LOCAL_USER = 'Local User'
CALL_STATUS_TYPES = {'VOIP_STATUS', 'GROUP_CALL_STATUS'}


def _set_csv_field_limit():
    try:
        csv.field_size_limit(sys.maxsize)
    except OverflowError:
        csv.field_size_limit(2 ** 31 - 1)


def _read_csv(path):
    """Header and rows of one backup CSV, or (None, []) when it cannot be read."""
    _set_csv_field_limit()
    try:
        with open(path, encoding='utf-8-sig', errors='replace', newline='') as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            return set(reader.fieldnames or ()), rows
    except (OSError, csv.Error) as ex:
        logfunc(f'Threema Android backup: could not read {path}: {ex}')
        return None, []


def _ts(value):
    # Threema writes every timestamp as Unix milliseconds (app/utils/CSVRow.java L249-L254).
    value = (value or '').strip()
    if value.isdigit() and int(value) > 0:
        return convert_unix_ts_to_utc(int(value))
    return ''


def _decode_json_body(body):
    """The JSON list stored in a message body, with the CSV writer's doubled backslashes undone."""
    body = (body or '').strip()
    if not body.startswith('['):
        return None
    for candidate in (body.replace('\\\\', '\\'), body):
        try:
            value = json.loads(candidate)
        except ValueError:
            continue
        if isinstance(value, list):
            return value
    logfunc('Threema Android backup: a message body could not be decoded as JSON and is reported as stored')
    return None


def _check_in(path, name):
    """Media reference and content type of a file, typed by its bytes.

    Voice messages are AAC in an ISO-BMFF container holding only a sound track, which a
    signature sniff types as video/mp4; the track handlers type them as audio instead."""
    hint = media_type_hint(path)
    try:
        content_type = hint or guess_mime(path) or ''
    except OSError:
        content_type = ''
    return check_in_media(path, name, force_type=hint), content_type


def _item(values, index):
    if values and len(values) > index and values[index] is not None:
        return values[index]
    return ''


class _Backup:
    """One folder holding the files of an unpacked Threema backup."""

    def __init__(self, root, names):
        self.root = root
        self.files = names            # basename -> path, this folder only
        self.contacts = {}
        self.groups = {}
        self.chats = []               # (path, kind, conversation id, creator id, rows)
        self.uid_index = {}           # uid -> (message row, chat)

    def contact_label(self, identity):
        identity = (identity or '').strip()
        if not identity:
            return ''
        contact = self.contacts.get(identity, {})
        name = f"{(contact.get('firstname') or '').strip()} {(contact.get('lastname') or '').strip()}".strip()
        name = name or (contact.get('nick_name') or '').strip()
        return f'{name} ({identity})' if name else identity

    def group_label(self, group_id, creator):
        name = (self.groups.get((group_id, creator), {}).get('groupname') or '').strip()
        return name or group_id


def _load_backups(files_found):
    """Every folder of files_found that holds Threema message CSVs with Threema's header."""
    folders = {}
    for path in files_found:
        path = str(path)
        if os.path.isfile(path):
            folders.setdefault(os.path.dirname(path), {})[os.path.basename(path)] = path

    backups = []
    for root, names in sorted(folders.items()):
        backup = _Backup(root, names)
        for name in sorted(names):
            one = ONE_TO_ONE_RE.match(name)
            group = GROUP_RE.match(name) if not one else None
            if not one and not group:
                continue
            header, rows = _read_csv(names[name])
            if header is None or not MESSAGE_HEADER <= header:
                continue
            if one:
                backup.chats.append((names[name], 'One-to-one', one.group(1), '', rows))
            else:
                backup.chats.append((names[name], 'Group', group.group(1), group.group(2), rows))
        if not backup.chats:
            continue

        if 'contacts.csv' in names:
            header, rows = _read_csv(names['contacts.csv'])
            if header and CONTACT_HEADER <= header:
                for row in rows:
                    identity = (row.get('identity') or '').strip()
                    if identity:
                        backup.contacts[identity] = row
        if 'groups.csv' in names:
            header, rows = _read_csv(names['groups.csv'])
            if header and GROUP_HEADER <= header:
                for row in rows:
                    key = ((row.get('id') or '').strip(), (row.get('creator') or '').strip())
                    backup.groups[key] = row

        for chat in backup.chats:
            for row in chat[4]:
                uid = (row.get('uid') or '').strip()
                if uid:
                    backup.uid_index[uid] = (row, chat)
        backups.append(backup)
    return backups


def _conversation_label(backup, chat):
    _, kind, conversation_id, creator, _ = chat
    if kind == 'Group':
        return backup.group_label(conversation_id, creator)
    return backup.contact_label(conversation_id)


def _is_status_without_direction(row):
    """A status message whose isoutbox Threema sets to 0 whatever happened; call statuses keep theirs.

    isstatusmessage is MessageType.isStatus (storage/models/MessageModel.kt L75-L76; the status types are
    listed in storage/models/MessageType.kt L30-L39). FORWARD_SECURITY_STATUS and GROUP_STATUS are created
    with outbox false (app/services/MessageServiceImpl.java L375, L399). Backups by older versions also
    flagged TEXT rows as status messages, with no apiid."""
    is_status = (row.get('isstatusmessage') or '').strip() == '1'
    return is_status and (row.get('type') or '').strip() not in CALL_STATUS_TYPES


def _direction(row):
    """'Outgoing' or 'Incoming' from isoutbox, which BackupService.java L692 writes from MessageModel.isOutbox.

    Every writer of that flag was read:
      set   - sending from this device: MessageServiceImpl.java L454 (text), L930 (location), L1194 (poll),
              L4060 (files); from another device of the account: processors/reflectedoutgoingmessage/
              ReflectedOutgoingMessageTask.kt L101; a poll the account created: MessageServiceImpl.java L419
      clear - receiving: MessageServiceImpl.java L1914, L2077, L2110, L2166; processors/incomingcspmessage/
              conversation/IncomingContactFileMessageTask.kt L130, IncomingGroupFileMessageTask.kt L156
      both  - from the message direction: app/libthreema/conversion/MessageStateConverter.kt L171-L177
      call  - the call's direction; missed 0, aborted 1: app/voip/VoipCallStatusMonitor.kt L43-L74
    Apart from loading and restoring, nothing changes it after the message is created."""
    if _is_status_without_direction(row):
        return ''
    value = (row.get('isoutbox') or '').strip()
    return {'1': 'Outgoing', '0': 'Incoming'}.get(value, value)


def _starred(row):
    # display_tags is a bit field; bit 1 is DISPLAY_TAG_STARRED (storage/models/data/DisplayTag.java L20).
    value = (row.get('display_tags') or '').strip()
    if value.isdigit():
        return 'Yes' if int(value) & 1 else ''
    return value


def _sender(backup, chat, row):
    if _is_status_without_direction(row):
        return ''
    if (row.get('isoutbox') or '').strip() == '1':
        return LOCAL_USER
    if chat[1] == 'Group':
        return backup.contact_label(row.get('identity'))
    return backup.contact_label(chat[2])


def _chat_span(rows):
    stamps = [int(r['posted_at']) for r in rows if (r.get('posted_at') or '').strip().isdigit()]
    if not stamps:
        return '', '', len(rows)
    return convert_unix_ts_to_utc(min(stamps)), convert_unix_ts_to_utc(max(stamps)), len(rows)


@artifact_processor
def threemaAndroidBackupMessages(context):
    data_list = []
    sources = []
    for backup in _load_backups(context.get_files_found()):
        for chat in backup.chats:
            path, kind, conversation_id, _, rows = chat
            sources.append(path)
            source_file = context.get_relative_path(path)
            conversation = _conversation_label(backup, chat)
            by_apiid = {(r.get('apiid') or '').strip(): r for r in rows if (r.get('apiid') or '').strip()}
            for row in rows:
                msg_type = (row.get('type') or '').strip()
                body = row.get('body') or ''
                values = _decode_json_body(body) if msg_type != 'TEXT' else None
                file_name = mime = ''
                latitude = longitude = accuracy = address = place = ''
                if msg_type == 'TEXT':
                    message = body
                elif msg_type == 'FILE':
                    file_name = _item(values, 4)
                    mime = _item(values, 2)
                    message = _item(values, 7) or (row.get('caption') or '')
                elif msg_type == 'LOCATION':
                    latitude, longitude, accuracy = _item(values, 0), _item(values, 1), _item(values, 2)
                    address, place = _item(values, 3), _item(values, 4)
                    message = '\n'.join(str(v) for v in (address, place) if v)
                elif msg_type == 'VOIP_STATUS':
                    details = _item(values, 1)
                    message = ''
                    if isinstance(details, dict):
                        message = '; '.join(f'{k} (as stored): {v}' for k, v in sorted(details.items()))
                else:
                    message = row.get('caption') or ''
                if not message:
                    message = f'[{msg_type}]' if msg_type else ''

                uid = (row.get('uid') or '').strip()
                media = ''
                media_path = backup.files.get(f'message_media_{uid}') if uid else None
                if media_path:
                    media = _check_in(media_path, str(file_name or os.path.basename(media_path)))[0]

                quoted_id = (row.get('quoted_message_apiid') or '').strip()
                quoted = ''
                if quoted_id and quoted_id in by_apiid:
                    target = by_apiid[quoted_id]
                    quoted = target.get('body') if (target.get('type') or '') == 'TEXT' else f"[{target.get('type')}]"

                data_list.append((
                    _ts(row.get('posted_at')), _ts(row.get('created_at')), _ts(row.get('modified_at')),
                    _ts(row.get('delivered_at')), _ts(row.get('read_at')),
                    _ts(row.get('edited_at')), _ts(row.get('deleted_at')),
                    _direction(row), _sender(backup, chat, row), conversation, message, media,
                    msg_type, file_name, mime, quoted, quoted_id,
                    (row.get('messagestae') or '').strip(),
                    'Yes' if (row.get('isstatusmessage') or '').strip() == '1' else '',
                    _starred(row), (row.get('g_msg_states') or '').strip(),
                    latitude, longitude, accuracy, address, place,
                    kind, conversation_id,
                    (row.get('identity') or '').strip() if kind == 'Group' else
                    ('' if (row.get('isoutbox') or '').strip() == '1' else conversation_id),
                    (row.get('apiid') or '').strip(), uid, source_file,
                ))

    data_headers = (
        ('Posted At', 'datetime'), ('Created At', 'datetime'), ('Modified At', 'datetime'),
        ('Delivered At', 'datetime'), ('Read At', 'datetime'), ('Edited At', 'datetime'), ('Deleted At', 'datetime'),
        'Direction', 'Sender', 'Conversation', 'Message', ('Media', 'media'),
        'Message Type', 'File Name', 'MIME Type', 'Quoted Message', 'Quoted Message ID',
        'Message State (as stored)', 'Status Message', 'Starred', 'Group Message States (as stored)',
        ('Latitude', 'latitude'), ('Longitude', 'longitude'), 'Location Accuracy (as stored)',
        'Location Address', 'Location Name',
        'Conversation Type', 'Conversation ID', 'Sender Threema ID', 'Message ID (apiid)', 'UID',
        'Source File',
    )
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def threemaAndroidBackupMedia(context):
    data_list = []
    sources = []
    for backup in _load_backups(context.get_files_found()):
        for name, path in sorted(backup.files.items()):
            if name.startswith('message_media_'):
                kind, uid = 'Media', name[len('message_media_'):]
            elif name.startswith('message_thumbnail_'):
                kind, uid = 'Thumbnail', name[len('message_thumbnail_'):]
            else:
                continue
            sources.append(path)
            row, chat = backup.uid_index.get(uid, (None, None))
            posted = direction = sender = conversation = msg_type = file_name = mime = ''
            if row is not None:
                posted = _ts(row.get('posted_at'))
                direction = _direction(row)
                sender = _sender(backup, chat, row)
                conversation = _conversation_label(backup, chat)
                msg_type = (row.get('type') or '').strip()
                if msg_type == 'FILE':
                    values = _decode_json_body(row.get('body'))
                    file_name, mime = _item(values, 4), _item(values, 2)
            media, content_type = _check_in(path, str(file_name or name))
            data_list.append((posted, direction, sender, conversation, media, content_type, kind,
                              file_name, mime, uid, context.get_relative_path(path)))

    data_headers = (
        ('Posted At', 'datetime'), 'Direction', 'Sender', 'Conversation', ('Media', 'media'), 'Content Type',
        'File Role', 'File Name', 'MIME Type (as stored)', 'UID', 'Source File',
    )
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def threemaAndroidBackupContacts(context):
    data_list = []
    sources = []
    for backup in _load_backups(context.get_files_found()):
        if not backup.contacts:
            continue
        sources.append(backup.files['contacts.csv'])
        spans = {chat[2]: _chat_span(chat[4]) for chat in backup.chats if chat[1] == 'One-to-one'}
        for identity, row in backup.contacts.items():
            first, last, count = spans.get(identity, ('', '', 0))
            pictures = []
            for prefix in ('contact_profile_pic_', 'contact_avatar_'):
                path = backup.files.get(prefix + identity)
                pictures.append(check_in_media(path, prefix + identity) if path else '')
            data_list.append((
                identity, (row.get('firstname') or '').strip(), (row.get('lastname') or '').strip(),
                (row.get('nick_name') or '').strip(), first, last, count, pictures[0], pictures[1],
                (row.get('verification') or '').strip(), (row.get('hidden') or '').strip(),
                (row.get('archived') or '').strip(), (row.get('publickey') or '').strip(),
                context.get_relative_path(backup.files['contacts.csv']),
            ))

    data_headers = (
        'Threema ID', 'First Name', 'Last Name', 'Nickname', ('First Message', 'datetime'),
        ('Last Message', 'datetime'), ('Messages', 'number'), ('Profile Picture', 'media'), ('Avatar', 'media'),
        'Verification Level (as stored)', 'Hidden (as stored)', 'Archived (as stored)', ('Public Key', 'hash'),
        'Source File',
    )
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def threemaAndroidBackupGroups(context):
    data_list = []
    sources = []
    for backup in _load_backups(context.get_files_found()):
        if not backup.groups:
            continue
        sources.append(backup.files['groups.csv'])
        spans = {(chat[2], chat[3]): _chat_span(chat[4]) for chat in backup.chats if chat[1] == 'Group'}
        for (group_id, creator), row in backup.groups.items():
            first, last, count = spans.get((group_id, creator), ('', '', 0))
            members = [m.strip() for m in (row.get('members') or '').split(';') if m.strip()]
            data_list.append((
                _ts(row.get('created_at')), first, last, backup.group_label(group_id, creator), group_id,
                backup.contact_label(creator), '\n'.join(backup.contact_label(m) for m in members),
                len(members), count, (row.get('deleted') or '').strip(), (row.get('archived') or '').strip(),
                context.get_relative_path(backup.files['groups.csv']),
            ))

    data_headers = (
        ('Created At', 'datetime'), ('First Message', 'datetime'), ('Last Message', 'datetime'), 'Group Name',
        'Group ID', 'Creator', 'Members', ('Member Count', 'number'), ('Messages', 'number'),
        'Deleted (as stored)', 'Archived (as stored)', 'Source File',
    )
    return data_headers, data_list, '\n'.join(sources)


def _read_settings(path):
    """Each row of the settings file as 'name=value', as stored."""
    _set_csv_field_limit()
    try:
        with open(path, encoding='utf-8-sig', errors='replace', newline='') as handle:
            return ['='.join(row) for row in csv.reader(handle) if row]
    except (OSError, csv.Error) as ex:
        logfunc(f'Threema Android backup: could not read {path}: {ex}')
        return []


@artifact_processor
def threemaAndroidBackupAccount(context):
    data_list = []
    sources = []
    for backup in _load_backups(context.get_files_found()):
        folder = os.path.basename(backup.root)
        match = BACKUP_NAME_RE.match(folder)
        threema_id = created = ''
        if match:
            threema_id = match.group(1)
            created = convert_unix_ts_to_utc(int(match.group(2)))
        settings = []
        if 'settings' in backup.files:
            settings = _read_settings(backup.files['settings'])
            sources.append(backup.files['settings'])
        if 'identity' in backup.files:
            sources.append(backup.files['identity'])
        if not sources or os.path.dirname(sources[-1]) != backup.root:
            sources.append(backup.chats[0][0])
        data_list.append((
            created, threema_id, 'Yes' if 'identity' in backup.files else 'No',
            '\n'.join(settings), folder,
        ))

    data_headers = (
        ('Created (from Name)', 'datetime'), 'Threema ID (from Name)', 'Identity File Present', 'Settings',
        'Backup Folder',
    )
    return data_headers, data_list, '\n'.join(sources)
