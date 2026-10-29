import { appendFile, mkdir } from "node:fs/promises";
import { join } from "node:path";
import { Plugin } from "@opencode/plugin";

const LOGGED_TOOLS = new Set(["edit", "write", "patch", "apply_patch"]);

export default Plugin.define({
  id: "sloperator.edit-log",
  setup: async (ctx) => {
    const logDir = join(ctx.location.project.canonical, "logs");
    const logPath = join(logDir, "plugin-tools.log");
    await ctx.tool.hook("execute.after", async (input) => {
      if (input.status !== "completed" || !LOGGED_TOOLS.has(input.tool)) return;
      await mkdir(logDir, { recursive: true });
      await appendFile(logPath, `${JSON.stringify({ tool: input.tool, status: "completed" })}\n`);
    });
  },
});
