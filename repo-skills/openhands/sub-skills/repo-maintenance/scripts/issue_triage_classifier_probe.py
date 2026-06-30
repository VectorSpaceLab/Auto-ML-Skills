#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

BROAD_TERMS = {
    'architecture',
    'architectural',
    'design',
    'epic',
    'framework',
    'infra',
    'infrastructure',
    'migration',
    'migrations',
    'overhaul',
    'platform',
    'project',
    'refactor',
    'roadmap',
    'security',
    'tracking',
    'umbrella',
}
CLEAR_SMALL_TERMS = {
    'copy',
    'docs',
    'documentation',
    'example',
    'label',
    'link',
    'readme',
    'text',
    'tooltip',
    'translation',
    'typo',
    'wording',
}
CONFIG_TERMS = {'config', 'configuration', 'setting', 'settings'}
REPRO_TERMS = {
    'actual',
    'expected',
    'reproduce',
    'reproduction',
    'steps',
    'traceback',
}
COMPLEX_AREA_TERMS = {
    'auth',
    'billing',
    'database',
    'enterprise',
    'keycloak',
    'migration',
    'oauth',
    'permissions',
    'sandbox',
    'secret',
    'secrets',
    'stripe',
}
DUPLICATE_TERMS = {
    'duplicate',
    'duplicates',
    'same as',
    'similar to',
    'overlap',
    'overlapping',
    'related to',
}
GOOD_FIRST_BLOCKING_LABELS = {
    'duplicate',
    'duplicate-candidate',
    'security',
    'enterprise',
    'needs-design',
    'needs discussion',
    'needs-discussion',
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            'Offline deterministic OpenHands issue triage probe. Reads one issue '
            'JSON object from a file path or stdin and emits conservative '
            'classification hints without GitHub, OpenHands, network calls, or state changes.'
        )
    )
    parser.add_argument(
        'issue_json',
        help=(
            'Path to a JSON issue object, or - for stdin. Expected fields: title, body, labels. '
            'Optional fields: state, locked, pull_request.'
        ),
    )
    parser.add_argument(
        '--pretty', action='store_true', help='Pretty-print JSON output with indentation.'
    )
    return parser.parse_args()


def as_text(value: Any) -> str:
    return str(value or '').strip()


def normalize_labels(raw_labels: Any) -> list[str]:
    if not isinstance(raw_labels, list):
        return []
    labels: list[str] = []
    for raw_label in raw_labels:
        if isinstance(raw_label, str):
            label = raw_label
        elif isinstance(raw_label, dict):
            label = as_text(raw_label.get('name'))
        else:
            label = ''
        if label:
            labels.append(label)
    return sorted(set(labels), key=lambda item: (item.lower(), item))


def tokenize(text: str) -> set[str]:
    return set(re.findall(r'[a-z0-9][a-z0-9_-]*', text.lower()))


def contains_phrase(text: str, phrases: set[str]) -> list[str]:
    lowered = text.lower()
    return sorted(phrase for phrase in phrases if phrase in lowered)


def classify(issue: dict[str, Any]) -> dict[str, Any]:
    title = as_text(issue.get('title'))
    body = as_text(issue.get('body'))
    labels = normalize_labels(issue.get('labels'))
    label_keys = {label.lower() for label in labels}
    text = f'{title}\n{body}'
    tokens = tokenize(text)

    criteria_met: list[str] = []
    disqualifiers: list[str] = []
    duplicate_hints: list[str] = []

    if issue.get('pull_request'):
        disqualifiers.append('pull request, not an issue')
    if as_text(issue.get('state')).lower() not in {'', 'open'}:
        disqualifiers.append('issue is not open')
    if issue.get('locked') is True:
        disqualifiers.append('issue is locked')

    blocking_labels = sorted(label_keys & GOOD_FIRST_BLOCKING_LABELS)
    if blocking_labels:
        disqualifiers.append('blocking label: ' + ', '.join(blocking_labels[:3]))

    broad_matches = sorted(tokens & BROAD_TERMS)
    if broad_matches:
        disqualifiers.append('broad or high-risk scope: ' + ', '.join(broad_matches[:4]))

    complex_matches = sorted(tokens & COMPLEX_AREA_TERMS)
    if complex_matches:
        disqualifiers.append('likely needs specialist context: ' + ', '.join(complex_matches[:4]))

    if len(body) < 40:
        disqualifiers.append('body is too short for confident newcomer labeling')
    elif tokens & REPRO_TERMS:
        criteria_met.append('includes reproduction or expected-behavior details')

    small_matches = sorted((tokens | label_keys) & CLEAR_SMALL_TERMS)
    if small_matches:
        criteria_met.append('appears narrow: ' + ', '.join(small_matches[:4]))

    if tokens & CONFIG_TERMS and not complex_matches:
        criteria_met.append('configuration or settings area is identifiable')

    duplicate_phrase_matches = contains_phrase(text, DUPLICATE_TERMS)
    if duplicate_phrase_matches:
        duplicate_hints.extend(duplicate_phrase_matches[:4])
    if 'duplicate-candidate' in label_keys or 'duplicate' in label_keys:
        duplicate_hints.append('duplicate-related label present')

    confidence = 'low'
    should_apply_label = False
    if not disqualifiers and len(criteria_met) >= 2:
        confidence = 'high'
        should_apply_label = True
    elif criteria_met and len(disqualifiers) <= 1:
        confidence = 'medium'

    duplicate_veto = bool(duplicate_hints)
    if duplicate_veto:
        should_apply_label = False
        if 'possible duplicate or overlapping-scope hint' not in disqualifiers:
            disqualifiers.append('possible duplicate or overlapping-scope hint')

    return {
        'should_apply_good_first_issue_hint': should_apply_label,
        'confidence': confidence,
        'duplicate_veto_hint': duplicate_veto,
        'criteria_met': criteria_met[:5],
        'disqualifiers': disqualifiers[:5],
        'duplicate_hints': duplicate_hints[:5],
        'normalized_labels': labels,
        'summary': build_summary(should_apply_label, confidence, duplicate_veto, criteria_met, disqualifiers),
    }


def build_summary(
    should_apply_label: bool,
    confidence: str,
    duplicate_veto: bool,
    criteria_met: list[str],
    disqualifiers: list[str],
) -> str:
    if duplicate_veto:
        return 'Do not auto-label before duplicate or overlap review.'
    if should_apply_label:
        return 'Looks like a narrow, clear newcomer candidate by offline heuristics.'
    if disqualifiers:
        return 'Do not auto-label: ' + disqualifiers[0]
    if criteria_met:
        return f'Potentially suitable, but confidence is {confidence}; require maintainer review.'
    return 'Insufficient evidence for newcomer auto-labeling.'


def load_issue(path: str) -> dict[str, Any]:
    raw = sys.stdin.read() if path == '-' else open(path, encoding='utf-8').read()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f'Invalid JSON input: {exc}') from exc
    if not isinstance(payload, dict):
        raise SystemExit('Issue JSON must be an object.')
    return payload


def main() -> int:
    args = parse_args()
    issue = load_issue(args.issue_json)
    result = classify(issue)
    json.dump(result, sys.stdout, indent=2 if args.pretty else None, sort_keys=True)
    sys.stdout.write('\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
