// game_operator.js
"use strict";

const SHIFTED_HEX_CHARS = "abcdefghijklmnop";

function bytesToShiftedHex(bytes) {
  let hex = "";
  for (let i = 0; i < bytes.length; i++) {
    hex += SHIFTED_HEX_CHARS[bytes[i] >> 4] + SHIFTED_HEX_CHARS[bytes[i] & 15];
  }
  return hex.toUpperCase();
}

function bytes32ToString(bytes) {
  const hex = bytesToShiftedHex(bytes);
  const buffer = new Uint8Array(32);
  const view = new DataView(buffer.buffer, 0);
  let s = "";

  for (let i = 0; i < bytes.length; i++) {
    view.setUint8(
      i,
      ((hex.charCodeAt(i << 1) - "A".charCodeAt(0)) << 4) |
        (hex.charCodeAt((i << 1) + 1) - "A".charCodeAt(0)),
      true
    );
  }
  for (let i = 0; i < 4; i++) {
    for (let j = 0; j < 14; j++) {
      s += String.fromCharCode(
        Number(
          (view.getBigUint64(i * 8, true) % 26n) + BigInt("A".charCodeAt(0))
        )
      );
      view.setBigUint64(i * 8, view.getBigUint64(i * 8, true) / 26n, true);
    }
  }
  return s.toUpperCase();
}

const inputBytes = process.argv.slice(2).map(Number);
const outputString = bytes32ToString(inputBytes);
console.log(outputString);
