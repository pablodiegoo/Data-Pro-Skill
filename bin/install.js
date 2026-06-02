#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise((r) => rl.question(q, r));
const ROOT = path.resolve(__dirname, '..');

const expand = (p) => p.startsWith('~') ? path.join(os.homedir(), p.slice(1)) : p;

const RUNTIMES = {
  opencode: {
    name: 'OpenCode',
    skillDir: '~/.config/opencode/skills',
    commandDir: '~/.config/opencode/command',
    needsCommandStubs: true,
    needsPerCommandSkills: false,
  },
  gemini: {
    name: 'Gemini CLI',
    skillDir: '~/.gemini/skills',
    commandDir: null,
    needsCommandStubs: false,
    needsPerCommandSkills: false,
    extraDirs: ['~/.gemini/antigravity/skills'],
  },
  codex: {
    name: 'Codex CLI',
    skillDir: '~/.codex/skills',
    commandDir: null,
    needsCommandStubs: false,
    needsPerCommandSkills: true,
  },
  antigravity: {
    name: 'Antigravity CLI',
    skillDir: '~/.antigravitycli/skills',
    commandDir: null,
    needsCommandStubs: false,
    needsPerCommandSkills: true,
  },
  copilot: {
    name: 'GitHub Copilot',
    skillDir: '~/.github/skills',
    commandDir: null,
    needsCommandStubs: false,
    needsPerCommandSkills: false,
  },
};

const DPS_COMMANDS = ['setup', 'cross', 'inject-open', 'export', 'clarify', 'plan'];
const DPS_MODES = ['mode:quant', 'mode:quali', 'mode:strategy'];

function copyFile(src, dst) {
  const dir = path.dirname(dst);
  fs.mkdirSync(dir, { recursive: true });
  fs.copyFileSync(src, dst);
}

async function installForRuntime(runtimeKey, runtime) {
  const skillBase = expand(runtime.skillDir);
  const targetDir = path.join(skillBase, 'data-pro-skill');

  console.log(`\n  → Installing to ${runtime.name} (${runtime.skillDir})`);

  // 1. Copy SKILL.md + constitution.md
  copyFile(path.join(ROOT, 'SKILL.md'), path.join(targetDir, 'SKILL.md'));
  copyFile(path.join(ROOT, 'constitution.md'), path.join(targetDir, 'constitution.md'));
  console.log('    ✓ SKILL.md + constitution.md');

  // 2. Extra directories (e.g. Gemini's antigravity)
  for (const extra of (runtime.extraDirs || [])) {
    const extraDir = path.join(expand(extra), 'data-pro-skill');
    copyFile(path.join(ROOT, 'SKILL.md'), path.join(extraDir, 'SKILL.md'));
    copyFile(path.join(ROOT, 'constitution.md'), path.join(extraDir, 'constitution.md'));
    console.log(`    ✓ ${extra}`);
  }

  // 3. Command stubs (OpenCode command/ directory)
  if (runtime.needsCommandStubs && runtime.commandDir) {
    const cmdDir = expand(runtime.commandDir);
    for (const cmd of [...DPS_COMMANDS, ...DPS_MODES]) {
      const filePath = path.join(cmdDir, `dps-${cmd}.md`);
      const nameline = cmd.includes(':') ? `dps-${cmd}` : `dps-${cmd}`;
      const desc = cmd.includes(':')
        ? `Activate ${cmd.split(':')[1]} persona`
        : `Data-Pro-Skill /dps-${cmd}`;
      fs.mkdirSync(cmdDir, { recursive: true });
      fs.writeFileSync(filePath, `---
description: "${desc}"
---

Read Data-Pro-Skill instructions and execute \`/dps-${cmd}\`.

@${targetDir}/SKILL.md
@${targetDir}/constitution.md
`);
    }
    console.log(`    ✓ ${DPS_COMMANDS.length + DPS_MODES.length} command stubs`);
  }

  // 4. Per-command skill directories (Codex, Antigravity, Gemini)
  if (runtime.needsPerCommandSkills) {
    const allCmds = [...DPS_COMMANDS, ...DPS_MODES];
    for (const cmd of allCmds) {
      const skillDir = path.join(skillBase, `dps-${cmd}`);
      const skillMd = path.join(skillDir, 'SKILL.md');
      fs.mkdirSync(skillDir, { recursive: true });
      fs.writeFileSync(skillMd, `---
name: dps-${cmd}
description: "Data-Pro-Skill: /dps-${cmd}"
---

Execute \`/dps-${cmd}\` as defined in the Data-Pro-Skill meta-prompt.

Read full instructions:
@${targetDir}/SKILL.md
@${targetDir}/constitution.md
`);
    }
    console.log(`    ✓ ${allCmds.length} command skills`);
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

  const runtimes = (idx >= keys.length)
    ? Object.entries(RUNTIMES)
    : [[keys[idx] || 'opencode', RUNTIMES[keys[idx] || 'opencode']]];

  for (const [key, rt] of runtimes) {
    await installForRuntime(key, rt);
  }

  console.log(`\n\x1b[32m✓ Data-Pro-Skill v2 installed to ${runtimes.length} runtime(s)\x1b[0m`);
  console.log('  Restart your harness and run: /dps-setup\n');
  rl.close();
}

main().catch((e) => { console.error(e); process.exit(1); });
