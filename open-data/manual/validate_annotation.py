#!/usr/bin/env python3
"""Validate guide-v0.1 structure. Does not certify semantics or change review status.

Usage: python3 validate_annotation.py annotation-example.json
Requires only the Python standard library; reads input without modifying it.
"""
import json
import math
import sys

ACTIONS = {'reach_grasp', 'place', 'handover', 'hold', 'fold', 'wipe', 'tilt', 'pour', 'open', 'close', 'align_insert', 'press', 'reveal'}
LEVELS = {'coarse': 0, 'medium': 1, 'fine': 2}
OUTCOMES = {'completed', 'not_completed', 'partial', 'unknown', 'not_applicable'}
SOURCES = {'imported', 'model_assisted', 'manual', 'human_corrected'}
STATUSES = {'draft', 'review_required', 'reviewed'}
ACTORS = {'left', 'right', 'both', 'none', 'unknown'}
VISIBILITIES = {'visible', 'partial', 'occluded', 'unknown'}
ROOT_FIELDS = {'annotation_version', 'sample_id', 'fps', 'frame_count', 'frame_offset', 'frame_index_base', 'end_frame_inclusive', 'objects', 'segments'}
SEGMENT_FIELDS = {'id', 'level', 'parent_id', 'start_frame', 'end_frame', 'instruction', 'actor', 'action', 'object_id', 'target_id', 'visibility', 'outcome', 'outcome_evidence', 'boundary_uncertainty', 'source', 'review_status', 'notes'}

def validate(document):
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
        return bool(condition)
    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())
    if not check(isinstance(document, dict), 'document must be an object'):
        return errors
    check(set(document) == ROOT_FIELDS, 'document fields differ from guide-v0.1')
    check(document.get('annotation_version') == 'annotation-guide-v0.1', 'unsupported annotation_version')
    check(nonempty(document.get('sample_id')), 'sample_id must be a nonempty string')
    fps = document.get('fps')
    check(type(fps) in (int, float) and math.isfinite(fps) and fps > 0, 'fps must be finite and positive')
    count = document.get('frame_count')
    valid_count = check(type(count) is int and count > 0, 'frame_count must be a positive integer')
    offset = document.get('frame_offset')
    check(type(offset) is int and offset >= 0, 'frame_offset must be a nonnegative integer')
    check(type(document.get('frame_index_base')) is int and document['frame_index_base'] == 0, 'frame_index_base must be 0')
    check(document.get('end_frame_inclusive') is True, 'end_frame_inclusive must be true')
    objects = document.get('objects')
    if not check(isinstance(objects, list) and bool(objects), 'objects must be a nonempty list'):
        objects = []
    object_ids = set()
    for index, item in enumerate(objects):
        if not check(isinstance(item, dict), f'object {index} must be an object'):
            continue
        check(set(item) == {'id', 'description'}, f'object {index}: unexpected fields')
        if check(nonempty(item.get('id')), f'object {index}: missing id'):
            check(item['id'] not in object_ids, f'object {index}: duplicate id')
            object_ids.add(item['id'])
        check(nonempty(item.get('description')), f'object {index}: missing description')
    segments = document.get('segments')
    if not check(isinstance(segments, list) and bool(segments), 'segments must be a nonempty list'):
        segments = []
    by_id = {}
    bounds = {}
    for index, segment in enumerate(segments):
        prefix = f'segment {index}'
        if not check(isinstance(segment, dict), prefix + ' must be an object'):
            continue
        check(set(segment) == SEGMENT_FIELDS, prefix + ': fields differ from guide-v0.1')
        sid = segment.get('id')
        if check(nonempty(sid), prefix + ': missing id'):
            check(sid not in by_id, prefix + ': duplicate id')
            by_id[sid] = segment
        level = segment.get('level')
        check(isinstance(level, str) and level in LEVELS, prefix + ': invalid level')
        start, end = segment.get('start_frame'), segment.get('end_frame')
        if check(valid_count and type(start) is int and type(end) is int and 0 <= start <= end < count, prefix + ': invalid inclusive frame range') and isinstance(sid, str):
            bounds[sid] = (start, end)
        check(nonempty(segment.get('instruction')), prefix + ': missing instruction')
        for field, options in [('actor', ACTORS), ('visibility', VISIBILITIES), ('outcome', OUTCOMES), ('source', SOURCES), ('review_status', STATUSES)]:
            value = segment.get(field)
            check(isinstance(value, str) and value in options, prefix + ': invalid ' + field)
        action = segment.get('action')
        check((action is None and level in ('coarse', 'medium')) or (isinstance(action, str) and action in ACTIONS), prefix + ': invalid action')
        notes = segment.get('notes')
        check(isinstance(notes, str), prefix + ': notes must be a string')
        for field in ('object_id', 'target_id'):
            value = segment.get(field)
            check(value is None or (isinstance(value, str) and value in object_ids), prefix + ': unbound ' + field)
        if segment.get('object_id') is None or segment.get('actor') == 'unknown' or segment.get('visibility') != 'visible':
            check(nonempty(notes), prefix + ': missing explanation of uncertain identity/visibility')
        evidence = segment.get('outcome_evidence')
        check(isinstance(evidence, str), prefix + ': outcome_evidence must be a string')
        if isinstance(segment.get('outcome'), str) and segment['outcome'] in {'completed', 'not_completed', 'partial'}:
            check(nonempty(evidence), prefix + ': outcome requires evidence')
        uncertainty = segment.get('boundary_uncertainty')
        if uncertainty is not None:
            fields = {'start_min', 'start_max', 'end_min', 'end_max'}
            valid_uncertainty = isinstance(uncertainty, dict) and set(uncertainty) == fields and all(type(uncertainty[k]) is int for k in fields)
            if check(valid_uncertainty, prefix + ': malformed boundary_uncertainty'):
                check(valid_count and type(start) is int and type(end) is int and 0 <= uncertainty['start_min'] <= start <= uncertainty['start_max'] < count and 0 <= uncertainty['end_min'] <= end <= uncertainty['end_max'] < count and uncertainty['start_min'] <= uncertainty['end_max'], prefix + ': invalid uncertainty range')
            check(segment.get('review_status') != 'reviewed', prefix + ': unresolved boundaries cannot be reviewed')
            check(nonempty(notes), prefix + ': boundary uncertainty needs notes')
    for sid, segment in by_id.items():
        level = segment.get('level')
        parent_id = segment.get('parent_id')
        if level == 'coarse':
            check(parent_id is None, sid + ': coarse parent must be null')
            continue
        if not check(isinstance(parent_id, str) and parent_id in by_id, sid + ': missing parent'):
            continue
        parent = by_id[parent_id]
        check(isinstance(level, str) and level in LEVELS and isinstance(parent.get('level'), str) and parent['level'] in LEVELS and LEVELS[level] == LEVELS[parent['level']] + 1, sid + ': invalid parent level')
        if sid in bounds and parent_id in bounds:
            start, end = bounds[sid]
            check(bounds[parent_id][0] <= start <= end <= bounds[parent_id][1], sid + ': outside parent interval')
    return errors

def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    try:
        with open(sys.argv[1], encoding='utf-8') as stream:
            document = json.load(stream)
        errors = validate(document)
    except (OSError, ValueError) as error:
        print(json.dumps({'structure_valid': False, 'error': str(error)}, ensure_ascii=False))
        return 2
    print(json.dumps({'structure_valid': not errors, 'semantic_quality': 'not verified by this validator', 'review_status_changed': False, 'errors': errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(main())
