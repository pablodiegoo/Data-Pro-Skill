#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');
const https = require('https');
const readline = require('readline');

const rl = readline.createInterface({ input: process.stdin, output: process.stdout, terminal: Boolean(process.stdin.isTTY) });
const lineQueue = [];
const lineWaiters = [];
let rlClosed = false;
rl.on('line', (line) => {
  if (lineWaiters.length > 0) lineWaiters.shift()(line);
  else lineQueue.push(line);
});
rl.on('close', () => {
  rlClosed = true;
  while (lineWaiters.length > 0) lineWaiters.shift()('');
});
const ask = (q) => new Promise((r) => {
  process.stdout.write(q);
  if (lineQueue.length > 0) return r(lineQueue.shift());
  if (rlClosed) return r('');
  lineWaiters.push(r);
});
const expand = (p) => p.startsWith('~') ? path.join(os.homedir(), p.slice(1)) : p;

const RAW = 'https://raw.githubusercontent.com/pablodiegoo/Data-Pro-Skill/main';
const CMD_LIST  = ['grill', 'clarify', 'setup', 'plan', 'cross', 'execute', 'advanced', 'inject-open', 'export'];
const MODE_LIST = ['mode:quant', 'mode:quali', 'mode:strategy'];
const ALL_CMDS  = [...CMD_LIST, ...MODE_LIST];
const ROOT_FILES = ['SKILL.md', 'constitution.md', 'GLOSSARY.md'];
const SCRIPT_FILES = [
  'crosstabs.py', 'quant_analyzer.py', 'qual_analyzer.py',
  'qualitative_categorizer.py', 'final_report_generator.py',
  'survey_report_generator.py', 'survey_pca.py', 'turf_analysis.py',
  'eda_notebook_generator.py', 'advanced_analytics_generator.py', 'weighting.py',
  'tufte_viz.py', 'tufte_html.py', 'design_schools.py',
];
const AGENT_FILES = [
  'agent-griller.md', 'agent-statistician.md', 'agent-critic.md',
  'agent-tufte-designer.md', 'agent-anthropologist.md', 'agent-strategist.md',
];
const REF_FILES = [
  'agent-loop.md', 'dps-clarify.md', 'dps-setup.md', 'dps-plan.md',
  'dps-cross.md', 'dps-execute.md', 'dps-advanced.md',
  'dps-inject-open.md', 'dps-export.md', 'modes.md', 'tufte-rules.md',
  'design-schools.md',
];
const ANALYSIS_FILES = [
  'analytical_methodology_patterns.md', 'causal.md', 'evaluation_and_diagnostics.md',
  'explicit_weight_handling.md', 'halo_removal.md', 'markdown_generation_escapes.md',
  'multivariate.md', 'new_methodologies.md', 'notebook_generation_pattern.md',
  'numbered_report_generation.md', 'priority_matrix.md', 'reasoning_rules.csv',
  'science.md', 'statistical_test_selector.md', 'stopwords_pt.txt',
  'survey_branching_validation.md', 'survey_governance.md',
];
const STYLE_FILES = [
  'tufte.css', 'few.css', 'knaflic.css', 'swiss.css', 'editorial.css',
  'palettes.csv', 'visualization_rules.csv', 'visualization_styles.csv',
];

const DESIGN_SCHOOLS = [
  { id: 'tufte',     name: 'Edward Tufte (Classic Data-Ink & Sidenote School)',        desc: 'Ivory #fffff8, Palatino serif, 58%/36% floating Margin Notes & Cleveland dot plots [Default]' },
  { id: 'few',       name: 'Stephen Few (Perceptual Dashboard & Bullet-Graph School)', desc: 'Perceptual full-width BI grid, Bullet Graphs, high-density tables & threshold alerts' },
  { id: 'knaflic',   name: 'Cole Knaflic (Storytelling with Data / Executive School)', desc: 'Decluttered white canvas, grey context + bold preattentive focal color & Action Titles' },
  { id: 'swiss',     name: 'Swiss Grid & Jacques Bertin (International Grid School)',  desc: 'Exposed architectural modular grid, Neo-Grotesque sans & Bertin retinal matrices' },
  { id: 'editorial', name: 'The Economist / FT Editorial (Data Journalism School)',    desc: 'Warm newsprint, signature crimson top bar, Kicker/Standfirst & lollipop range charts' },
];

