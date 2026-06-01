#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise((r) => rl.question(q, r));

const ROOT = path.resolve(__dirname, '..');

const RUNTIMES = {
  opencode: { name: 'OpenCode', skillDir: ['~/.config/opencode/skills'] },
  claude: { name: 'Claude Code', skillDir: ['~/.claude/skills'] },
  gemini: { name: 'Gemini CLI', skillDir: ['~/.gemini/skills'] },
  codex: { name: 'Codex CLI', skillDir: ['~/.codex/skills'] },
};

function expand(p) {
  return p.startsWith('~') ? path.join(os.homedir(), p.slice(1)) : p;
}

async function install() {
  console.log(`
\x1b[36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Data-Pro-Skill v2 — Installer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m
`);
  console.log('Select your AI harness:\n');
  const keys = Object.keys(RUNTIMES);
  keys.forEach((k, i) => console.log(`  ${i + 1}. ${RUNTIMES[k].name}`));

  const ans = await ask(`\nEnter number [1]: `);
  const idx = parseInt(ans || '1', 10) - 1;
  const runtime = keys[idx] || 'opencode';
  const cfg = RUNTIMES[runtime];

  const skillBase = expand(cfg.skillDir[0]);
  const targetDir = path.join(skillBase, 'data-pro-skill');

  console.log(`\n\x1b[2mInstalling to: ${targetDir}\x1b[0m\n`);

  // Create target
  fs.mkdirSync(targetDir, { recursive: true });

  // Copy core files
  const copyFiles = ['SKILL.md', 'constitution.md'];
  for (const f of copyFiles) {
    const src = path.join(ROOT, f);
    const dst = path.join(targetDir, f);
    if (!fs.existsSync(src)) { console.log(`  ⚠ ${f} not found`); continue; }
    fs.copyFileSync(src, dst);
    console.log(`  \x1b[32m✓\x1b[0m ${f}`);
  }

  // Copy agents
  const agentsDir = path.join(ROOT, 'agents');
  if (fs.existsSync(agentsDir)) {
    const agentFiles = fs.readdirSync(agentsDir).filter(f => f.endsWith('.md'));
    for (const f of agentFiles) {
      fs.copyFileSync(path.join(agentsDir, f), path.join(targetDir, f));
    }
    console.log(`  \x1b[32m✓\x1b[0m ${agentFiles.length} agent(s)`);
  }

  console.log(`\n\x1b[32m✓ Data-Pro-Skill v2 installed to ${runtime}\x1b[0m`);
  console.log(`  Restart ${cfg.name} and run: /dps-setup\n`);
  rl.close();
}

install().catch((e) => { console.error(e); process.exit(1); });
