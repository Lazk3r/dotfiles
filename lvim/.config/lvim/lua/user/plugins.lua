lvim.plugins = {
  "catppuccin/nvim",
  -- "j-hui/fidget.nvim",
  "karb94/neoscroll.nvim",
  "https://git.sr.ht/~whynothugo/lsp_lines.nvim",
  "is0n/jaq-nvim",
  {
    "0x100101/lab.nvim",
    build = "cd js && npm ci",
  },
  {
    'dccsillag/magma-nvim',
    build = ':UpdateRemotePlugins'
  },
}
