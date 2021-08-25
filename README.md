# timecard
CLI tool for tracking various tasks and storing completed 'shifts' 


### Urgent TODO

- `update()` function that can tell if current working task has been renamed
- If no current working task, set one automatically 

### TODO

- Output shifts for a given task 
- interactive 'scrolling' with <tab> for task selection 
- shell mode 
- undo 
- output shifts to `punchcard` for displaying graphically amount worked on task (like github)


### Usage

```
$ timecard view --ongoing 
# just show all tasks that are currently active 

$ timecard rename "Task1" "New Name"
# Renames task
```