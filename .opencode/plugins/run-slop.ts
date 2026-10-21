import { spawn } from "node:child_process";
import { Plugin } from "@opencode/plugin";

export default Plugin.define({
  id: "sloperator.run-slop",
  setup: async (ctx) => {
    await ctx.tool.transform((tools) => {
      tools.add({
        name: "run_slop",
        description: "Run a SlopLang file with sloperator and return its output and exit code",
        input: {
          type: "object",
          properties: {
            filepath: { type: "string", description: "Path to the .slop file to run" },
          },
          required: ["filepath"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input, context) => {
          const { filepath } = input as { filepath: string };
          const result = await new Promise<{ stdout: string; stderr: string; exitCode: number }>(
            (resolve, reject) => {
              const child = spawn("uv", ["run", "--no-active", "sloperator.py", filepath], {
                cwd: ctx.location.project.canonical,
                signal: context.signal,
              });
              let stdout = "";
              let stderr = "";
              child.stdout.setEncoding("utf8");
              child.stderr.setEncoding("utf8");
              child.stdout.on("data", (chunk: string) => (stdout += chunk));
              child.stderr.on("data", (chunk: string) => (stderr += chunk));
              child.on("error", reject);
              child.on("close", (exitCode) => {
                resolve({ stdout, stderr, exitCode: exitCode ?? 1 });
              });
            },
          );
          return { content: JSON.stringify(result) };
        },
      });
    });
  },
});
