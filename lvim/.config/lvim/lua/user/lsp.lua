lvim.builtin.treesitter.ensure_installed = {
  "bash",
  "c",
  "javascript",
  "json",
  "lua",
  "python",
  "typescript",
  "tsx",
  "css",
  "rust",
  "java",
  "yaml",
}

lvim.builtin.treesitter.ignore_install = { "haskell" }
lvim.builtin.treesitter.highlight.enable = true

local status_ok, lsp_lines = pcall(require, "lsp_lines")
if not status_ok then
  return
end

lsp_lines.setup()
vim.diagnostic.config({ virtual_lines = false })

-- local formatters = require "lvim.lsp.null-ls.formatters"
-- formatters.setup {
--   { command = "autopep8", filetypes = { "python" } },
--   {
--     command = "prettier",
--     extra_args = { "--single-quote", "--jsx-single-quote" },
--     filetypes = { "html", "css", "javascript", "javascriptreact", "typescript", "typescriptreact", "vue" },
--   },
-- }

-- local linters = require "lvim.lsp.null-ls.linters"
-- linters.setup {
--   { command = "flake8", filetypes = { "python" } },
--   -- { command = "eslint", filetypes = { "html", "css", "javascript", "javascriptreact", "typescript", "typescriptreact", "vue" } },
-- }

-- vim.list_extend(lvim.lsp.automatic_configuration.skipped_servers, { "arduino_language_server" })

-- require("lvim.lsp.manager").setup("arduino_language_server", {
--   cmd = {
--     "arduino-language-server",
--     "-cli-config", "/path/to/arduino-cli.yaml",
--     "-fqbn", "arduino:avr:uno",
--     "-cli", "arduino-cli",
--     "-clangd", "clangd"
--   }
-- })
