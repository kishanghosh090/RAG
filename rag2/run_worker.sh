#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
exec rq worker --url redis://13.204.134.210:6379 "$@"