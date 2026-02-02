# Mermaid Diagram Selection Guide

## By Use Case

### 📊 Data Visualization

| Need | Diagram | Example |
|------|---------|---------|
| Show proportions | **Pie Chart** | Survey results, market share |
| Compare categories | **XY Chart (bar)** | Sales by region, monthly revenue |
| Show trends | **XY Chart (line)** | Time series, growth metrics |
| Show flow of quantities | **Sankey** | Budget allocation, energy flow |
| Strategic positioning | **Quadrant Chart** | BCG matrix, priority matrix |

### 🔄 Process & Workflow

| Need | Diagram | Example |
|------|---------|---------|
| Decision flow | **Flowchart** | Approval process, algorithms |
| State transitions | **State Diagram** | Order lifecycle, login states |
| Parallel processes | **Flowchart (subgraphs)** | Multi-department workflows |
| Project phases | **Block Diagram** | System pipeline, data flow |

### 📅 Planning & Time

| Need | Diagram | Example |
|------|---------|---------|
| Project schedule | **Gantt Chart** | Sprint planning, roadmap |
| Historical events | **Timeline** | Company history, releases |
| Task management | **Kanban** | Agile boards, todo lists |
| Customer experience | **User Journey** | Onboarding, purchase flow |

### 🏗️ Architecture & Systems

| Need | Diagram | Example |
|------|---------|---------|
| System overview | **C4 Context** | Service boundaries, actors |
| Cloud architecture | **Architecture** | AWS/GCP infrastructure |
| Component layout | **Block Diagram** | Microservices, modules |
| API interactions | **Sequence Diagram** | REST calls, auth flow |
| Network protocols | **Packet Diagram** | TCP/IP headers, data frames |

### 📐 Data Modeling

| Need | Diagram | Example |
|------|---------|---------|
| Database schema | **ERD** | Tables, relationships |
| Object-oriented design | **Class Diagram** | Domain models, inheritance |
| Requirements tracing | **Requirement Diagram** | Specs to implementation |

### 💡 Ideation & Concepts

| Need | Diagram | Example |
|------|---------|---------|
| Brainstorming | **Mindmap** | Feature ideas, research topics |
| Hierarchical concepts | **Mindmap** | Taxonomy, org structure |
| Experience mapping | **User Journey** | Pain points, emotions |

### 🔧 Technical Documentation

| Need | Diagram | Example |
|------|---------|---------|
| Version control | **Gitgraph** | Branching strategy, releases |
| API calls | **Sequence/ZenUML** | Service communication |
| State machines | **State Diagram** | Component behavior |

---

## Quick Decision Tree

```
What are you documenting?
│
├── Data/Metrics?
│   ├── Proportions → Pie Chart
│   ├── Comparison → XY Chart (bar)
│   ├── Trends → XY Chart (line)
│   ├── Flow quantities → Sankey
│   └── 2x2 Analysis → Quadrant
│
├── Process/Flow?
│   ├── Decisions involved → Flowchart
│   ├── States/Lifecycle → State Diagram
│   └── System pipeline → Block Diagram
│
├── Time/Planning?
│   ├── Project schedule → Gantt
│   ├── History/Events → Timeline
│   └── Agile tasks → Kanban
│
├── Architecture?
│   ├── High-level overview → C4 Context
│   ├── Cloud resources → Architecture
│   ├── Component relations → Block
│   └── Service calls → Sequence
│
├── Data Model?
│   ├── Database → ERD
│   └── Classes/OOP → Class Diagram
│
├── Concepts/Ideas?
│   ├── Brainstorm → Mindmap
│   └── Experience → User Journey
│
└── Technical?
    ├── Git branches → Gitgraph
    ├── API flow → Sequence/ZenUML
    └── Network → Packet Diagram
```

---

## Diagram Complexity Guide

| Simple (1-5 min) | Medium (5-15 min) | Complex (15+ min) |
|------------------|-------------------|-------------------|
| Pie Chart | Flowchart (large) | C4 Context |
| Timeline | Sequence Diagram | Architecture |
| Simple Flowchart | State Diagram | ERD (full schema) |
| Mindmap (small) | Gantt Chart | Class Diagram |
| Gitgraph (simple) | XY Chart | Sankey (many flows) |
