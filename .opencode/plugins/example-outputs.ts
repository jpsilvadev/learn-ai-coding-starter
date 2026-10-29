import { spawn } from "node:child_process";
import { readdir } from "node:fs/promises";
import { join } from "node:path";
import { Plugin } from "@opencode/plugin";

export default Plugin.define({
  id: "sloperator.example-outputs",
  setup: async (ctx) => {
    const root = ctx.location.project.canonical;
    await ctx.tool.transform((tools) => {
      tools.add({
        name: "example_outputs",
        description:
          "Run every examples/*.slop file and return each file's name, exit code, and first line of output",
        input: {
          type: "object",
          properties: {},
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (_input, context) => {
          const files = (await readdir(join(root, "examples")))
            .filter((file) => file.endsWith(".slop"))
            .sort();
          const examples = [];
          for (const name of files) {
            const result = await new Promise<{ stdout: string; exitCode: number }>(
              (resolve, reject) => {
                const child = spawn(
                  "uv",
                  ["run", "--no-active", "sloperator.py", join("examples", name)],
                  { cwd: root, signal: context.signal },
                );
                let stdout = "";
                child.stdout.setEncoding("utf8");
                child.stdout.on("data", (chunk: string) => (stdout += chunk));
                child.on("error", reject);
                child.on("close", (exitCode) => resolve({ stdout, exitCode: exitCode ?? 1 }));
              },
            );
            const firstLine = result.stdout.split("\n")[0].replace(/\r$/, "");
            examples.push({ name, exitCode: result.exitCode, firstLine });
          }
          return { content: JSON.stringify({ examples }) };
        },
      });
    });
  },
});
