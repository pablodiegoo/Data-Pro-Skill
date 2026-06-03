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
const LOCAL = { name: 'Local project (current directory)', local: true };

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
  console.log('Select destination(s):\n');
  keys.forEach((k, i) => console.log(`  ${i + 1}. ${RUNTIMES[k].name}`));
  console.log(`  ${keys.length + 1}. All of the above`);
  console.log(`  0. Local project (current dir)`);

  const ans = await ask(`\nEnter number(s) [1]: `);
  const nums = (ans || '1')
    .split(/[,;\s]+/)
    .map(s => parseInt(s, 10))
    .filter(n => !isNaN(n));

  const hasAll = nums.some(n => n === keys.length + 1);
  const hasLocal = nums.some(n => n === 0);
  const harnessNums = nums.filter(n => n >= 1 && n <= keys.length);

  const list = [];
  if (hasAll) {
    Object.entries(RUNTIMES).forEach(([k, v]) => list.push([k, v]));
  } else {
    [...new Set(harnessNums)].forEach(n => list.push([keys[n - 1], RUNTIMES[keys[n - 1]]]));
  }
  if (hasLocal) list.push(['local', LOCAL]);

  for (const [, rt] of list) {
    if (rt.local) {
      const cwd = process.cwd();
      const { execSync } = require('child_process');
      console.log(`\n  → Installing Data-Pro-Skill in current project (${cwd})`);
      const dir = path.join(cwd, '.dps');
      if (fs.existsSync(dir)) {
        console.log('    ⚠ .dps/ already exists — run: git -C .dps pull origin main');
        continue;
      }
      execSync(
        `git clone --depth 1 https://github.com/pablodiegoo/Data-Pro-Skill.git "${dir}" 2>&1`,
        { stdio: 'inherit' }
      );
      console.log('    ✓ .dps/ cloned');

      // Reference in AGENTS.md
      const agentsPath = path.join(cwd, 'AGENTS.md');
      const ref = `\n<!-- DPS:project-start -->\n- @.dps/SKILL.md\n- @.dps/constitution.md\n<!-- DPS:project-end -->\n`;
      if (fs.existsSync(agentsPath)) {
        if (!fs.readFileSync(agentsPath, 'utf-8').includes('DPS:project-start')) {
          fs.appendFileSync(agentsPath, ref);
          console.log('    ✓ AGENTS.md updated');
        }
      } else {
        fs.writeFileSync(agentsPath, ref);
        console.log('    ✓ AGENTS.md created');
      }
      continue;
    }
    const skillBase = path.join(expand(rt.dir), 'skills');
    await installForRuntime(rt, skillBase);
  }

  const harnessCount = list.filter(([, r]) => !r.local).length;
  const hasLocalInstall = list.some(([, r]) => r.local);
  console.log(`\n\x1b[32m✓ Data-Pro-Skill v2 installed\x1b[0m`);
  if (harnessCount > 0) console.log(`  ${harnessCount} harness(es) — restart and run: /dps-setup`);
  if (hasLocalInstall) console.log(`  Local project — run: /dps-setup`);
  rl.close();
}

main().catch((e) => { console.error(`\n✗ Error: ${e.message}`); process.exit(1); });