const REPO_ROOT = path.resolve(__dirname, '..');

async function loadAsset(relPath) {
  const localCandidate = path.join(REPO_ROOT, relPath);
  if (fs.existsSync(localCandidate) && fs.statSync(localCandidate).isFile()) {
    return fs.readFileSync(localCandidate, 'utf-8');
  }
  return await dl(`${RAW}/${relPath}`);
}

function dl(url) {
  return new Promise((resolve, reject) => {
    https.get(url, r => {
      if (r.statusCode !== 200) return reject(new Error(`HTTP ${r.statusCode}`));
      let d = '';
      r.on('data', c => d += c);
      r.on('end', () => resolve(d));
    }).on('error', reject);
  });
}

function writeFile(dir, name, content) {
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, name), content);
}

const HARNESSES = [
  { id: 'opencode',      name: 'OpenCode',        dir: '~/.config/opencode',      command: true },
  { id: 'gemini',        name: 'Gemini CLI',       dir: '~/.gemini',               command: false },
  { id: 'codex',         name: 'Codex CLI',        dir: '~/.codex',                 command: false },
  { id: 'antigravity',   name: 'Antigravity CLI',  dir: '~/.antigravitycli',        command: false },
  { id: 'copilot',       name: 'GitHub Copilot',   dir: '~/.github',               command: false },
];

async function installHarness(h, localDps) {
  const base = expand(h.dir);
  const skillDir = path.join(base, 'skills', 'data-pro-skill');
  fs.mkdirSync(skillDir, { recursive: true });

  const srcDir = localDps || skillDir;

  for (const f of ROOT_FILES) {
    const c = fs.existsSync(path.join(srcDir, f)) ? fs.readFileSync(path.join(srcDir, f), 'utf-8') : await loadAsset(f);
    writeFile(skillDir, f, c);
  }

  // Command stubs (only OpenCode)
  if (h.command) {
    const cmdDir = path.join(base, 'command');
    fs.mkdirSync(cmdDir, { recursive: true });
    for (const cmd of ALL_CMDS) {
      const name = `dps-${cmd}`;
      writeFile(cmdDir, `${name}.md`,
`---
description: "Data-Pro-Skill: /${name}"
---

Execute \`/${name}\` as defined in SKILL.md.

@${skillDir}/SKILL.md
@${skillDir}/constitution.md
@${skillDir}/references
`);
    }
  }
  console.log(`  ✓ ${h.name} (skill${h.command ? ` + ${ALL_CMDS.length} commands` : ''})`);
}

