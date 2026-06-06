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