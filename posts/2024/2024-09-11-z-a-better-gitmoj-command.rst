A Better Gitmoji command (for Neovim)
=====================================

:author: Taylor Talkington
:date: 2024-09-11
:tags: neovim, git, lua

After writing the post about
`setting up Neovim <{filename}2024-09-11-moving-to-neovim.rst>`_ I got to
thinking about the ``:Gitmoji`` command I made and a better way of doing it.

It works well enough, but since there are over 70 different emojis, finding one
in the list can be a bit difficult. A way to filter the list would be nice.

It turns out that using ``vim.ui.input`` for this instead of ``vim.ui.select``
is possible, but I couldn't find any examples of using a custom completion
function from Lua.

I was able to get it working after some trial and error, but it requires a
little more setup than just adding code to ``init.lua``.

Instead, this needs to be housed within it's own module, i.e. ``~\nvim\lua\gitmoji.lua``
folder.

We still need the list of emoji and descriptions:

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
        {'✏️' , 'Fix typos.'},
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

Next, define a table to hold our module and the actual functions:

.. code-block:: lua

    local M = {}

    function M.complete_gitmoji(arglead, cmdline, cursorpos)

        local matches = {}
        for i, g in ipairs(gitmojis) do
            if string.match(string.lower(g[2]), string.lower(cmdline)) then
                table.insert(matches, string.format('%s - %s', g[1], g[2]))
            end
        end
        return table.concat(matches, '\n')
    end

    local function oncomplete(text)
        if not text then return end

        local description = string.match(text, '. %- (.+)')

        if not description then
            print('Invalid selection.')
            return
        end

        for i,g in ipairs(gitmojis) do
            if g[2]==description then
                vim.cmd('normal! i' .. g[1] .. ' ')
                return
            end
        end

        print('Invalid gitmoji: ' .. description)
    end

    vim.api.nvim_create_user_command('Gitmoji', function()
        vim.ui.input({
            prompt = 'Select Gitmoji (type a partial description and press tab):',
            completion = "custom,v:lua.require'gitmoji'.complete_gitmoji",
        }, oncomplete)
    end, { nargs = 0 })

    return M

``complete_gitmoji`` is called when the user presses ``tab`` when the input
window is open. The ``cmdline`` parameter contains the entire line of text from
the input box. This is used to filter the list of gitmojis, which are returned
as a newline separated list.

``oncomplete`` is called when the user either cancels or selects a gitmoji. This
function compares the text with all of the gitmoji descriptions. If one matches,
it inserts that unicode gitmoji into the buffer. If the there is no match it
displays a message instead.

The real magic is in the call to ``vim.ui.input``. The ``completion`` option
specifies how the autocompletion is performed, in this case, our module is
loaded and the ``complete_gitmoji`` function is called.

Finally, just load the module in ``init.lua``:

.. code-block:: lua

    require('gitmoji')
