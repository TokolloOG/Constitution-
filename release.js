#!/usr/bin/env node
/**
 * Heavenet Release v0.1
 * Law VII: Heavenet Owns Heavenet. 7-of-12 to release.
 *
 * Verifies firmware signatures and updates manifest.json
 * Once manifest.json is committed, that firmware is official.
 *
 * Law III: Code is Law. If not in manifest, devices reject it.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const MANIFEST = 'manifest.json';
const OATH = "I will uphold Law I-VII or I will fork. I seek Rep, not equity.";

function verifySigs(firmwarePath) {
    const sigDir = path.join('firmware', 'signatures');
    const sigs = fs.readdirSync(sigDir).map(f => path.join(sigDir, f));

    let validSigs = [];
    let totalRep = 0;

    console.log(`Verifying ${sigs.length} signatures for ${firmwarePath}...`);

    sigs.forEach(sigFile => {
        try {
            execSync(`node proof.js ${sigFile}`, { stdio: 'pipe' });
            const data = JSON.parse(fs.readFileSync(sigFile));
            validSigs.push({
                pubkey: data.pubkey,
                rep: data.rep,
                timestamp: data.timestamp
            });
            totalRep += data.rep;
            console.log(` ✅ ${data.pubkey.substring(0,8)}... Rep: ${data.rep}`);
        } catch (e) {
            console.log(` ❌ ${sigFile} invalid`);
        }
    });

    return { validSigs, totalRep };
}

function updateManifest(version, firmwarePath, sha256) {
    const manifest = JSON.parse(fs.readFileSync(MANIFEST));
    const { validSigs, totalRep } = verifySigs(firmwarePath);

    if (validSigs.length < 7) {
        console.error(`\n❌ Law VII violation: Only ${validSigs.length}/7 valid signatures.`);
        process.exit(1);
    }

    if (totalRep < 7000) {
        console.error(`\n❌ Law VII violation: Total Rep ${totalRep} < 7000.`);
        process.exit(1);
    }

    const release = {
        version,
        date: new Date().toISOString().split('T')[0],
        sha256,
        file: firmwarePath,
        min_rep_to_run: 0,
        required_signatures: 7,
        signatures: validSigs,
        total_rep: totalRep,
        notes: "Law VII: Approved by 7-of-12 maintainer multisig.",
        status: "RELEASED"
    };

    // Update manifest
    manifest.devices["Helios One"].current = version;
    manifest.devices["Helios One"].releases[0] = release;

    fs.writeFileSync(MANIFEST, JSON.stringify(manifest, null, 2));

    console.log(`\n✅ LAW VII PASS`);
    console.log(` Version: ${version}`);
    console.log(` Signatures: ${validSigs.length}/7`);
    console.log(` Total Rep: ${totalRep}`);
    console.log(` SHA256: ${sha256}`);
    console.log(`\n Commit manifest.json. This firmware is now official.`);
    console.log(` ${OATH}`);
}

function main() {
    const [version, firmwarePath] = process.argv.slice(2);

    if (!version ||!firmwarePath) {
        console.log("Usage: node release.js <version> <firmware.bin>");
        console.log("Ex: node release.js 0.1.0 firmware/helios-v0.1.0.bin");
        process.exit(1);
    }

    const sha256 = execSync(`sha256sum ${firmwarePath}`).toString().split(' ')[0];
    updateManifest(version, firmwarePath, sha256);
}

main();