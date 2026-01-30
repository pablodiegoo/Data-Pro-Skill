# Mermaid Examples Reference

## State Diagram
Useful for finite state machines.

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: Event Triggered
    Processing --> Success: Completed
    Processing --> Error: Failed
    Success --> [*]
    Error --> Idle: Retry
```

## Gantt Chart
Useful for project timelines.

```mermaid
gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD
    section Phase 1
    Analysis      :a1, 2024-01-01, 30d
    Design        :after a1, 20d
    section Phase 2
    Implementation :2024-03-01, 45d
    Testing       : 20d
```

## Entity Relationship Diagram (ERD)
Useful for database schemas.

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER }|..|{ DELIVERY-ADDRESS : uses
```

## User Journey
Useful for product design.

```mermaid
journey
    title My working day
    section Go to work
      Wake up: 5: Me, Cat
      Brush teeth: 5: Me
      Walk to bus: 5: Me
    section Work
      Work on desk: 8: Me
      Go home: 5: Me
```
