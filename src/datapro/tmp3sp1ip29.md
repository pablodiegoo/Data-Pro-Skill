---
title: "Report"
subtitle: ""
author: "DataPro"
date: "February 2026"
titlepage: true
titlepage-color: "1a5276"
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "FFFFFF"
titlepage-rule-height: 2
toc: false
toc-title: "Table of Contents"
toc-own-page: true
numbersections: true
geometry: "margin=2.5cm"
fontsize: 11pt
mainfont: "Inter"
sansfont: "Inter"
documentclass: report
colorlinks: true
linkcolor: "1a5276"
urlcolor: "1a5276"
header-includes:
  - \usepackage{graphicx}
  - \usepackage{float}
  - \floatplacement{figure}{H}
  - \setlength{\parindent}{0pt}
  - \setlength{\parskip}{6pt}
  - \usepackage{caption}
  - \captionsetup{justification=centering}
  - \usepackage{etoolbox}
  - \AtBeginEnvironment{figure}{\centering}
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhead[L]{\small }
  - \fancyhead[R]{\small \thepage}
  - \fancyfoot[C]{}
  - \renewcommand{\headrulewidth}{0.4pt}
  - \usepackage{booktabs}
  - \usepackage{longtable}
  - \usepackage{multicol}
---



```{=latex}
\begin{multicols}{2}
```

# Simple Test

This is a simple test without mermaid.

## Section 1
Content here.

## Section 2
More content.


```{=latex}
\end{multicols}
```

