const knownPlaintext = "This is a known message!";
const knownCiphertext = "a469b1c502c1cab966965e50425438e1bb1b5f9037a4c159";
const unknownCiphertext = "bf73bcd3509299d566c35b5d450337e1bb175f903fafc159";

// Convert the known plaintext and ciphertext to binary
const knownPlaintextBinary = hexToBinary(asciiToHex(knownPlaintext));
const knownCiphertextBinary = hexToBinary(knownCiphertext);

// XOR the known plaintext and ciphertext to get the keystream
const keystreamBinary = xor(knownPlaintextBinary, knownCiphertextBinary);

// Convert the keystream to hexadecimal
const keystreamHex = binaryToHex(keystreamBinary);

// Convert the unknown ciphertext to binary
const unknownCiphertextBinary = hexToBinary(unknownCiphertext);

// XOR the keystream and the unknown ciphertext to get the unknown plaintext
const unknownPlaintextBinary = xor(keystreamBinary, unknownCiphertextBinary);

// Convert the unknown plaintext to ASCII
const unknownPlaintext = hexToAscii(binaryToHex(unknownPlaintextBinary));

// Output the unknown plaintext
console.log("run")
console.log(unknownPlaintext);

// Helper functions
function hexToBinary(hex) {
  return hex.split("").map((c) => parseInt(c, 16).toString(2).padStart(4, "0")).join("");
}

function binaryToHex(binary) {
  return binary.match(/.{1,4}/g).map((b) => parseInt(b, 2).toString(16)).join("");
}

function asciiToHex(ascii) {
  return ascii.split("").map((c) => c.charCodeAt(0).toString(16)).join("");
}

function hexToAscii(hex) {
  return hex.match(/.{1,2}/g).map((h) => String.fromCharCode(parseInt(h, 16))).join("");
}

function xor(a, b) {
  return a.split("").map((c, i) => (c === b[i] ? "0" : "1")).join("");
}
