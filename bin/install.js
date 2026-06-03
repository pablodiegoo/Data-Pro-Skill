#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');
const https = require('https');
const readline = require('readline');

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise((r) => rl.question(q, r));
const expand = (p) => p.startsWith('~') ? path.join(os.homedir(), p.slice(1)) : p;

const RAW = 'https://raw.githubusercontent.com/pablodiegoo/Data-Pro-Skill/main';
const CMD_LIST  = ['setup', 'cross', 'inject-open', 'export', 'clarify', 'plan'];
const MODE_LIST = ['mode:quant', 'mode:quali', 'mode:strategy'];
const ALL_CMDS  = [...CMD_LIST, ...MODE_LIST];
const SCRIPT_FILES = [
  'crosstabs.py', 'quant_analyzer.py', 'qual_analyzer.py',
  'qualitative_categorizer.py', 'final_report_generator.py',
  'survey_report_generator.py', 'survey_pca.py', 'turf_analysis.py',
  'eda_notebook_generator.py', 'advanced_analytics_generator.py', 'weighting.py',
];
const AGENT_FILES = [
  'agent-statistician.md', 'agent-critic.md', 'agent-tufte-designer.md',
  'agent-anthropologist.md', 'agent-strategist.md',
];

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

  for (const f of ['SKILL.md', 'constitution.md']) {
    const c = fs.existsSync(path.join(srcDir, f)) ? fs.readFileSync(path.join(srcDir, f), 'utf-8') : await dl(`${RAW}/${f}`);
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
`);
    }
  }
  console.log(`  ✓ ${h.name} (skill${h.command ? ` + ${ALL_CMDS.length} commands` : ''})`);
}

async function main() {
  console.log(`\n\u001b[36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n Data-Pro-Skill v2 — Installer\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\n`);

  console.log('Destinations:\n  0. Local project (current dir)\n' +
    HARNESSES.map((h, i) => `  ${i + 1}. ${h.name}`).join('\n') +
    `\n  ${HARNESSES.length + 1}. All harnesses\n`);
  const ans = await ask('Enter number(s) [1]: ');
  const nums = (ans || '1').split(/[,;\s]+/).map(s => parseInt(s, 10)).filter(n => !isNaN(n));
  const hasLocal = nums.includes(0);
  const hasAll   = nums.includes(HARNESSES.length + 1);
  const selected = hasAll ? HARNESSES : HARNESSES.filter((_, i) => nums.includes(i + 1));

  let localDps = null;

  // ── LOCAL PROJECT ──────────────────────────────────────────────
  if (hasLocal) {
    const cwd = process.cwd();
    const dps = path.join(cwd, '.dps');
    console.log(`\n  → Installing local project: ${dps}`);

    if (fs.existsSync(dps)) fs.rmSync(dps, { recursive: true, force: true });
    fs.mkdirSync(dps, { recursive: true });

    // SKILL.md + constitution.md
    writeFile(dps, 'SKILL.md',       await dl(`${RAW}/SKILL.md`));
    writeFile(dps, 'constitution.md', await dl(`${RAW}/constitution.md`));
    console.log('  ✓ SKILL.md + constitution.md');

    // Scripts
    const scriptsDir = path.join(dps, 'scripts');
    for (const s of SCRIPT_FILES) {
      writeFile(scriptsDir, s, await dl(`${RAW}/scripts/${s}`));
    }
    console.log(`  ✓ ${SCRIPT_FILES.length} Python scripts`);

    // Agents
    const agentsDir = path.join(dps, 'agents');
    for (const a of AGENT_FILES) {
      writeFile(agentsDir, a, await dl(`${RAW}/agents/${a}`));
    }
    console.log(`  ✓ ${AGENT_FILES.length} agents`);

    // Output dirs
    for (const d of ['setup', 'cross', 'quali', 'export']) {
      fs.mkdirSync(path.join(dps, 'outputs', d), { recursive: true });
    }

    // Requirements
    writeFile(dps, 'requirements.txt', 'pandas>=2.0\nnumpy>=1.24\nscipy>=1.11\nscikit-learn>=1.3\n');

    // AGENTS.md
    const agentsMd = path.join(cwd, 'AGENTS.md');
    const ref = '\n<!-- DPS:project -->\n- @.dps/SKILL.md\n- @.dps/constitution.md\n<!-- /DPS -->\n';
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
