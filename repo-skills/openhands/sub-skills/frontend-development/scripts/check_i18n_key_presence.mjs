#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const usage = `Usage: node check_i18n_key_presence.mjs --translation <translation.json> --declaration <declaration.ts> --key <I18N_KEY>

Checks that one i18n key exists in both an OpenHands translation JSON file and generated declaration file.

Options:
  --translation  Path to translation.json
  --declaration  Path to declaration.ts
  --key          Key to check, for example SETTINGS$SAVE_CHANGES
  --help         Show this help message
`;

const parseArgs = (argv) => {
  const args = {};

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];

    if (arg === "--help" || arg === "-h") {
      args.help = true;
      continue;
    }

    if (!["--translation", "--declaration", "--key"].includes(arg)) {
      throw new Error(`Unknown option: ${arg}`);
    }

    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      throw new Error(`Missing value for ${arg}`);
    }

    args[arg.slice(2)] = value;
    index += 1;
  }

  return args;
};

const readTextFile = (filePath, label) => {
  const resolvedPath = path.resolve(filePath);

  try {
    return fs.readFileSync(resolvedPath, "utf8");
  } catch (error) {
    throw new Error(`Unable to read ${label} at ${filePath}: ${error.message}`);
  }
};

const escapeRegExp = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

const main = () => {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    process.stdout.write(usage);
    return;
  }

  const missing = ["translation", "declaration", "key"].filter(
    (name) => !args[name],
  );

  if (missing.length > 0) {
    throw new Error(`Missing required option(s): ${missing.join(", ")}\n\n${usage}`);
  }

  const translationText = readTextFile(args.translation, "translation file");
  let translations;

  try {
    translations = JSON.parse(translationText);
  } catch (error) {
    throw new Error(`Invalid translation JSON: ${error.message}`);
  }

  const hasTranslationKey = Object.prototype.hasOwnProperty.call(
    translations,
    args.key,
  );

  const declarationText = readTextFile(args.declaration, "declaration file");
  const escapedKey = escapeRegExp(args.key);
  const declarationPattern = new RegExp(
    `(^|\\s)${escapedKey}\\s*=\\s*["']${escapedKey}["']`,
    "m",
  );
  const hasDeclarationKey = declarationPattern.test(declarationText);

  if (!hasTranslationKey || !hasDeclarationKey) {
    if (!hasTranslationKey) {
      process.stderr.write(`Missing translation key: ${args.key}\n`);
    }
    if (!hasDeclarationKey) {
      process.stderr.write(`Missing declaration key: ${args.key}\n`);
    }
    process.exitCode = 1;
    return;
  }

  process.stdout.write(`Found i18n key in translation and declaration: ${args.key}\n`);
};

try {
  main();
} catch (error) {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
}