async function main() {
  const args = process.argv.slice(2);

  // ── REMOVE ─────────────────────────────────────────────────────
  if (args.includes('--remove') || args.includes('--uninstall')) {
    for (const h of HARNESSES) {
      const base = expand(h.dir);
      fs.rmSync(path.join(base, 'skills', 'data-pro-skill'), { recursive: true, force: true });
      for (const c of ALL_CMDS) {
        fs.rmSync(path.join(base, 'command', `dps-${c}.md`), { recursive: true, force: true });
      }
    }
    fs.rmSync(path.join(process.cwd(), '.dps'), { recursive: true, force: true });
    console.log('✓ Data-Pro-Skill removed from all harnesses and project\n');
    rl.close(); return;
  }

  // ── UPDATE ─────────────────────────────────────────────────────
  if (args.includes('--update')) {
    const dps = path.join(process.cwd(), '.dps');
    if (fs.existsSync(dps)) {
      console.log('   Updating .dps/ from GitHub...');
      fs.rmSync(dps, { recursive: true, force: true });
    }
    // Fall through to install
    console.log(`\n\u001b[36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n Data-Pro-Skill v2 — Updater\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\n`);
    args.forEach(a => { if (a === '--update') {} });
  } else {
    console.log(`\n\u001b[36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n Data-Pro-Skill v2 — Installer\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\n`);
  }

  let hasLocal = false;
  let hasHarness = false;
  if (args.includes('--local') || args.includes('--global')) {
    hasLocal = args.includes('--local');
    hasHarness = args.includes('--global');
  } else {
    const ans1 = await ask('Install type:\n  0. Local (current project)\n  1. Global (harness config)\n  2. Both\n\nChoice [2]: ');
    const t = parseInt(ans1 || '2', 10);
    hasLocal = t === 0 || t === 2;
    hasHarness = t === 1 || t === 2;
  }

  let selected = [];
  if (hasHarness) {
    console.log('');
    const ans2 = await ask('Harnesses to install:\n' +
      HARNESSES.map((h, i) => `  ${i + 1}. ${h.name}`).join('\n') +
      `\n  ${HARNESSES.length + 1}. All\n\nNumbers [6]: `);
    const nums = (ans2 || `${HARNESSES.length + 1}`)
      .split(/[,;\s]+/).map(s => parseInt(s, 10)).filter(n => !isNaN(n));
    selected = nums.includes(HARNESSES.length + 1)
      ? HARNESSES
      : HARNESSES.filter((_, i) => nums.includes(i + 1));
  }

  // Resolve Data Design School from --school flag or interactive prompt
  let cliSchool = null;
  const schoolFlagIdx = args.findIndex(a => a === '--school' || a === '-s');
  if (schoolFlagIdx !== -1 && args[schoolFlagIdx + 1]) {
    cliSchool = args[schoolFlagIdx + 1].toLowerCase().trim();
  }
  let chosenSchool = DESIGN_SCHOOLS[0];
  if (cliSchool) {
    const found = DESIGN_SCHOOLS.find(s => s.id === cliSchool || s.name.toLowerCase().includes(cliSchool));
    if (found) chosenSchool = found;
  } else {
    console.log('');
    const ansSchool = await ask(
      'Default Data Design School (/dps-setup & /dps-export):\n' +
      DESIGN_SCHOOLS.map((s, i) => `  ${i + 1}. ${s.id.padEnd(10)} — ${s.desc}`).join('\n') +
      '\n\nSchool [1 (tufte)]: '
    );
    const trimmed = (ansSchool || '1').trim().toLowerCase();
    const numChoice = parseInt(trimmed, 10);
    if (!isNaN(numChoice) && numChoice >= 1 && numChoice <= DESIGN_SCHOOLS.length) {
      chosenSchool = DESIGN_SCHOOLS[numChoice - 1];
    } else {
      const byName = DESIGN_SCHOOLS.find(s => s.id === trimmed || s.name.toLowerCase().includes(trimmed));
      if (byName) chosenSchool = byName;
    }
  }

  let localDps = null;

  // ── LOCAL PROJECT ──────────────────────────────────────────────
  if (hasLocal) {
    const cwd = process.cwd();
    const dps = path.join(cwd, '.dps');
    console.log(`\n  → Installing local project: ${dps} (Design School: ${chosenSchool.id})`);

    if (fs.existsSync(dps)) fs.rmSync(dps, { recursive: true, force: true });
    fs.mkdirSync(dps, { recursive: true });

    // SKILL.md + constitution.md + GLOSSARY.md
    for (const rf of ROOT_FILES) {
      writeFile(dps, rf, await loadAsset(rf));
    }
    console.log('  ✓ SKILL.md + constitution.md + GLOSSARY.md');

    // Scripts
    const scriptsDir = path.join(dps, 'scripts');
    for (const s of SCRIPT_FILES) {
      writeFile(scriptsDir, s, await loadAsset(`scripts/${s}`));
    }
    console.log(`  ✓ ${SCRIPT_FILES.length} Python scripts`);

    // Agents
    const agentsDir = path.join(dps, 'agents');
    for (const a of AGENT_FILES) {
      writeFile(agentsDir, a, await loadAsset(`agents/${a}`));
    }
    console.log(`  ✓ ${AGENT_FILES.length} agents`);

    // References
    for (const r of REF_FILES) {
      writeFile(path.join(dps, 'references'), r, await loadAsset(`references/${r}`));
    }
    for (const an of ANALYSIS_FILES) {
      writeFile(path.join(dps, 'references', 'analysis'), an, await loadAsset(`references/analysis/${an}`));
    }
    console.log(`  ✓ ${REF_FILES.length + ANALYSIS_FILES.length} reference & survey science files`);

    // Styles (tufte.css, few.css, knaflic.css, swiss.css, editorial.css + CSVs)
    for (const s of STYLE_FILES) {
      const styleContent = await loadAsset(`references/styles/${s}`);
      writeFile(path.join(dps, 'references', 'styles'), s, styleContent);
      if (s.endsWith('.css')) {
        writeFile(path.join(dps, 'references'), s, styleContent);
      }
    }
    console.log(`  ✓ ${STYLE_FILES.length} style files (5 Data Design Schools)`);

    // Output dirs
    for (const d of ['setup', 'cross', 'advanced', 'quali', 'export']) {
      fs.mkdirSync(path.join(dps, 'outputs', d), { recursive: true });
    }

    // Persist chosen Data Design School in .dps/config.json and .dps/outputs/setup/design_school.json
    const schoolConfig = JSON.stringify({
      design_school: chosenSchool.id,
      design_school_name: chosenSchool.name,
      updated_at: new Date().toISOString(),
    }, null, 2) + '\n';
    writeFile(dps, 'config.json', schoolConfig);
    writeFile(path.join(dps, 'outputs', 'setup'), 'design_school.json', schoolConfig);
    console.log(`  ✓ Default Data Design School locked: ${chosenSchool.name} (${chosenSchool.id})`);

    // Requirements
    writeFile(dps, 'requirements.txt', 'pandas>=2.0\nnumpy>=1.24\nscipy>=1.11\nscikit-learn>=1.3\n');

    // AGENTS.md
    const agentsMd = path.join(cwd, 'AGENTS.md');
    const ref = '\n<!-- DPS:project -->\n- @.dps/SKILL.md\n- @.dps/constitution.md\n- @.dps/GLOSSARY.md\n<!-- /DPS -->\n';
    if (fs.existsSync(agentsMd)) {
      if (!fs.readFileSync(agentsMd, 'utf-8').includes('DPS:project'))
        fs.appendFileSync(agentsMd, ref);
    } else {
      fs.writeFileSync(agentsMd, ref);
    }
    console.log('  ✓ AGENTS.md');

    localDps = dps;
  }

  // ── HARNESS ────────────────────────────────────────────────────
  if (selected.length) {
    console.log(`\n  → Installing harness(es):`);
    for (const h of selected) {
      await installHarness(h, localDps);
    }
  }

  // ── DONE ───────────────────────────────────────────────────────
  console.log(`\n\u001b[32m✓ Data-Pro-Skill v2 installed\u001b[0m`);
  if (hasLocal)  console.log('  Local:  .dps/ with scripts + agents');
  if (selected.length) console.log(`  Global: ${selected.length} harness(es)`);
  if (hasLocal)  console.log('\n  Then:   pip install -r .dps/requirements.txt --break-system-packages');
  console.log('');
  rl.close();
}

main().catch(e => { console.error(`\n✗ ${e.message}`); process.exit(1); });
