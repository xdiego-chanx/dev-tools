import { build } from "esbuild";
import fs from "fs";

const result = await build({
  entryPoints: ["src/main/main.ts"],
  bundle: true,
  platform: "node",
  format: "esm",
  outfile: "dist/main.js"
});

const shebang = "#!/usr/bin/env node\n";
const file = fs.readFileSync("dist/main.js", "utf8");
fs.writeFileSync("dist/main.js", shebang + file);
