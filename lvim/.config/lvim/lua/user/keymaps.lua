local opts = { noremap = true, silent = true }

lvim.leader = "space"
lvim.keys.normal_mode["<C-s>"] = ":w<cr>"
vim.keymap.set("i", "jk", "<esc>", opts)
vim.keymap.set("i", "kj", "<esc>", opts)
vim.keymap.set(
  "",
  "gn",
  require("lsp_lines").toggle,
  { desc = "Toggle lsp_lines" }
)
vim.keymap.set("n", "<m-r>", ":silent only | Jaq<cr>", opts)
vim.keymap.set("n", "<m-4>", ":Lab code run<cr>", opts)
vim.keymap.set("n", "<m-5>", ":Lab code stop<cr>", opts)
vim.keymap.set("n", "<m-6>", ":Lab code panel<cr>", opts)
