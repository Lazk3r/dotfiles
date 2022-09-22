require('packer').startup(function()
  use 'wbthomason/packer.nvim'

  -- Theme
  use 'navarasu/onedark.nvim'
  -- Nvim-Tree
  use {
      'kyazdani42/nvim-tree.lua',
      requires = 'kyazdani42/nvim-web-devicons',
      config = function() require'nvim-tree'.setup {} end
  }
  -- Auto pairs
  use 'jiangmiao/auto-pairs'
  -- Commnds
  use 'scrooloose/nerdcommenter'
  -- Icons
  use 'ryanoasis/vim-devicons'
  -- Lualine and BufferLine
  use {
    'hoob3rt/lualine.nvim',
    requires = {'kyazdani42/nvim-web-devicons', opt = true}
  }
  use {'akinsho/bufferline.nvim', requires = 'kyazdani42/nvim-web-devicons'}
  -- LSP and Compe
  use 'neovim/nvim-lspconfig'
  use 'kabouzeid/nvim-lspinstall'
  use 'nvim-lua/completion-nvim'
  use 'nvim-lua/diagnostic-nvim'
  use 'glepnir/lspsaga.nvim'
  use 'onsails/lspkind-nvim'
  use 'ray-x/lsp_signature.nvim'
  use {
    "hrsh7th/nvim-cmp",
    requires = {
      "L3MON4D3/LuaSnip",
      "saadparwaiz1/cmp_luasnip",
      "hrsh7th/cmp-buffer",
      "hrsh7th/cmp-nvim-lsp",
      "hrsh7th/cmp-calc",
      "f3fora/cmp-spell",
      "hrsh7th/cmp-path",
    }
  }
  -- Telescope
  use {
    'nvim-telescope/telescope.nvim',
    requires = { {'nvim-lua/plenary.nvim'} }
  }
  -- TreeSitter
  use {
      'nvim-treesitter/nvim-treesitter',
      run = ':TSUpdate'
  }
  -- Git
  use 'lewis6991/gitsigns.nvim'
  -- Emmet
  use 'mattn/emmet-vim'
  -- Colorizer
  use 'norcalli/nvim-colorizer.lua'
end)
