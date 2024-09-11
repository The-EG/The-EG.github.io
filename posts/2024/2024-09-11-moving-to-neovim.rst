Moving to Neovim
================

:author: Taylor Talkington
:date: 2024-09-11
:tags: neovim, vscode, lua, windows-terminal

.. image:: /assets/nvim/neovim-hero.png

----

This could also be titled 'Running Away from Visual Studio Code!'

And it's not that VS Code is bad, but I came to a realization: I use it for
syntax highlighting and a terminal. Yes, it has more functionality than that,
especially with extensions, but that's really all I wanted from it.

And, there are other tools that accomplish those things that I like better, so
why not use them?

If I were running Linux I would use it as my IDE, essentially. Either Vim or
Emacs for editing files, terminals for running commands and scripts, and the
window manager file explorer for managing files.

I decided to take the same approach with Windows 11.

This is a long post, so here is each section:

- `Windows Terminal`_
- `Neovim`_
- `GUI`_
- `Neovim Plugins`_
- `Color Scheme`_
- `Vertical Rulers`_
- `Line Numbers`_
- `Syntax Highlighting`_
- `Tabs Spaces`_
- `Window Title`_
- `Git Integration`_
- `Spellcheck`_
- `Scrollbars`_
- `Statusline`_
- `Font Icons`_
- `A better vim.ui.select`_
- `The Whole Thing`_

Windows Terminal
----------------

Pretty much everything that comes below will be built off my choice of terminal
emulator. I find Windows Terminal to be really good these days! It does need
some configuration tweaking and additional profiles however.

Neovim
------

I was considering trying to get Emacs setup again, however I *hate* working with
lisp, so I looked at Vim again and found Neovim. Neovim uses Lua for
customization and extension.

Getting Neovim was straightforward, just use the installer from the `latest
release <https://github.com/neovim/neovim/releases>`_.

GUI
---

Unlike GVim or Emacs for Windows, Neovim does not come with a GUI. It is a
console application like Vim. This wasn't surprising but what was surprising is
that telling Windows to open a file directly with ``nvim.exe`` opened it up in
Windows Terminal, since I had it installed. 

This looked surprisingly good and I realized that Neovim doesn't *need* a GUI,
just run it in the terminal.

It does, however need configuration to look better.

Neovim Plugins
--------------

I quickly found that nearly all Neovim customizations are plugins and that most
are setup to be installed with a plugin manager. I chose to use `lazy.nvim
<https://github.com/folke/lazy.nvim>`_.

This does require having ``git``, but I already have Git for Windows installed
and it 'just worked.'

I found the documentation for ``lazy.nvim`` a bit vague and difficult to follow
from the perspective of never using Neovim or a plugin manager before. However,
the initial installation is straightforward enough:

1. Create a new user configuration file for Neovim. On Windows this is in 
   ``C:\users\<username>\AppData\Local\nvim`` and should be named ``init.lua``.

   .. code-block:: powershell

        PS C:\users\taylo\AppData\Local\nvim> nvim init.lua

2. Add the following line:

    .. code-block:: lua

        require('config.lazy')

3. Create a new set of folders within the nvim folder next to ``init.lua`` named
   lua and one within that named config:

   .. code-block:: text

        AppData\Local\nvim
         |-lua
         |  |-config
         |-init.lua

4. In the new ``lua\config`` folder create a new file ``lazy.lua``:

   .. code-block:: powershell

        PS C:\users\taylo\AppData\Local\nvim> nvim .\lua\config\lazy.lua

