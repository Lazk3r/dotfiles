vim.list_extend(lvim.lsp.automatic_configuration.skipped_servers, { "pyright", "jsonls" })

local pyright_opts = {
    single_file_support = true,
    settings = {
        pyright = {
            disableLanguageServices = false,
            disableOrganizeImports = false,
            useLibraryCodeForTypes = true,
        },
        python = {
            analysis = {
                autoImportCompletions = true,
                autoSearchPaths = true,
                diagnosticMode = "workspace", -- openFilesOnly, workspace
                typeCheckingMode = "basic", -- off, basic, strict
                useLibraryCodeForTypes = true,
            },
        },
    },
}

require("lvim.lsp.manager").setup("pyright", pyright_opts)
