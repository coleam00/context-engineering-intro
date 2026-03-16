# Parallel Task Version Execution

## Variables
FEATURE_NAME: $ARGUMENTS
PLAN_TO_EXECUTE: $ARGUMENTS
NUMBER_OF_PARALLEL_WORKTREES: $ARGUMENTS

## Instructions

We're going to create NUMBER_OF_PARALLEL_WORKTREES new subagents that use the Task tool to create N versions of the same feature in parallel.

Be sure to read PLAN_TO_EXECUTE.

This enables use to concurrently build the same feature in parallel so we can test and validate each subagent's changes in isolation then pick the best changes.

The first agent will run in trees/<FEATURE_NAME>-1/
The second agent will run in trees/<FEATURE_NAME>-2/
...
The last agent will run in trees/<FEATURE_NAME>-<NUMBER_OF_PARALLEL_WORKTREES>/

The code in trees/<FEATURE_NAME>-<i>/ will be identical to the code in the current branch. It will be setup and ready for you to build the feature end to end.

Each agent will independently implement the engineering plan detailed in PLAN_TO_EXECUTE in their respective workspace.

When the subagent completes it's work, have the subagent to report their final changes made in a comprehensive `RESULTS.md` file at the root of their respective workspace.

Make sure agents don't run any tests or other code - focus on the code changes only.