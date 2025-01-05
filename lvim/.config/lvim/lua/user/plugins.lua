lvim.plugins = {
  "catppuccin/nvim",
  "karb94/neoscroll.nvim",
  {
    "scalameta/nvim-metals",
    config = function()
      require("user.metals").config()
    end,
  },
}
