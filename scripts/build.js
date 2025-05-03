import { build } from "esbuild";
import alias from "esbuild-plugin-alias";
import fs from "fs";
import path from "path";

const result = await build({
    entryPoints: ["src/main/main.ts"],
    bundle: true,
    platform: "node",
    format: "esm",
    outfile: "dist/main.js",
    plugins: [
        alias({
            "@main": path.join(import.meta.dirname, "..", "src", "main"),
            "@test": path.join(import.meta.dirname, "..", "src", "test"),
        })
    ]
});

const shebang = "#!/usr/bin/env node\n";
const file = fs.readFileSync("dist/main.js", "utf8");
fs.writeFileSync("dist/main.js", shebang + file);
