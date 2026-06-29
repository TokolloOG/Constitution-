const { ethers } = require("ethers");
const fs = require("fs");

if (!fs.existsSync("./keys")) fs.mkdirSync("./keys");

for (let i = 1; i <= 7; i++) {
  const wallet = ethers.Wallet.createRandom();
  const privKey = wallet.privateKey;
  const address = wallet.address;

  fs.writeFileSync(`./keys/signer_${i}.key`, privKey);
  console.log(`Signer ${i}:`);
  console.log(`  Address: ${address}`);
  console.log(`  Saved to: ./keys/signer_${i}.key\n`);
}