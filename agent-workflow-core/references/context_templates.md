# Context Templates

Read only when creating a context workspace, environment map, navigation, task snapshot or log. Adapt the matching example; existing task restoration needs no template load.

## Contents

- [Template 1](#template-1)
- [Template 2](#template-2)
- [Template 3](#template-3)
- [Template 4](#template-4)
- [Template 5](#template-5)
- [Template 6](#template-6)

## Template 1

```markdown
# <Local context map>

## <Quick entry>

- <Task navigation>: [`context.md`](context.md)
- <Machine environment>: [`environment.md`](environment.md)

## <Information owners>

| Information | Single owner |
| --- | --- |
| Active and closed task navigation | `context.md` |
| Current task snapshot | `tasks/<TASK_ID>.md` |
| Machine-specific runtime and paths | `environment.md` |
| Optional append-only agent log | `agent_logs/<TASK_ID>.agent_log.md` |
```

## Template 2

```markdown
# Local Environments

Minimal local environment map for skills. Store only machine-specific facts needed to choose the correct runtime and avoid guessing.

## Runtime Resolution

- preferred shell: `<shell or unknown>`
- forbidden aliases: `<aliases and reason, or none>`
- selection precedence: `project/repo runtime -> exact generic validation runtime -> bounded discovery`

| Workload | Exact runtime/command | Scope/status |
| --- | --- | --- |
| Generic validation | `<exact path/command or unknown>` | `<user-confirmed, draft/unconfirmed, or unknown>` |
| Project runtime | `<exact path/command or unknown>` | `<project/shell constraints>` |

## Repository Roots

- context workspace: `<path or unknown>`
- primary repo: `<path or unknown>`
- dbt root: `<path or unknown>`
- Python project root: `<path or unknown>`
- extra repo roots: `<path(s) or unknown>`

## Local Executables

| Tool | Exact path/version | Scope/status |
| --- | --- | --- |
| `<tool>` | `<exact path/version or unknown>` | `<selection constraint or status>` |

## Local Config Pointers

- `<purpose>`: `<secret-safe file path or unknown>`

## Boundaries

- current configuration only; task/project history lives in its owning context
- local executables are not an inventory of installed skills or MCP servers
- no credential values, account identities, or access/approval policy
- discovered values: `<draft/unconfirmed or user-confirmed>`
```

## Template 3

```markdown
# Локальный контекст задач

В этом файле хранится навигация по локальному контексту задач. Подробности ведутся в отдельных файлах, а не здесь.

## Как вести контекст

- Каждую отдельную задачу с task id вести в `tasks/<TASK_ID>.md`.
- `context.md` использовать как индекс и точку входа, а не как журнал.
- Новые незавершённые задачи добавлять в `Активные задачи`.
- Завершённые задачи переносить в `Закрытые задачи` с кратким итогом.

## Активные задачи

## Закрытые задачи
```

## Template 4

```markdown
# <Meta-task name>

## Назначение

## Текущий фокус

## Открытые вопросы

## Архитектура контекста

## Как вести контекст

## Текущее состояние

## Журнал
```

## Template 5

```markdown
# <TASK_ID> - short title

## Текущий статус

## Цель

## План

## Валидация

## Контекст

## Решения

## Проверки

## Изменения

## Риски и стоп-точки

## Следующий шаг

## Архив
```

## Template 6

```markdown
# <TASK_ID> Agent Log

## YYYY-MM-DD HH:MM MSK

### Mode

### Active skills

### Skill routing updates

### Facts

### Hypotheses

### Checks

### Decisions

### Rejected alternatives

### Validation

### Self-review
```
