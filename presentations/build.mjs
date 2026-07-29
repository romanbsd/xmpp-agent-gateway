#!/usr/bin/env node

import { existsSync } from "node:fs";
import {
  mkdir,
  mkdtemp,
  readFile,
  rm,
  writeFile,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const MARP_VERSION = "4.5.0";
const MERMAID_CLI_VERSION = "11.16.0";

const presentationDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(presentationDir, "..");
const source = join(presentationDir, "xmpp-agent-gateway-protoxep.md");
const assetsDir = join(presentationDir, "assets");
const distDir = join(presentationDir, "dist");
const slidesDir = join(distDir, "slides");

const diagrams = [
  "discover-and-delegate",
  "recover-and-interact",
];

function commandPath(command) {
  const result = spawnSync("sh", ["-c", `command -v ${command}`], {
    encoding: "utf8",
  });
  return result.status === 0 ? result.stdout.trim() : "";
}

function findBrowser() {
  const configured = process.env.CHROME || process.env.BROWSER_PATH;
  const candidates = [
    configured,
    commandPath("google-chrome"),
    commandPath("chromium"),
    commandPath("chromium-browser"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
  ].filter(Boolean);

  const found = candidates.find((candidate) => existsSync(candidate));
  if (!found) {
    throw new Error(
      "Chrome, Chromium, or Edge is required. Set CHROME or BROWSER_PATH to its executable.",
    );
  }
  return found;
}

function run(command, args) {
  const result = spawnSync(command, args, {
    cwd: repoRoot,
    stdio: "inherit",
  });
  if (result.status !== 0) {
    throw new Error(`${command} exited with status ${result.status}`);
  }
}

async function finalizeHtmlAssets(htmlPath) {
  const html = (await readFile(htmlPath, "utf8"))
    .replaceAll("./assets/", "../assets/");
  await writeFile(htmlPath, html);

  const references = new Set(
    [...html.matchAll(/\.\.\/assets\/([^"&)<]+)/g)]
      .map((match) => decodeURIComponent(match[1])),
  );
  const missing = [...references]
    .filter((asset) => !existsSync(join(assetsDir, asset)));

  if (missing.length > 0) {
    throw new Error(`HTML references missing assets: ${missing.join(", ")}`);
  }
}

async function main() {
  const browserPath = findBrowser();
  const scratchDir = await mkdtemp(join(tmpdir(), "xmpp-agent-gateway-deck-"));
  const puppeteerConfig = join(scratchDir, "puppeteer-config.json");

  await rm(distDir, { recursive: true, force: true });
  await mkdir(distDir, { recursive: true });
  await mkdir(slidesDir, { recursive: true });
  await writeFile(
    puppeteerConfig,
    `${JSON.stringify({
      executablePath: browserPath,
      args: ["--no-sandbox"],
    }, null, 2)}\n`,
  );

  try {
    for (const diagram of diagrams) {
      run("npx", [
        "--yes",
        `@mermaid-js/mermaid-cli@${MERMAID_CLI_VERSION}`,
        "-p",
        puppeteerConfig,
        "-i",
        join(assetsDir, `${diagram}.mmd`),
        "-o",
        join(assetsDir, `${diagram}.svg`),
        "-b",
        "transparent",
      ]);
    }

    const marp = [
      "--yes",
      `@marp-team/marp-cli@${MARP_VERSION}`,
      source,
      "--html",
      "--allow-local-files",
      "--browser-path",
      browserPath,
    ];

    run("npx", [...marp, "--pdf", "--pdf-outlines", "-o",
      join(distDir, "xmpp-agent-gateway-protoxep.pdf")]);
    run("npx", [...marp, "--pptx", "-o",
      join(distDir, "xmpp-agent-gateway-protoxep.pptx")]);
    const htmlOutput = join(distDir, "xmpp-agent-gateway-protoxep.html");
    run("npx", [...marp, "-o", htmlOutput]);
    await finalizeHtmlAssets(htmlOutput);
    run("npx", [...marp, "--images", "png", "--image-scale", "1", "-o",
      join(slidesDir, "slide.png")]);
  } finally {
    await rm(scratchDir, { recursive: true, force: true });
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
