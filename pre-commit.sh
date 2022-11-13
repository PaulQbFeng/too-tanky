#!/usr/bin/env bash
CHANGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')
CHANGED_FILES=`echo $CHANGED_FILES`  # Strip newlines
if [[ -n "$CHANGED_FILES" ]] ; then
  echo X $CHANGED_FILES 1>&2
  # isort -q $CHANGED_FILES
  black -q $CHANGED_FILES
  git add $CHANGED_FILES
fi
