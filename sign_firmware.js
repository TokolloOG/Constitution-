#!/usr/bin/env node
/**
 * Heavenet Firmware Signer v0.1
 * Law VII: Heavenet Owns Heavenet. 7-of-12 required.
 *
 * Usage: node sign_firmware.js firmware/helios-v0.1.bin
 * 
 * Creates signature file proving you, with Rep, approve this binary.
 * Law III: If 7 sigs aren't in repo, firmware cannot ship.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const crypto = require('crypto');

const HEAVENET_ROOT = path.resolve(__dirname);
const OATH = "I will uphold Law I-VII or I will fork. I seek Rep, not equity.";

function sha256(filePath) {
    const data = fs.readFileSync(filePath);
    return crypto.createHash('sha256').update(data).digest('hex');
}

function getIdentity() {
    const oathPath = path.join(HEAVENET_ROOT, '.heavenet/oath.json');
    if (!fs.existsSync(oathPath)) {
        console.error("❌ Law II violation: Run node oath.js first. No identity.");
        process.exit(1);
    }
    return JSON.parse(fs.readFileSync(oathPath));
}

function signFile(filePath, privkeyPath) {
    const hash = sha256(filePath);
    const signature = execSync(
        `ssh-keygen -Y sign -f ${privkeyPath} -n heavenet`,
        { input: hash, encoding: 'utf8' }
    );
    return { hash, signature };
}

function main() {
    const firmwarePath = process.argv[2];
    if (!firmwarePath || !fs.existsSync(firmwarePath)) {
        console.log("Usage: node sign_firmware.js <firmware.bin>");
        console.log("Law VII: 7-of-12 signatures required to ship.");
        process.exit(1);
    }

    console.log("=== Heavenet Firmware Signer v0.1 ===");
    console.log(`Target: ${firmwarePath}`);

    const identity = getIdentity();
    const privkey = path.join(HEAVENET_ROOT, '.heavenet/id_ed25519');
    
    console.log(`Signer: ${identity.pubkey.substring(0,16)}... | Rep: ${identity.rep}`);
    
    if (identity.rep < 100) {
        console.log(`❌ Law II: Rep ${identity.rep} < 100. Earn Rep before signing firmware.`);
        process.exit(1);
    }

    const { hash, signature } = signFile(firmwarePath, privkey);

    const sigData = {
        oath: OATH,
        pubkey: identity.pubkey,
        rep: identity.rep,
        firmware: path.basename(firmwarePath),
        sha256: hash,
        signature: signature,
        timestamp: new Date().toISOString(),
        laws: "I-VII"
    };

    const sigDir = path.join(HEAVENET_ROOT, 'firmware/signatures');
    fs.mkdirSync(sigDir, { recursive: true });
    
    const sigPath = path.join(sigDir, `${identity.pubkey.substring(0,16)}.json`);
    fs.writeFileSync(sigPath, JSON.stringify(sigData, null, 2));

    console.log(`\n✅ SIGNED`);
    console.log(` SHA256: ${hash}`);
    console.log(` Signature: ${sigPath}`);
    console.log(`\n Law VII: Need 6 more signatures to ship.`);
    console.log(` Others run: node proof.js ${sigPath}`);
}

main();