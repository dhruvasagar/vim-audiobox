" =============================================================================
" File:          plugin/audiobox.vim
" Description:   Vim plugin to control audiobox playback.
" Author:        Dhruva Sagar <http://dhruvasagar.com/>
" License:       MIT (http://www.opensource.org/licenses/MIT)
" Website:       http://github.com/dhruvasagar/vim-audiobox
" Version:       0.2
" Copyright Notice:
"                Permission is hereby granted to use and distribute this code,
"                with or without modifications, provided that this copyright
"                notice is copied with it. Like anything else that's free,
"                table-mode.vim is provided *as is* and comes with no warranty
"                of any kind, either expressed or implied. In no event will
"                the copyright holder be liable for any damamges resulting
"                from the use of this software.
" =============================================================================

" Init {{{1
if exists('g:loaded_audiobox')
  finish
endif
let g:loaded_audiobox = 1

if !has('python')
  echoerr 'This plugin depends on python, make sure vim is compiled with python support.'
  finish
endif

" Configuration {{{1
function! s:SetOption(opt, val)
  if !exists('g:' . a:opt) | let g:{a:opt} = a:val | endif
endfunction

let s:dbus_interface_prefix = 'org.mpris.MediaPlayer2'
call s:SetOption('audiobox_debug', 0)
call s:SetOption('audiobox_player', 'rhythmbox')
call s:SetOption('audiobox_dbus_path', '/org/mpris/MediaPlayer2')
call s:SetOption('audiobox_dbus_dest', s:dbus_interface_prefix . '.' . g:audiobox_player)
call s:SetOption('audiobox_dbus_interface', s:dbus_interface_prefix . '.' . 'Player')
call s:SetOption('audiobox_dbus_properties_interface', 'org.freedesktop.DBus.Properties')

let s:plugin_path = escape(expand('<sfile>:p:h'), '\')

if !exists('g:audiobox_py_loaded')
  python import sys, vim
  python if vim.eval('expand("<sfile>:p:h")') not in sys.path:
        \  sys.path.append(vim.eval('expand("<sfile>:p:h")'))
  python import audiobox
endif
let g:audiobox_py_loaded = 1

command! -bar AudioboxPlay python audiobox.setup() and audiobox.setup().Play()
command! -bar AudioboxNext python audiobox.setup() and audiobox.setup().Next()
command! -bar AudioboxPrev python audiobox.setup() and audiobox.setup().Prev()
command! -bar AudioboxPause python audiobox.setup() and audiobox.setup().Pause()
command! -bar AudioboxTogglePlay python audiobox.setup() and audiobox.setup().PlayPause()
command! -bar AudioboxShowCurrentSong python audiobox.setup() and audiobox.setup().GetCurrentSong()

nnoremap <silent> <Plug>AudioboxPlay :AudioboxPlay<CR>
nnoremap <silent> <Plug>AudioboxPause :AudioboxPause<CR>
nnoremap <silent> <Plug>AudioboxTogglePlay :AudioboxTogglePlay<CR>
nnoremap <silent> <Plug>AudioboxShowCurrentSong :AudioboxShowCurrentSong<CR>
nnoremap <silent> <Plug>AudioboxNext :AudioboxNext <Bar> AudioboxShowCurrentSong<CR>
nnoremap <silent> <Plug>AudioboxPrev :AudioboxPrev <Bar> AudioboxShowCurrentSong<CR>

if !hasmapto('<Plug>AudioboxPlay')
  nmap <Leader>ap <Plug>AudioboxPlay
endif
if !hasmapto('<Plug>AudioboxNext')
  nmap <Leader>an <Plug>AudioboxNext
endif
if !hasmapto('<Plug>AudioboxPrev')
  nmap <Leader>aN <Plug>AudioboxPrev
endif
if !hasmapto('<Plug>AudioboxPause')
  nmap <Leader>aP <Plug>AudioboxPause
endif
if !hasmapto('<Plug>AudioboxTogglePlay')
  nmap <Leader>at <Plug>AudioboxTogglePlay
endif
if !hasmapto('<Plug>AudioboxShowCurrentSong')
  nmap <Leader>as <Plug>AudioboxShowCurrentSong
endif
