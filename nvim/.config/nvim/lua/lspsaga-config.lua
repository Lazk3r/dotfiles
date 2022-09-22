local saga = require 'lspsaga'

saga.init_lsp_saga {
  error_sign = '',
  warn_sign = '',
  hint_sign = '',
  infor_sign = '',
}

vim.cmd([[
nnoremap <silent> gh :Lspsaga lsp_finder<CR>
nnoremap <silent> gs :Lspsaga signature_help<CR>
nnoremap <leader>rn :Lspsaga rename<CR>
nnoremap <leader>pd :Lspsaga preview_definition<CR>
]])
