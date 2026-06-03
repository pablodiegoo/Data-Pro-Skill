#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');
const http = require('https');
const readline = require('readline');

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise((r) => rl.question(q, r));
const expand = (p) => p.startsWith('~') ? path.join(os.homedir(), p.slice(1)) : p;

const REPO_URL = 'https://raw.githubusercontent.com/pablodiegoo/Data-Pro-Skill/main';

const RUNTIMES = {
  opencode: {
    name: 'OpenCode',
    dir: '~/.config/opencode',
    needsCommandStubs: true,
    needsPerCommandSkills: false,
    extraDirs: [],
  },
  gemini: {
    name: 'Gemini CLI',
    dir: '~/.gemini',
    needsCommandStubs: false,
    needsPerCommandSkills: false,
    extraDirs: ['~/.gemini/antigravity/skills'],
  },
  codex: {
    name: 'Codex CLI',
    dir: '~/.codex',
    needsCommandStubs: false,
    needsPerCommandSkills: true,
    extraDirs: [],
  },
  antigravity: {
    name: 'Antigravity CLI',
    dir: '~/.antigravitycli',
    needsCommandStubs: false,
    needsPerCommandSkills: true,
    extraDirs: [],
  },
  copilot: {
    name: 'GitHub Copilot',
    dir: '~/.github',
    needsCommandStubs: false,
    needsPerCommandSkills: false,
    extraDirs: [],
  },
};

const DPS_COMMANDS = ['setup', 'cross', 'inject-open', 'export', 'clarify', 'plan'];
const DPS_MODES = ['mode:quant', 'mode:quali', 'mode:strategy'];

function download(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode} fetching ${url}`));
        return;
      }
      let data = '';
      res.on('data', (c) => data += c);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

async function installForRuntime(runtime, skillBase) {
  const targetDir = path.join(skillBase, 'data-pro-skill');
  fs.mkdirSync(targetDir, { recursive: true });

  console.log(`\n  → Installing to ${runtime.name}`);

  // Download SKILL.md + constitution.md
  for (const file of ['SKILL.md', 'constitution.md']) {
    const url = `${REPO_URL}/${file}`;
    const content = await download(url);
    fs.writeFileSync(path.join(targetDir, file), content);
    console.log(`    ✓ ${file} (${(content.length / 1024).toFixed(0)}KB)`);
  }

  // Extra dirs (Gemini antigravity)
  for (const extra of runtime.extraDirs) {
    const d = expand(extra);
    fs.mkdirSync(d, { recursive: true });
    for (const file of ['SKILL.md', 'constitution.md']) {
      const content = await download(`${REPO_URL}/${file}`);
      fs.writeFileSync(path.join(d, file), content);
    }
    console.log(`    ✓ extra: ${extra}`);
  }

  // Command stubs (OpenCode)
  if (runtime.needsCommandStubs) {
    const cmdDir = path.join(expand(runtime.dir), 'command');
    fs.mkdirSync(cmdDir, { recursive: true });
    for (const cmd of [...DPS_COMMANDS, ...DPS_MODES]) {
      const name = `dps-${cmd}`;
      fs.writeFileSync(path.join(cmdDir, `${name}.md`),
`---
description: "Data-Pro-Skill: /${name}"
---

Execute \`/${name}\` as defined in the Data-Pro-Skill meta-prompt.

@${targetDir}/SKILL.md
@${targetDir}/constitution.md
`);
    }
    console.log(`    ✓ ${DPS_COMMANDS.length + DPS_MODES.length} command stubs`);
  }

  // Per-command skill dirs (Codex, Antigravity)
  if (runtime.needsPerCommandSkills) {
    for (const cmd of [...DPS_COMMANDS, ...DPS_MODES]) {
      const name = `dps-${cmd}`;
      const dir = path.join(skillBase, name);
      fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(path.join(dir, 'SKILL.md'),
`---
name: ${name}
description: "Data-Pro-Skill: /${name}"
---

Execute \`/${name}\` as defined in the Data-Pro-Skill meta-prompt.

@${targetDir}/SKILL.md
@${targetDir}/constitution.md
`);
    }
    console.log(`    ✓ ${DPS_COMMANDS.length + DPS_MODES.length} command skills`);
  }
}

async function main() {
  console.log(`
\x1b[36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Data-Pro-Skill v2 — Installer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m
`);
  const keys = Object.keys(RUNTIMES);
  console.log('Select AI harness:\n');
  keys.forEach((k, i) => console.log(`  ${i + 1}. ${RUNTIMES[k].name}`));
  console.log(`  ${keys.length + 1}. All of the above`);

  const ans = await ask(`\nEnter number [1]: `);
  const idx = parseInt(ans || '1', 10) - 1;

  const list = (idx >= keys.length)
    ? Object.entries(RUNTIMES)
    : [[keys[idx] || 'opencode', RUNTIMES[keys[idx] || 'opencode']]];

  for (const [, rt] of list) {
    const skillBase = path.join(expand(rt.dir), 'skills');
    await installForRuntime(rt, skillBase);
  }

  console.log(`\n\x1b[32m✓ Data-Pro-Skill v2 installed to ${list.length} runtime(s)\x1b[0m`);
  console.log('  Restart your harness and run: /dps-setup\n');
  rl.close();
}

main().catch((e) => { console.error(`\n✗ Error: ${e.message}`); process.exit(1); });
