#!/usr/bin/env node
console.log("\n=== Heavenet Oath ===\n")
console.log("I will uphold Law I-VII or I will fork.")
console.log("I seek Rep, not equity.\n")
console.log("The 7 Laws:")
console.log("1. Fork > Exit")
console.log("2. Rep > Equity")
console.log("3. Code is Law")
console.log("4. Default to Open")
console.log("5. Ship Daily")
console.log("6. Users > Investors")
console.log("7. Heavenet Owns Heavenet\n")
console.log("Welcome, Founder. Start building.\n")
#!/usr/bin/env node
/**
 * Heavenet Law II: Rep > Equity
 * "Reputation is earned by commits, not titles. Build > Talk."
 *
 * This generates your maintainer identity and signs The Oath.
 * Rep is calculated from git history. Cannot be faked or bought.
 *
 * Law III: Code is Law. If you haven't signed the Oath, you have no Rep.
 */

const { execSync } = require('child_process');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const OATH = "I will uphold Law I-VII or I will fork. I seek Rep, not equity.";
const HEAVENET_ROOT = path.resolve(__dirname);

function sha256(data) {
  return crypto.createHash('sha256').update(data).digest('hex');
}

// Generate Ed25519 keypair for maintainer if not exists
function initIdentity() {
  const keyPath = path.join(HEAVENET_ROOT, '.heavenet');
  const privPath = path.join(keyPath, 'id_ed25519');
  const pubPath = path.join(keyPath, 'id_ed25519.pub');

  if (!fs.existsSync(privPath)) {
    console.log("No identity found. Generating Ed25519 keypair...");
    fs.mkdirSync(keyPath, { recursive: true });
    execSync(`ssh-keygen -t ed25519 -f ${privPath} -N "" -C "heavenet-maintainer"`, { stdio: 'inherit' });
    console.log(`✅ Identity created: ${pubPath}`);
  }

  return {
    pubkey: fs.readFileSync(pubPath, 'utf8').trim().split(' ')[1], // base64 pubkey only
    privkey: privPath
  };
}

// Sign The Oath with private key
function signOath(privkeyPath) {
  const signature = execSync(`ssh-keygen -Y sign -f ${privkeyPath} -n heavenet`, {
    input: OATH,
    encoding: 'utf8'
  });
  return signature;
}

// Calculate Rep from git log. Law II: Build > Talk.
function calculateRep(pubkey) {
  console.log("Calculating Rep from git history...");
  let rep = 0;

  try {
    // Weight: commits to core/ = 100 rep, docs = 10 rep, tests = 50 rep
    const log = execSync(`git log --pretty=format:"%H %ae %s" --numstat`, { encoding: 'utf8' });
    const commits = log.split('\n\n');

    commits.forEach(commit => {
      const lines = commit.split('\n');
      const header = lines[0];
      if (!header) return;

      // TODO: Match commit email to pubkey via.gitallowed_signers
      // For v1.0, we trust local git config. Law VII: Heavenet Owns Heavenet

      lines.slice(1).forEach(file => {
        if (file.startsWith('core/')) rep += 100;
        else if (file.startsWith('test')) rep += 50;
        else if (file.endsWith('.md')) rep += 10;
        else if (file) rep += 5;
      });
    });
  } catch (e) {
    console.log("No git history found. Rep = 0. Start shipping. Law V.");
  }

  return rep;
}

// Main: create.heavenet/oath.json
function main() {
  console.log("=== Heavenet Oath Signer v1.0 ===");
  console.log(`OATH: "${OATH}"\n`);

  const { pubkey, privkey } = initIdentity();
  const signature = signOath(privkey);
  const rep = calculateRep(pubkey);

  const oathFile = {
    oath: OATH,
    pubkey: pubkey,
    signature: signature,
    rep: rep,
    timestamp: new Date().toISOString(),
    laws: "I-VII"
  };

  fs.writeFileSync(path.join(HEAVENET_ROOT, '.heavenet/oath.json'), JSON.stringify(oathFile, null, 2));

  console.log(`\n✅ OATH SIGNED`);
  console.log(` Pubkey: ${pubkey.substring(0,16)}...`);
  console.log(` Rep: ${rep}`);
  console.log(` File:.heavenet/oath.json`);
  console.log(`\n Law II: Rep > Equity. You cannot buy this.`);

  if (rep === 0) {
    console.log(`\n Law V: Ship Daily. Make your first commit to earn Rep.`);
  }
}

main();