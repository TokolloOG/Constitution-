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
/**
 * Generate keypair using TweetNaCl
 * Outputs keypair to console only (no file writes)
 */

const nacl = require('tweetnacl');
const bs58 = require('bs58');

function generateKeypair() {
  // Generate a new keypair
  const keypair = nacl.box.keyPair();
  
  // Encode to base58 for readability
  const publicKeyB58 = bs58.encode(Buffer.from(keypair.publicKey));
  const secretKeyB58 = bs58.encode(Buffer.from(keypair.secretKey));
  
  return {
    publicKey: publicKeyB58,
    secretKey: secretKeyB58,
    publicKeyRaw: keypair.publicKey,
    secretKeyRaw: keypair.secretKey,
  };
}

function main() {
  console.log('Generating TweetNaCl keypair...\n');
  
  const keypair = generateKeypair();
  
  console.log('=== Generated Keypair ===');
  console.log('Public Key (Base58):');
  console.log(keypair.publicKey);
  console.log('\nSecret Key (Base58):');
  console.log(keypair.secretKey);
  console.log('\n⚠️  NEVER share your secret key!\n');
}

main();
/**
 * HeavenET Key Generator
 * Uses TweetNaCl to generate keypair
 * Outputs to console only (no file writes)
 * All keys are base58 encoded for readability
 */

const nacl = require('tweetnacl');
const bs58 = require('bs58');

/**
 * Generate a new keypair using TweetNaCl
 * @returns {Object} Object with public and secret keys in base58
 */
function generateKeypair() {
  // Generate a new box keypair (encryption)
  const keypair = nacl.box.keyPair();

  // Encode to base58 for safe string representation
  const publicKeyB58 = bs58.encode(Buffer.from(keypair.publicKey));
  const secretKeyB58 = bs58.encode(Buffer.from(keypair.secretKey));

  return {
    publicKey: publicKeyB58,
    secretKey: secretKeyB58,
    publicKeyRaw: keypair.publicKey,
    secretKeyRaw: keypair.secretKey,
  };
}

/**
 * Main execution
 */
function main() {
  console.log('\n========================================');
  console.log('🔑 HeavenET Key Generator');
  console.log('========================================\n');

  try {
    const keypair = generateKeypair();

    console.log('✅ Keypair generated successfully\n');

    console.log('PUBLIC_KEY (base58):');
    console.log(keypair.publicKey);
    console.log();

    console.log('PRIVATE_KEY (base58):');
    console.log(keypair.secretKey);
    console.log();

    console.log('========================================');
    console.log('⚠️  IMPORTANT SECURITY WARNINGS:');
    console.log('========================================');
    console.log('• NEVER commit private keys to git');
    console.log('• NEVER share private keys with anyone');
    console.log('• Store private keys in secure vaults only');
    console.log('• Use environment variables in production');
    console.log('• This output is NOT saved to any file\n');

  } catch (error) {
    console.error('❌ Error generating keypair:', error.message);
    process.exit(1);
  }
}

main();