5. And put the following in ``lazy.lua``:

   .. code-block:: lua
    
        -- Bootstrap lazy.nvim
        local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
        if not (vim.uv or vim.loop).fs_stat(lazypath) then
          local lazyrepo = "https://github.com/folke/lazy.nvim.git"
          local out = vim.fn.system({ "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath })
          if vim.v.shell_error ~= 0 then
            vim.api.nvim_echo({
              { "Failed to clone lazy.nvim:\n", "ErrorMsg" },
              { out, "WarningMsg" },
              { "\nPress any key to exit..." },
            }, true, {})
            vim.fn.getchar()
            os.exit(1)
          end
        end
        vim.opt.rtp:prepend(lazypath)

        -- Make sure to setup `mapleader` and `maplocalleader` before
        -- loading lazy.nvim so that mappings are correct.
        -- This is also a good place to setup other settings (vim.opt)
        vim.g.mapleader = " "
        vim.g.maplocalleader = "\\"

        -- Setup lazy.nvim
        require("lazy").setup({
          spec = {
            -- import your plugins
            { import = "plugins" },
          },
          -- Configure any other settings here. See the documentation for more details.
          -- colorscheme that will be used when installing plugins.
          install = { colorscheme = { "habamax" } },
          -- automatically check for plugin updates
          checker = { enabled = true },
        })

6. Restart Neovim and run ``:checkhealth lazy``.
7. Create a new folder named ``plugins`` in the lua folder

   .. code-block:: text

        AppData\Local\nvim
         |-lua
         |  |-config
         |  |  |-lazy.lua
         |  |-plugins
         |-init.lua

Now, each plugin or group of plugins can be defined by creating a Lua file in
``plugins``.

Color Scheme
------------

Neovim supports coloschemes like any other editor. I use `Nightfox
<https://github.com/EdenEast/nightfox.nvim?tab=readme-ov-file>`_.

Of course, it is a plugin, so install it using ``lazy.nvim``:

1. Create a file in ``~\nvim\lua\plugins\`` called ``colorschemes.lua``:

    .. code-block:: powershell

        PS C:\users\taylo\AppData\Local\nvim> nvim .\lua\plugins\colorschemes.lua

2. Put the following in ``colorschemes.lua``:

   .. code-block:: lua

        return {
            { "EdenEast/nightfox.nvim" },
        }

   This returns a table with a single entry for Nightfox. With this setup, it is
   possible to add additional entries for more color schemes later.

3. Run ``:Lazy install`` within nvim to install the color scheme.
4. Open the main Neovim configuration file, ``init.lua``:

   .. code-block:: powershell

        PS C:\users\taylo\AppData\Local\nvim> nvim init.lua

5. Add the following lines:

   .. code-block:: lua

        vim.o.background = nil -- disable the default background

        require('nightfox').setup({
            options = { transparent = true }, -- disable the background completely
        })

        vim.cmd('colorscheme carbonfox') -- use the Carbonfox variant

   This sets up Nightfox and selects the Carbonfox variant as the color scheme
   for all new windows. Additionally, ``options = { transparent = true }``
   disables the background color completely. This means that the background
   color and transparency in the current Windows-Terminal profile will be used
   instead, which is a nice effect. It does require coordinating the Windows
   Terminal and Neovim color scheme settings, however.

Now things look better, but it's not quite there yet.

Vertical Rulers
---------------

I like having rulers, or visual indicators showing where columns 80 and 120 are
for code formatting.

Luckily this is pretty simple, just a single line added to ``init.lua``:

.. code-block:: lua

    vim.opt.colorcolumn = '80,120'

Line Numbers
------------

Enabling line numbers display is just as easy, add the following to ``init.lua``:

.. code-block:: lua

    vim.opt.number = true

Syntax Highlighting
-------------------

The color scheme makes things look much better and Neovim comes with syntax 
highlighting rules for many languages, however they are pretty basic.

I decided to use `nvim-treesitter <https://github.com/nvim-treesitter/nvim-treesitter>`_.

The only downside to treesitter is that it requires a working c/c++ toolchain
to be in PATH when it first loads a parser for a particular language. This
sounds intimidating, but it's really as simple as running ``nvim`` from 
either ``Developer Command Prompt for VS`` or ``Developer Power Shell for VS``
whenever a parser needs to be built. 

In other words, when opening a new file type for the first time, run ``nvim``
from a developer prompt.

Otherwise, the setup for ``nvim-treesitter`` is pretty simple:

1. Create a plugin spec for it:

   .. code-block:: powershell

        PS C:\users\taylo\AppData\Local\nvim> nvim .\lua\plugins\treesitter.lua

   With the following content:

   .. code-block:: lua

        return { "nvim-treesitter/nvim-treesitter" }

2. And add the following to the main Neovim configuration (``init.lua`` ):

   .. code-block:: lua

        require('nvim-treesitter.configs').setup({
            ensure_installed = {
                "c",
                "cpp",
                "glsl",
                "json",
                "yaml",
                "lua",
                "vim",
                "vimdoc",
                "query",
                "markdown",
                "markdown_inline",
                "rst"
            },
            sync_install = false,
            auto_install = true,
            highlight = {
                enable = true,
            },
        })

   The ``ensure_installed`` key will pre-install parsers for those languages.
   All others will be installed the first time they a file with that type is
   opened.

3. Close and reopen nvim *from a developer command/powershell*.

At this point treesitter will build and install the parsers mentioned above.
Now that those parsers are installed, nvim can be opened without needing to
worry about msvc being accessible in the path.

Now syntax highlighting works well. However, it doesn't always detect the file
type properly, in particular GLSL when the files have ``.vert`` or ``.frag``
extensions.

This can be setup with the following lines in ``init.lua``:

.. code-block:: lua

    vim.filetype.add({
        extension = {
            frag = "glsl",
            vert = "glsl",
        }
    })

.. role:: strikethrough
   :class: text-decoration-line-through

:strikethrough:`Tabs` Spaces
----------------------------

I like spaces instead of tabs, and specifically 4. This is also an easy change
to ``init.lua``:

.. code-block:: lua

    vim.opt.tabstop = 4
    vim.opt.shiftwidth = 4
    vim.opt.expandtab = true

Window Title
------------

So far the only downside to using Neovim through Windows terminal is the title
shown in the taskbar isn't the filename. This is fixed by adding the following
to ``init.lua``:

.. code-block:: lua

    vim.opt.title = true
    vim.opt.titlestring = [[%t - %{expand('%:p:h')}]]

The first line enables setting the title and the second formats what is shown:

.. code-block:: text

    <filename> - <path>


Git Integration
---------------

One 'nice to have' from VS Code that I thought I may have to give up with Git
integration, specifically highlighting changes and showing line blame.

I was pleasantly surprised to find that `gitsigns.nvim <https://github.com/lewis6991/gitsigns.nvim>`_
handles both of those things and more quite nicely.

As with other plugins, create a spec in ``~\nvim\lua\plugins\git.lua``:

.. code-block:: lua

    return {
        { url = "git@github.com:lewis6991/gitsigns.nvim.git" },
    }

And add the following to the Neovim configuration ``init.lua``:

.. code-block:: lua

    require('gisigns').setup({
        signcolumn = true,
        current_line_blame = true,
        attach_to_untracked = true,
    })

Spellcheck
----------

Enabling spell check is another easy addition to ``init.lua``:

.. code-block:: lua

   vim.opt.spell = true

Scrollbars
----------

Even though Neovim is a console application it does support mouse interactions.

It doesn't come with a vertical scrollbar by default, however, but the
`nvim-scrollview <https://github.com/dstein64/nvim-scrollview>`_ plugin works
nicely.

Just create a plugin spec for it in ``~\nvim\lua\plugins\scrollview.lua``:

.. code-block:: lua

    return {        
        { 'dstein64/nvim-scrollview' }
    }

Once it's installed, that's it. It works automatically.

Statusline
----------

The default status line in Neovim is a little sparse. I like to see the file
format (line endings) and encoding at a minimum.

There are multiple status line plugins out there, but I settled on `feline.nvim
<https://github.com/freddiehaddad/feline.nvim>`_

Just like other plugins, create a Lazy spec for it in ``~\nvim\lua\plugins\statusline.lua``:

.. code-block:: lua

    return {
        {'freddiehaddad/feline.nvim'},
    }

Unlike most of the other plugins up to this point, Feline is going to require
some more effort to get it looking how I want it.

It's not overly difficult, though and it all goes into ``init.lua``:

.. code-block:: lua

    -- load Feline and providers    
    local feline = require('feline')
    local vi_mode_utils = require('feline.providers.vi_mode')

    -- The status line is made up of components.
    -- A different set of components is show for active and inactive states.
    -- I don't use inactive windows so I just leave that set empty
    local statusline_components = {
        active = {},
        inactive = {},
    }

    -- The first group of components is left aligned
    statusline_components.active[1] = {
        -- this first component is just a block/spacer character
        {
            provider = '▊ ',
            hl = {
                fg = 'skyblue',
            },
        },
        -- next is the Vim mode indicator
        {
            provider = 'vi_mode',
            hl = function()
                return {
                    name = vi_mode_utils.get_mode_highlight_name(),
                    fg = vi_mode_utils.get_mode_color(),
                    style = 'bold',
                }
            end,
        },
        -- File name and type
        {
            provider = {
                name = 'file_info',
                opts = {
                    colored_icon = false,
                },
            },
            hl = {
                fg = 'white',
                bg = 'oceanblue',
                style = 'bold',
            },
            left_sep = {
                'slant_left_2',
                { str = ' ', hl = { bg = 'oceanblue', fg = 'NONE' } },
            },
            right_sep = {
                { str = ' [', hl = { bg = 'oceanblue', fg = 'white' } },
            },
        },
        {
            provider = {
                name = 'file_type',
                opts = {
                    case = 'lowercase',
                },
            },
            hl = {
                fg = 'white',
                bg = 'oceanblue',
            },
            right_sep = {
                { str = ']', hl = { bg = 'oceanblue', fg = 'white' } },
                { str = ' ', hl = { bg = 'oceanblue', fg = 'NONE' } },
                'slant_right_2',
                ' ',
            },
        },
        -- File Size
        {
            provider = 'file_size',
            right_sep = {
                ' ',
                {
                    str = 'vertical_bar',
                    hl = {
                        fg = 'oceanblue',
                        bg = 'bg',
                    },
                },
            },
        },
        -- Row:Col
        {
            provider = 'position',
            left_sep = ' ',
            right_sep = {
                ' ',
                {
                    str = 'vertical_bar',
                    hl = {
                        fg = 'oceanblue',
                        bg = 'bg',
                    },
                },
            },
        },
        -- File Format
        {
            provider = 'file_format',
            left_sep = ' ',
            right_sep = {
                ' ',
                {
                    str = 'vertical_bar',
                    hl = { fg = 'oceanblue', bg = 'bg' },
                }
            },
        },
        -- Encoding
        {
            provider = 'file_encoding',
            left_sep = ' ',
        },
    }

    -- the next group is right aligned    
    statusline_components.active[2] = {
        -- Git branch
        {
            provider = 'git_branch',
            hl = {
                fg = 'white',
                bg = 'black',
                style = 'bold',
            },
            right_sep = {
                str = ' ',
                hl = {
                    fg = 'NONE',
                    bg = 'black',
                },
            },
        },
        -- Git changes
        {
            provider = 'git_diff_added',
            hl = {
                fg = 'green',
                bg = 'black',
            },
        },
        {
            provider = 'git_diff_changed',
            hl = {
                fg = 'orange',
                bg = 'black',
            },
        },
        {
            provider = 'git_diff_removed',
            hl = {
                fg = 'red',
                bg = 'black',
            },
            right_sep = {
                str = ' ',
                hl = {
                    fg = 'NONE',
                    bg = 'black',
                },
            },
        },
        -- File position %
        {
            provider = 'line_percentage',
            hl = {
                style = 'bold',
            },
            left_sep = '  ',
            right_sep = ' ',
        },
        {
            provider = 'scroll_bar',
            hl = {
                fg = 'skyblue',
                style = 'bold',
            },
        },
    }

    -- finally, tell Feline to use our custom component setup
    feline.setup({components = statusline_components})

At this point the status line has all the information I wanted, but it doesn't
look as nice as the Felin examples. That is because Feline needs a patched font
to use the icons and symbols. That's next.

Font Icons
----------

Getting the symbols and icons for Feline and other plugins requires a patched
font. This is simpler than it sounds.

First, `nvim-web-devicons <https://github.com/nvim-tree/nvim-web-devicons>`_ is
needed.

Since I'm primarily installing this for the status line I added it to
``~\lua\plugins\statusline.lua``:

.. code-block:: lua

    return {
        {'freddiehaddad/feline.nvim'},
        {'nvim-tree/nvim-web-devicons'},
    }

Next is installing an actual patched font. I went with a patched Cascadia Code
(which is called 'Caskaydia Cove') from
`Nerd Fonts <https://github.com/ryanoasis/nerd-fonts>`_. 

The only catch here is that it needs to be installed to the system folder, not
the user fonts folder. That can be done by holding shift while right clicking 
on the downloaded ``.ttf`` and selecting 'Install for all users'.

Once installed, select the font within Windows Terminal.

Now the status line is looking nice!

gitmoji
-------

I have become accustomed to using `gitmojis <https://gitmoji.dev/>`_ in my git
commit messages. In VSCode this is made easy with an extension. There are a few
Neovim plugins for this, but the ones I came across required other plugins that
I had no interest in using, especially given how simple this is:

I just want to pick an emoji from a list with descriptions and have that
inserted into the editor.

Luckily this is fairly simple. I came up with this after looking at a few of the
existing plugins (all of this can go into ``init.lua``):

.. code-block:: lua

    local gitmojis = {
        {'🎨', 'Improve structure/format of the code.'},
        {'⚡️', 'Improve performance.'},
        {'🔥', 'Remove code or files.'},
        {'🐛', 'Fix a bug.'},
        {'🚑️', 'Critical hotfix.'},
        {'✨', 'Introduce new features.'},
        {'📝', 'Add or update documentation.'},
        {'🚀', 'Deploy stuff.'},
        {'💄', 'Add or update the UI and style files.'},
        {'🎉', 'Begin a project.'},
        {'✅', 'Add, update, or pass tests.'},
        {'🔒️', 'Fix security or privacy issues.'},
        {'🔐', 'Add or update secrets.'},
        {'🔖', 'Release/version tags.'},
        {'🚨', 'Fix compiler/linter warnings.'},
        {'🚧', 'Work in progress.'},
        {'💚', 'Fix CI build.'},
        {'⬇️' , 'Downgrade dependencies.'},
        {'⬆️' , 'Upgrade dependencies.'},
        {'📌', 'Pin dependencies to specific versions.'},
        {'👷', 'Add or update CI build system.'},
        {'📈', 'Add or update analytics or track code.'},
        {'♻️' , 'Refactor code.'},
        {'➕', 'Add a dependency.'},
        {'➖', 'Remove a dependency.'},
        {'🔧', 'Add or update configuration files.'},
        {'🔨', 'Add or update development scripts.'},
        {'🌐', 'Internationalization and localization.'},
        {'✏️' , 'Fix tyops.'},
        {'💩', 'Write bad code that needs to be improved.'},
        {'⏪️', 'Revert changes.'},
        {'🔀', 'Merge branches.'},
        {'📦️', 'Add or update compiled files or packages.'},
        {'👽️', 'Update code due to external API changes.'},
        {'🚚', 'Move or rename resources (e.g.: files, paths, routes).'},
        {'📄', 'Add or update license.'},
        {'💥', 'Introduce breaking changes.'},
        {'🍱', 'Add or update assets.'},
        {'♿️', 'Improve accessibility.'},
        {'💡', 'Add or update comments in source code.'},
        {'🍻', 'Write code drunkenly.'},
        {'💬', 'Add or update text and literals.'},
        {'🗃️', 'Perform database related changes.'},
        {'🔊', 'Add or update logs.'},
        {'🔇', 'Remove logs.'},
        {'👥', 'Add or update contributor(s).'},
        {'🚸', 'Improve user experience/usability.'},
        {'🏗️', 'Make architectural changes.'},
        {'📱', 'Work on responsive design.'},
        {'🤡', 'Mock things.'},
        {'🥚', 'Add or update easter egg.'},
        {'🙈', 'Add or update .gitignore file.'},
        {'📸', 'Add or update snapshots.'},
        {'⚗️' , 'Perform experiments.'},
        {'🔍️', 'Improve SEO.'},
        {'🏷️', 'Add or update types.'},
        {'🌱', 'Add or update seed files.'},
        {'🚩', 'Add, update, or remove feature flags.'},
        {'🥅', 'Catch errors.'},
        {'💫', 'Add or update animations and transitions.'},
        {'🗑️', 'Deprecate code that needs to be cleaned up.'},
        {'🛂', 'Work on code related to authorization, roles, and permissions.'},
        {'🩹', 'Simple fix for a non-critical issue.'},
        {'🧐', 'Data exploration/inspection.'},
        {'⚰️' , 'Remove dead code.'},
        {'🧪', 'Add a failing test.'},
        {'👔', 'Add or update business logic.'},
        {'🩺', 'Add or update healthcheck.'},
        {'🧱', 'Infrastructure related changes.'},
        {'🧑‍💻', 'Improve developer experience.'},
        {'💸', 'Add sponsorships or money related infrastructure.'},
        {'🧵', 'Add or update code related to multithreading or concurrency.'},
        {'🦺', 'Add or update code related to validation.'},
    }

    local function gitmoji_select()
        vim.ui.select(gitmojis, {
            prompt = "Select Gitmoji",
            format_item = function(i) return string.format('%s - %s', i[1], i[2]) end,
        }, function(choice)
            if choice==nil then
                vim.print("Gitmoji canceled.")
            else
                vim.cmd('normal! i'.. choice[1] .. ' ')
            end
        end)
    end

    vim.api.nvim_create_user_command('Gitmoji', gitmoji_select, { nargs = 0 })

Now when the ``:Gitmoji`` command is run within Neovim, the Gitmoji list is
displayed and the appropriate unicode emoji is inserted. This is handy because
I now use Neovim as my commit message editor as well.

.. note::

   Unfortunately, this doesn't allow for completion/searching through the list
   of descriptions. Maybe I'll figure that out later :)

A better vim.ui.select
-----------------------

After implementing my ``:Gitmoji`` command above I realized that the reason all
of the other solutions required some other plugin is because the default
``vim.ui.select`` is a little underwhelming.

But, rather than going down a route that requires a specific plugin, I decided
to use
`dressing.nvim <https://github.com/stevearc/dressing.nvim?tab=readme-ov-file>`_
which replaces ``vim.ui.select`` in a configurable way.

Create a new plugin spec for it in ``~\nvim\lua\plugins\uiselect.lua``:

.. code-block:: lua

    return {
        { 'stevearc/dressing.nvim' }
    }

And that's it, our ``:Gitmoji`` command looks much nicer.

Except, not everything is using ``vim.ui.select`` it would seem. The spell
checker replace misspelled work command (``z=``) still looks the same.

I found a quick solution from a closed PR for this (added to ``init.lua``):

.. code-block:: lua

    -- change the z= (replace misspelled word) to use vim.ui.select
    -- https://github.com/neovim/neovim/pull/25833/files
    local spell_on_choice = vim.schedule_wrap(function(_, idx)
        if type(idx) == 'number' then
            vim.cmd.normal({ idx .. 'z=', bang = true })
        end
    end)

    local function spell_select()
        if vim.v.count > 0 then
            spell_on_choice(nil, vim.v.count)
            return
        end
        local cword = vim.fn.expand('<cword>')
        vim.ui.select(
            vim.fn.spellsuggest(cword, vim.o.lines),
            { prompt = 'Change ' .. cword .. ' to:' },
            spell_on_choice
        )
    end
    vim.keymap.set('n', 'z=', spell_select, { desc = 'Shows spelling suggestions' })

The Whole Thing
---------------

The entire ``init.lua`` with everything above:

.. code-block:: lua


    vim.opt.title = true
    vim.opt.titlestring = [[%t - %{expand('%:p:h')}]]

    require('config.lazy')

    require('gitsigns').setup({
        signcolumn = true,
        current_line_blame = true,
        attach_to_untracked = true,
    })

    vim.o.background = nil

    require('nightfox').setup({
        options = {transparent = true},
    })

    -- colorscheme
    vim.cmd('colorscheme carbonfox')

    vim.opt.colorcolumn = '80,120'

    vim.opt.tabstop = 4
    vim.opt.shiftwidth = 4
    vim.opt.expandtab = true

    vim.opt.number = true

    vim.opt.spell = true
    vim.opt.spelllang = 'en_us'


    -- change the z= (replace misspelled word) to use vim.ui.select
    -- https://github.com/neovim/neovim/pull/25833/files
    local spell_on_choice = vim.schedule_wrap(function(_, idx)
        if type(idx) == 'number' then
            vim.cmd.normal({ idx .. 'z=', bang = true })
        end
    end)

    local function spell_select()
        if vim.v.count > 0 then
            spell_on_choice(nil, vim.v.count)
            return
        end
        local cword = vim.fn.expand('<cword>')
        vim.ui.select(
            vim.fn.spellsuggest(cword, vim.o.lines),
            { prompt = 'Change ' .. cword .. ' to:' },
            spell_on_choice
        )
    end
    vim.keymap.set('n', 'z=', spell_select, { desc = 'Shows spelling suggestions' })

    -- treesitter
    require('nvim-treesitter.configs').setup({
        ensure_installed = {
            "c",
            "cpp",
            "glsl",
            "json",
            "yaml",
            "lua",
            "vim",
            "vimdoc",
            "query",
            "markdown",
            "markdown_inline",
            "rst"
        },
        sync_install = false,
        auto_install = true,
        highlight = {
            enable = true,
        },
    })

    vim.filetype.add({
        extension = {
            frag = "glsl",
            vert = "glsl",
        }
    })

    local feline = require('feline')
    local vi_mode_utils = require('feline.providers.vi_mode')

    local statusline_components = {
        active = {},
        inactive = {},
    }

    statusline_components.active[1] = {
        {
            provider = '▊ ',
            hl = {
                fg = 'skyblue',
            },
        },
        {
            provider = 'vi_mode',
            hl = function()
                return {
                    name = vi_mode_utils.get_mode_highlight_name(),
                    fg = vi_mode_utils.get_mode_color(),
                    style = 'bold',
                }
            end,
        },
        {
            provider = {
                name = 'file_info',
                opts = {
                    colored_icon = false,
                },
            },
            hl = {
                fg = 'white',
                bg = 'oceanblue',
                style = 'bold',
            },
            left_sep = {
                'slant_left_2',
                { str = ' ', hl = { bg = 'oceanblue', fg = 'NONE' } },
            },
            right_sep = {
                { str = ' [', hl = { bg = 'oceanblue', fg = 'white' } },
            },
        },
        {
            provider = {
                name = 'file_type',
                opts = {
                    case = 'lowercase',
                },
            },
            hl = {
                fg = 'white',
                bg = 'oceanblue',
            },
            right_sep = {
                { str = ']', hl = { bg = 'oceanblue', fg = 'white' } },
                { str = ' ', hl = { bg = 'oceanblue', fg = 'NONE' } },
                'slant_right_2',
                ' ',
            },
        },
        {
            provider = 'file_size',
            right_sep = {
                ' ',
                {
                    str = 'vertical_bar',
                    hl = {
                        fg = 'oceanblue',
                        bg = 'bg',
                    },
                },
            },
        },
        {
            provider = 'position',
            left_sep = ' ',
            right_sep = {
                ' ',
                {
                    str = 'vertical_bar',
                    hl = {
                        fg = 'oceanblue',
                        bg = 'bg',
                    },
                },
            },
        },
        {
            provider = 'file_format',
            left_sep = ' ',
            right_sep = {
                ' ',
                {
                    str = 'vertical_bar',
                    hl = { fg = 'oceanblue', bg = 'bg' },
                }
            },
        },
        {
            provider = 'file_encoding',
            left_sep = ' ',
        },
    }

    statusline_components.active[2] = {
        {
            provider = 'git_branch',
            hl = {
                fg = 'white',
                bg = 'black',
                style = 'bold',
            },
            right_sep = {
                str = ' ',
                hl = {
                    fg = 'NONE',
                    bg = 'black',
                },
            },
        },
        {
            provider = 'git_diff_added',
            hl = {
                fg = 'green',
                bg = 'black',
            },
        },
        {
            provider = 'git_diff_changed',
            hl = {
                fg = 'orange',
                bg = 'black',
            },
        },
        {
            provider = 'git_diff_removed',
            hl = {
                fg = 'red',
                bg = 'black',
            },
            right_sep = {
                str = ' ',
                hl = {
                    fg = 'NONE',
                    bg = 'black',
                },
            },
        },
        {
            provider = 'line_percentage',
            hl = {
                style = 'bold',
            },
            left_sep = '  ',
            right_sep = ' ',
        },
        {
            provider = 'scroll_bar',
            hl = {
                fg = 'skyblue',
                style = 'bold',
            },
        },
    }

    feline.setup({components = statusline_components})
    -- feline.winbar.setup()
    --feline.statuscolumn.setup()


    local gitmojis = {
        {'🎨', 'Improve structure/format of the code.'},
        {'⚡️', 'Improve performance.'},
        {'🔥', 'Remove code or files.'},
        {'🐛', 'Fix a bug.'},
        {'🚑️', 'Critical hotfix.'},
        {'✨', 'Introduce new features.'},
        {'📝', 'Add or update documentation.'},
        {'🚀', 'Deploy stuff.'},
        {'💄', 'Add or update the UI and style files.'},
        {'🎉', 'Begin a project.'},
        {'✅', 'Add, update, or pass tests.'},
        {'🔒️', 'Fix security or privacy issues.'},
        {'🔐', 'Add or update secrets.'},
        {'🔖', 'Release/version tags.'},
        {'🚨', 'Fix compiler/linter warnings.'},
        {'🚧', 'Work in progress.'},
        {'💚', 'Fix CI build.'},
        {'⬇️' , 'Downgrade dependencies.'},
        {'⬆️' , 'Upgrade dependencies.'},
        {'📌', 'Pin dependencies to specific versions.'},
        {'👷', 'Add or update CI build system.'},
        {'📈', 'Add or update analytics or track code.'},
        {'♻️' , 'Refactor code.'},
        {'➕', 'Add a dependency.'},
        {'➖', 'Remove a dependency.'},
        {'🔧', 'Add or update configuration files.'},
        {'🔨', 'Add or update development scripts.'},
        {'🌐', 'Internationalization and localization.'},
        {'✏️' , 'Fix tyops.'},
        {'💩', 'Write bad code that needs to be improved.'},
        {'⏪️', 'Revert changes.'},
        {'🔀', 'Merge branches.'},
        {'📦️', 'Add or update compiled files or packages.'},
        {'👽️', 'Update code due to external API changes.'},
        {'🚚', 'Move or rename resources (e.g.: files, paths, routes).'},
        {'📄', 'Add or update license.'},
        {'💥', 'Introduce breaking changes.'},
        {'🍱', 'Add or update assets.'},
        {'♿️', 'Improve accessibility.'},
        {'💡', 'Add or update comments in source code.'},
        {'🍻', 'Write code drunkenly.'},
        {'💬', 'Add or update text and literals.'},
        {'🗃️', 'Perform database related changes.'},
        {'🔊', 'Add or update logs.'},
        {'🔇', 'Remove logs.'},
        {'👥', 'Add or update contributor(s).'},
        {'🚸', 'Improve user experience/usability.'},
        {'🏗️', 'Make architectural changes.'},
        {'📱', 'Work on responsive design.'},
        {'🤡', 'Mock things.'},
        {'🥚', 'Add or update easter egg.'},
        {'🙈', 'Add or update .gitignore file.'},
        {'📸', 'Add or update snapshots.'},
        {'⚗️' , 'Perform experiments.'},
        {'🔍️', 'Improve SEO.'},
        {'🏷️', 'Add or update types.'},
        {'🌱', 'Add or update seed files.'},
        {'🚩', 'Add, update, or remove feature flags.'},
        {'🥅', 'Catch errors.'},
        {'💫', 'Add or update animations and transitions.'},
        {'🗑️', 'Deprecate code that needs to be cleaned up.'},
        {'🛂', 'Work on code related to authorization, roles, and permissions.'},
        {'🩹', 'Simple fix for a non-critical issue.'},
        {'🧐', 'Data exploration/inspection.'},
        {'⚰️' , 'Remove dead code.'},
        {'🧪', 'Add a failing test.'},
        {'👔', 'Add or update business logic.'},
        {'🩺', 'Add or update healthcheck.'},
        {'🧱', 'Infrastructure related changes.'},
        {'🧑‍💻', 'Improve developer experience.'},
        {'💸', 'Add sponsorships or money related infrastructure.'},
        {'🧵', 'Add or update code related to multithreading or concurrency.'},
        {'🦺', 'Add or update code related to validation.'},
    }

    local function gitmoji_select()
        vim.ui.select(gitmojis, {
            prompt = "Select Gitmoji",
            format_item = function(i) return string.format('%s - %s', i[1], i[2]) end,
        }, function(choice)
            if choice==nil then
                vim.print("Gitmoji canceled.")
            else
                vim.cmd('normal! i'.. choice[1] .. ' ')
            end
        end)
    end

    vim.api.nvim_create_user_command('Gitmoji', gitmoji_select, { nargs = 0 })
