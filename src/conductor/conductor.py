#!/usr/bin/env python
# * coding: utf8 *
"""
a description of what this module does.
this file is for testing linting...
"""

import json
from collections import namedtuple

import github

from .checks import (
    ArcGisOnlineChecker, GSheetChecker, MetaTableChecker, MSSqlTableChecker, OpenDataChecker, PGSqlTableChecker
)

try:
    from conductor.connections import DB, GITHUB_TOKEN
except ModuleNotFoundError:
    from conductor.connection_sample import DB, GITHUB_TOKEN


def startup():
    """the method called when invoking `conductor`
    """

    issues = gather_issues(github.Github(GITHUB_TOKEN).get_repo('agrc/porter', lazy=True))

    if len(issues) == 0:
        return

    reports = write_reports(issues)

    grades = grade_reports(reports)

    publish_grades(grades)

    return grades


def gather_issues(porter):
    """finds the issues and delegates them to the checkers
    issues will have metadata for the bot to use to check for items
    <!-- conductor = {"table":"schema.table","when":"2020-07-16T09:00:00.000Z"} -->
    """
    issues = porter.get_issues(state='open')

    conductor_issues = []
    ConductorIssue = namedtuple('ConductorIssue', 'issue introduction')

    for issue in issues:
        labels = [label.name for label in issue.labels]
        introduction = False
        capture = False

        if 'reminder' in labels:
            continue
        if 'scheduled' in labels:
            continue

        if 'introduction' in labels:
            introduction = True
            capture = True
        elif 'deprecation' in labels:
            introduction = False
            capture = True

        if not capture:
            continue

        conductor_issues.append(ConductorIssue(issue, introduction))

    return conductor_issues


def write_reports(conductor_issues):
    """
    checks that the data has been added to the expected areas
    conductor_issues: a named tuple with the issue and a introduction label boolean
    """
    reports = {}

    for issue in conductor_issues:
        Report = namedtuple('Report', 'check issue report grader')
        metadata = extract_metadata_from_issue_body(issue.issue, notify=False)

        if metadata is None:
            continue

        if 'table' in metadata:
            table = metadata['table']
            reports[table] = []

            check = MSSqlTableChecker(table, DB['internalsgid'])
            reports[table].append(Report('internal sgid', issue, check.exists(), MSSqlTableChecker.grade))

            check = MSSqlTableChecker(table, DB['sgid10'])
            reports[table].append(Report('sgid10', issue, check.exists(), MSSqlTableChecker.grade))

            check = MetaTableChecker(f'sgid.{metadata["table"]}', DB['internalsgid'])
            reports[table].append(Report('meta table', issue, check.exists(), MetaTableChecker.grade))
            meta_table_data = check.data

            if meta_table_data.exists != 'missing item name':
                check = PGSqlTableChecker(table, DB['opensgid'])
                check.table = PGSqlTableChecker.postgresize(meta_table_data.item_name)
                reports[table].append(Report('open sgid', issue, check.exists(), PGSqlTableChecker.grade))

                check = OpenDataChecker(meta_table_data.item_name)
                reports[table].append(Report('open data', issue, check.exists(), OpenDataChecker.grade))

            if meta_table_data.exists != 'missing item id':
                check = ArcGisOnlineChecker(meta_table_data.item_id)
                reports[table].append(Report('arcgis online', issue, check.exists(), ArcGisOnlineChecker.grade))

            check = GSheetChecker(table, '11ASS7LnxgpnD0jN4utzklREgMf1pcvYjcXcIcESHweQ', 'SGID Stewardship Info')
            reports[table].append(Report('stewardship', issue, check.exists(), GSheetChecker.grade))

    return reports


def grade_reports(all_reports):
    """turns the reports into actionable items that can be added to the issues as comments
       reports: [namedtuple('Report', 'check ConductorIssue report')]
    """

    grades = {}
    Grade = namedtuple('Grade', 'check grade issue')

    for table, reports in all_reports.items():
        grades[table] = []
        for report in reports:
            git_issue, is_introduction = report.issue

            grades[table].append(Grade(report.check, report.grader(is_introduction, report.report), git_issue))

    return grades


def publish_grades(all_grades):
    """adds a comment to the issue with the grades
        all_grades: dict table: [Grade(check grade issue)]
    """
    comments = []
    for _, grades in all_grades.items():
        issue = grades[0].issue
        comment_table = '| check | status |\n| - | :-: |\n'
        comment = '\n'.join([f'| {grade.check} | {grade.grade} |' for grade in grades])
        comments.append(f'## conductor results\n\n{comment_table}{comment}')

        issue.create_comment(f'## conductor results\n\n{comment_table}{comment}')


    return comments


def extract_metadata_from_issue_body(issue, notify=True):
    """extracts conductor metadata from an issue body
    """
    metadata = None
    for line in issue.body.splitlines():
        if not line.startswith('<!--'):
            continue

        if 'conductor' not in line:
            continue

        start = line.index('{')
        end = line.rindex('}') + 1

        metadata = json.loads(line[start:end])

    if notify and metadata is None:
        _notify_missing_metadata(issue)

    return metadata


def _notify_missing_metadata(issue):
    """leave a comment on an issue and add a label
    """
    issue.add_to_labels('missing-metadata')


if __name__ == '__main__':
    github.enable_console_debug_logging()
    results = startup()
