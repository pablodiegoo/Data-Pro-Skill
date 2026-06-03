#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');
const readline = require('readline');

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise((r) => rl.question(q, r));
const expand = (p) => p.startsWith('~') ? path.join(os.homedir(), p.slice(1)) : p;

const REPO = 'https://github.com/pablodiegoo/Data-Pro-Skill.git';
const RAW = 'https://raw.githubusercontent.com/pablodiegoo/Data-Pro-Skill/main';

const CMD_LIST = [
  'setup', 'cross', 'inject-open', 'export', 'clarify', 'plan',
  'mode:quant', 'mode:quali', 'mode:strategy'
];

const HARNESSES = [
  { id: 'opencode',      name: 'OpenCode',        dir: '~/.config/opencode' },
  { id: 'gemini',        name: 'Gemini CLI',       dir: '~/.gemini' },
  { id: 'codex',         name: 'Codex CLI',        dir: '~/.codex' },
  { id: 'antigravity',   name: 'Antigravity CLI',  dir: '~/.antigravitycli' },
  { id: 'copilot',       name: 'GitHub Copilot',   dir: '~/.github' },
];

const LABELS = HARNESSES.map((h, i) => `${i + 1}. ${h.name}`).join('\n');
const PROMPT = `Select destination(s) [1]:

  0. Local project (current dir)
${LABELS}
  ${HARNESSES.length + 1}. All harnesses

Enter: `;

function stubsFor(targetDir, cmdDir) {
  fs.mkdirSync(cmdDir, { recursive: true });
  for (const cmd of CMD_LIST) {
    const name = `dps-${cmd}`;
    fs.writeFileSync(path.join(cmdDir, `${name}.md`),
`---
description: "Data-Pro-Skill: /${name}"
---

Execute \`/${name}\` via the Data-Pro-Skill pipeline.

@${targetDir}/SKILL.md
@${targetDir}/constitution.md
@${targetDir}/scripts
`);
  }
}

async function main() {
  console.log(`\n\u001b[36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n Data-Pro-Skill v2 — Installer\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\n`);

  const ans = await ask(PROMPT);
  const nums = (ans || '1')
    .split(/[,;\s]+/)
    .map(s => parseInt(s, 10))
    .filter(n => !isNaN(n));
  const hasLocal  = nums.includes(0);
  const hasAll    = nums.includes(HARNESSES.length + 1);
  const selected  = hasAll
    ? HARNESSES
    : HARNESSES.filter((_, i) => nums.includes(i + 1));

  // ── LOCAL PROJECT ──────────────────────────────────────────────
  if (hasLocal) {
    const cwd = process.cwd();
    const dps = path.join(cwd, '.dps');
    console.log(`\n  → Installing in ${cwd}`);

    if (fs.existsSync(dps)) {
      console.log('    ⚠ .dps/ exists — run: git -C .dps pull origin main');
    } else {
      execSync(`git clone --depth 1 ${REPO} "${dps}"`, { stdio: 'inherit' });
      console.log('    ✓ .dps/ cloned');
    }

    // Output directories
    for (const d of ['setup', 'cross', 'quali', 'export']) {
      fs.mkdirSync(path.join(dps, 'outputs', d), { recursive: true });
    }
    console.log('    ✓ outputs/ prepared');

    // Requirements
    fs.writeFileSync(path.join(dps, 'requirements.txt'),
      'pandas>=2.0\nnumpy>=1.24\nscipy>=1.11\nscikit-learn>=1.3\n');
    console.log('    ✓ requirements.txt');

    // AGENTS.md
    const agents = path.join(cwd, 'AGENTS.md');
    const ref = '\n<!-- DPS:project -->\n- @.dps/SKILL.md\n- @.dps/constitution.md\n<!-- /DPS -->\n';
    if (fs.existsSync(agents)) {
      if (!fs.readFileSync(agents, 'utf-8').includes('DPS:project')) {
        fs.appendFileSync(agents, ref);
      }
    } else {
      fs.writeFileSync(agents, ref);
    }
    console.log('    ✓ AGENTS.md');
  }

  // ── HARNESS INSTALL ────────────────────────────────────────────
  const dpsPath = hasLocal
    ? path.join(process.cwd(), '.dps')
    : null;

  for (const h of selected) {
    const base = expand(h.dir);
    const skillDir = path.join(base, 'skills', 'data-pro-skill');
    const cmdDir   = path.join(base, 'command');

    fs.mkdirSync(skillDir, { recursive: true });

    // Copy skill files from local .dps/ or download from GitHub
    if (dpsPath && fs.existsSync(path.join(dpsPath, 'SKILL.md'))) {
      fs.copyFileSync(path.join(dpsPath, 'SKILL.md'),       path.join(skillDir, 'SKILL.md'));
      fs.copyFileSync(path.join(dpsPath, 'constitution.md'), path.join(skillDir, 'constitution.md'));
    } else {
      // Fallback: download from GitHub
      const https = require('https');
      const dl = (url, dest) => new Promise((resolve, reject) => {
        https.get(url, r => {
          if (r.statusCode !== 200) return reject(new Error(`HTTP ${r.statusCode}`));
          let d = '';
          r.on('data', c => d += c);
          r.on('end', () => { fs.writeFileSync(dest, d); resolve(); });
        }).on('error', reject);
      });
      await dl(`${RAW}/SKILL.md`,       path.join(skillDir, 'SKILL.md'));
      await dl(`${RAW}/constitution.md`, path.join(skillDir, 'constitution.md'));
    }
    console.log(`    ✓ ${h.name}: skill`);

    // Command stubs – linked to the local .dps/ if available
    const targetDir = dpsPath || skillDir;
    stubsFor(targetDir, cmdDir);
    console.log(`    ✓ ${h.name}: ${CMD_LIST.length} commands`);
  }

  // ── SUMMARY ────────────────────────────────────────────────────
  console.log(`\n\u001b[32m✓ Data-Pro-Skill v2 installed\u001b[0m`);
  if (hasLocal) console.log('  Local:  .dps/ — run: /dps-setup');
  if (selected.length) console.log(`  Global: ${selected.length} harness(es) — restart and run: /dps-setup`);
  console.log(`\nInstall Python deps:  pip install -r .dps/requirements.txt\n`);
  rl.close();
}

main().catch(e => { console.error(`\n✗ ${e.message}`); process.exit(1); });
