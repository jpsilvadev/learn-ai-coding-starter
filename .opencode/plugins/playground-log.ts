import { appendFile, mkdir } from "node:fs/promises";
import { join } from "node:path";
import { Plugin } from "@opencode/plugin";

export default Plugin.define({
  id: "sloperator.playground-log",
  setup: async (ctx) => {
    const logDir = join(ctx.location.project.canonical, "logs");
    const logPath = join(logDir, "plugin-playground.log");
    await ctx.shell.hook("create.before", async (input) => {
      if (!input.command.includes("playground/server.py")) return;
      await mkdir(logDir, { recursive: true });
      await appendFile(logPath, `${new Date().toISOString()} playground shell request\n`);
    });
  },
});
