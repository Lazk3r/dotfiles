local opts = { noremap = true, silent = true }

lvim.leader = "space"
lvim.keys.normal_mode["<C-s>"] = ":w<cr>"
vim.keymap.set("i", "jk", "<esc>", opts)
vim.keymap.set("i", "kj", "<esc>", opts)
-- vim.keymap.set(
--   "",
--   "gn",
--   require("lsp_lines").toggle,
--   { desc = "Toggle lsp_lines" }
-- )