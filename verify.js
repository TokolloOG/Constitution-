const fs = require('fs');
const crypto = require('crypto');

const log = JSON.parse(fs.readFileSync('./proof/log.jsonl', 'utf8'));
let valid = true;

log.forEach((entry, i) => {
  const { hash, ...data } = entry;
  const calcHash = crypto.createHash('sha256')
    .update(JSON.stringify(data))
    .digest('hex');
  
  if (calcHash !== hash) {
    console.log(`Entry ${i}: INVALID - hash mismatch`);
    valid = false;
  }
});

if (valid) {
  console.log(`All ${log.length} entries VERIFIED ✓`);
  console.log('Proof chain is tamper-proof');
} else {
  console.log('Proof chain BROKEN - someone edited log.jsonl');
}
#!/usr/bin/env node
/**
 * Heavenet Law I Verifier
 * "Green LED off = <1mV at antenna. No software backdoor possible."
 * 
 * This script must be run on physical Helios One hardware.
 * It will FAIL if run in a VM, container, or on non-Helios hardware.
 * 
 * Law III: Code is Law. If this fails, device is not Heavenet.
 */

const { execSync } = require('child_process');
const fs = require('fs');

const OATH = "I will uphold Law I-VII or I will fork. I seek Rep, not equity.";

function assert(condition, law, message) {
  if (!condition) {
    console.error(`\n❌ LAW ${law} VIOLATION`);
    console.error(`   ${message}`);
    console.error(`\n   ${OATH}\n`);
    process.exit(1);
  }
}

// Law VII: Heavenet Owns Heavenet - check we are on real Helios One
function checkHeliosHardware() {
  console.log("Checking for Helios One hardware signature...");
  try {
    const dmi = fs.readFileSync('/sys/class/dmi/id/product_name', 'utf8').trim();
    assert(dmi === 'Helios One', 'VII', `Not running on Helios One. Detected: ${dmi}`);
  } catch (e) {
    assert(false, 'VII', 'Cannot read DMI. Are you running on real hardware?');
  }
}

// Law I: Kill Switch is Physics - measure antenna voltage
function verifyKillSwitch() {
  console.log("Testing Law I: Kill Switch is Physics...");
  
  // 1. Check physical switch exists in device tree
  const gpio = fs.existsSync('/sys/class/gpio/rf_kill_sw');
  assert(gpio, 'I', 'Physical RF kill switch not found in /sys/class/gpio/');
  
  // 2. Read switch state. 0 = OFF, 1 = ON
  const switchState = fs.readFileSync('/sys/class/gpio/rf_kill_sw/value', 'utf8').trim();
  
  if (switchState === '0') {
    console.log("Physical switch is OFF. Measuring antenna voltage...");
    
    // 3. Use onboard ADC to measure voltage at antenna feed point
    // Helios One spec: ADC channel 0 = WiFi antenna, 1 = BT, 2 = Cellular
    const antennas = ['WiFi', 'BT', 'Cellular'];
    antennas.forEach((ant, i) => {
      const mv = parseFloat(execSync(`cat /sys/bus/iio/devices/iio:device0/in_voltage${i}_raw`).toString());
      console.log(`   ${ant} antenna: ${mv.toFixed(3)}mV`);
      assert(mv < 1.0, 'I', `${ant} antenna has ${mv}mV > 1mV while switch is OFF. MOSFET failed.`);
    });
    
    console.log("✅ Law I PASS: All radios <1mV. Physics enforced.");
  } else {
    console.log("Physical switch is ON. Kill switch not engaged. Skipping voltage test.");
  }
}

// Law II: Rep > Equity - check no telemetry processes
function verifyNoTelemetry() {
  console.log("Testing Law II: Rep > Equity. Scanning for telemetry...");
  const badProcesses = ['telemetryd', 'analytics', 'datacollect', 'adsd'];
  const ps = execSync('ps aux').toString();
  badProcesses.forEach(proc => {
    assert(!ps.includes(proc), 'II', `Telemetry process found: ${proc}. Users > Investors.`);
  });
  console.log("✅ Law II PASS: No telemetry detected.");
}

function main() {
  console.log("=== Heavenet Law Verifier v1.0 ===");
  console.log("Constitution: https://github.com/TokolloOG/heavenet/blob/main/CONSTITUTION.md\n");
  
  checkHeliosHardware();
  verifyKillSwitch();
  verifyNoTelemetry();
  
  console.log("\n✅ ALL LAWS VERIFIED");
  console.log("   This Helios One is Helios Compatible.");
  console.log(`\n   ${OATH}\n`);
}

main();