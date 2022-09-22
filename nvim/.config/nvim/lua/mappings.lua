vim.cmd([[
" Use alt + hjkl to resize windows
nnoremap <M-j>    :resize -2<CR>
nnoremap <M-k>    :resize +2<CR>
nnoremap <M-h>    :vertical resize -2<CR>
nnoremap <M-l>    :vertical resize +2<CR>

" TAB in general mode will move to text buffer
nnoremap <TAB> :bnext<CR>
" SHIFT-TAB will go back
nnoremap <S-TAB> :bprevious<CR>

" Don't use ESC
inoremap jk <Esc>
inoremap kj <Esc>

" Better tabbing
vnoremap < <gv
vnoremap > >gv

" Better window navigation
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" NERDTREE
nnoremap <leader>e :NvimTreeToggle<CR>

" Format
nnoremap <leader>i :Format<CR>

" Git
"nnoremap <leader>gs :Git status<CR>
"nnoremap <leader>ga :Git add .<CR>
"nnoremap <leader>gc :Git commit -m ""
"nnoremap <leader>gps :Git push<CR>
"nnoremap <leader>gpl :Git pull<CR>

" Alternative to save and close
nmap <leader>s :w<CR>
nmap <leader>x :wq<CR>
nmap <leader>q :q!<CR>

" Close a buffer
nmap <leader>w :bd<CR>

" Search
nmap <leader>h :nohlsearch<CR>

" Terminal
nnoremap <leader>t :split<CR>:term<CR>:resize 12<CR>i
tnoremap <Esc> <C-\><C-n>
tnoremap jk <C-\><C-n>
tnoremap kj <C-\><C-n>
tnoremap <C-h> <C-\><C-n><C-w>h
tnoremap <C-j> <C-\><C-n><C-w>j
tnoremap <C-k> <C-\><C-n><C-w>k
tnoremap <C-l> <C-\><C-n><C-w>l
nnoremap <silent> <F11> :set spell!<CR>
]])
